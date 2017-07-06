# -*- coding: utf-8 -*-
import config
import telebot
import random
import Players
import tasks
import time

bot = telebot.TeleBot(config.token)
active_players = []

@bot.message_handler(content_types=["sticker"])
def sticker_parsing(message): 
    if message.from_user.username == "sverhmassivnaya":
        if message.sticker.file_id == 'CAADAgADHgAD6gKUEl9xLyPpAAFHBgI':
            bot.send_message(message.chat.id, "Погоди, сейчас выдам Дипа")
    elif message.from_user.username == "random_answer":
        for w in config.hi_stickers[:]:
            if message.sticker.file_id == w:
                bot.send_message(message.chat.id, random.choice(config.hi_citrus))
    bot.send_message(message.chat.id, message.sticker.file_id)

#find and append players
def findplayer(user):
     for w in active_players[:]:
        if w.user.id == user.id:
            return w
     player = Players.Player_state(user)
     active_players.append(player)
     return player

#collect players and give them tasks
@bot.message_handler(commands=["get_task"])
def task_send(message):
    player = findplayer(message.from_user)
    if time.time() -  player.last_task > config.seconds_in_day:
        player.task_status = 0
    if player.task_status == 1:
        bot.send_message(message.chat.id, "ТЫ УЖЕ ЧТО-ТО ДЕЛАЕШЬ!", reply_to_message_id = message.message_id)
    elif player.task_status == 2:
        bot.send_message(message.chat.id, "ТЫ УЖЕ НЕ СМОГ!", reply_to_message_id = message.message_id)
    elif player.task_status == 0:
        if time.time() -  player.last_task < config.seconds_in_day:
             bot.send_message(message.chat.id, "НОВОЕ ЗАДАНИЕ БУДЕТ ЗАВТРА!", reply_to_message_id = message.message_id)
        else:
            player.task_status = 1
            player.last_task = time.time()
            task = random.choice(config.tasks)
            bot.send_sticker(message.chat.id, task[0])
            bot.send_message(message.chat.id, task[1])
            player.task = tasks.Task(*task)

# root command. See all players with tasks.
@bot.message_handler(commands=["all_tasks"])
def task_send(message):
    for w in config.root[:]:
        if message.from_user.username == w:
            for x in active_players[:]:
                if x.task_status == 1:
                   bot.send_message(message.chat.id, x.to_string()) 

# root debug command. reset players
@bot.message_handler(commands=["refresh"])
def task_send(message):
    for w in config.root[:]:
        if message.from_user.username == w:
            active_players[:] = []

@bot.message_handler(commands=["help"])
def task_send(message):
    bot.send_message(message.chat.id, random.choice(config.help_list), reply_to_message_id = message.message_id)

@bot.message_handler(commands=["donate"])
def task_send(message):
    bot.send_message(message.chat.id, random.choice(config.donate_list), reply_to_message_id = message.message_id)

@bot.message_handler(commands=["roll"])
def task_send(message):
    bot.send_message(message.chat.id, random.randint(1,6), reply_to_message_id = message.message_id)

@bot.message_handler(content_types=["text"])
def message_parsing(message):
    if message.text == 'МОЛОДЕЦ!':
        if message.reply_to_message:
            for w in config.root[:]:
                if message.from_user.username == w:
                    player = findplayer(message.reply_to_message.from_user)
                    if player.task_status == 1:
                        player.task_status = 0
                        player.task_completed += 1
                        bot.send_message(message.chat.id, "ЗАДАНИЕ ВЫПОЛНЕНО!\nВСЕГО СДЕЛАНО " + str(player.task_completed) + " ЗАДАНИЙ", reply_to_message_id = message.reply_to_message.message_id)
    if message.text == 'ТЫ ДУРА?':
        if message.reply_to_message:
            for w in config.root[:]:
                if message.from_user.username == w: 
                    player = findplayer(message.reply_to_message.from_user)
                    if player.task_status == 1:
                        player.task_status = 2
                        bot.send_message(message.chat.id, "ЗАДАНИЕ ПРОВАЛЕНО!", reply_to_message_id = message.reply_to_message.message_id)
                    

if __name__ == '__main__':
    random.seed()
    bot.polling(none_stop=True)