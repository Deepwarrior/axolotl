# -*- coding: utf-8 -*-
import config
import telebot
import random
import players
import tasks
import time
import json

bot = telebot.TeleBot(config.token)
active_players = []

vip_chat_id = -1001107497089 #now it`s debug chat replace with: -1001090074308  #check.
debug_chat_id = -1001107497089


def jsonDefault(object):
    return object.__dict__

class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

#find and append players
def findplayer(user):
     for w in active_players[:]:
        if w.user.id == user.id:
            return w
     player = players.Player_state(user)
     active_players.append(player)
     return player

#collect players and give them tasks
@bot.message_handler(commands=["get_task"])
def task_send(message):
    if message.chat.id != vip_chat_id and  message.chat.id != debug_chat_id:
        bot.send_message(message.chat.id, "ПО ЛИЧКАМ ШУШУКАЕТЕСЬ? НЕ ТОТ ЧЯТИК!", reply_to_message_id = message.message_id) #check!!! # IMPORTANT
    else:
        player = findplayer(message.from_user)
        if time.time() -  player.last_task_time > config.seconds_in_day:
            player.task_status = 0
        if player.task_status == 1:
            bot.send_message(message.chat.id, "ТЫ УЖЕ ЧТО-ТО ДЕЛАЕШЬ!", reply_to_message_id = message.message_id)
        elif player.task_status == 2:
            bot.send_message(message.chat.id, "ТЫ УЖЕ НЕ СМОГ!", reply_to_message_id = message.message_id)
        elif player.task_status == 0:
            if time.time() -  player.last_task_time < config.seconds_in_day:
                bot.send_message(message.chat.id, "НОВОЕ ЗАДАНИЕ БУДЕТ ЗАВТРА!", reply_to_message_id = message.message_id)
            else:
                player.task_status = 1
                player.last_task_time = time.time()
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
                   bot.send_message(message.chat.id, players.to_string(x)) 

# root debug command. reset players
@bot.message_handler(commands=["refresh"])
def task_send(message):
    for w in config.root[:]:
        if message.from_user.username == w:
            active_players[:] = []

@bot.message_handler(commands=["help"])
def task_send(message):
    bot.send_message(message.chat.id, random.choice(config.help_list), reply_to_message_id = message.message_id)
    bot.send_message(message.chat.id, message.message_id)

@bot.message_handler(commands=["donate"])
def task_send(message):
    bot.send_message(message.chat.id, random.choice(config.donate_list), reply_to_message_id = message.message_id)

@bot.message_handler(commands=["backup"])
def task_send(message):
    f = open('players.json', 'w')
    json.dump(active_players, f, default=jsonDefault)
    f.close()

@bot.message_handler(content_types=["sticker"])
def sticker_parsing(message):
    for w in active_players[:]:
        if w.informed == False:
            if w.task.time:
                if time.time() - w.last_task_time >  w.task.time * 3600:
                    bot.send_message(debug_chat_id, players.to_string(w) + '\nВремя задания истекло! Оцените!')
                    w.informed = True
            if w.task.messages:
                if message.message_id - w.last_task_mssg >  w.task.messages:
                    bot.send_message(debug_chat_id, players.to_string(w) + '\nВсе сообщения написаны! Оцените!')
                    w.informed = True

    if message.from_user.username == "sverhmassivnaya":
        if message.sticker.file_id == 'CAADAgADHgAD6gKUEl9xLyPpAAFHBgI':
            bot.send_message(message.chat.id, "Погоди, сейчас выдам Дипа", reply_to_message_id = message.message_id)
    elif message.from_user.username == "random_answer":
        for w in config.hi_stickers[:]:
            if message.sticker.file_id == w:
                bot.send_message(message.chat.id, random.choice(config.hi_citrus), reply_to_message_id = message.message_id)
    if message.sticker.file_id == 'CAADAgADpgEAAmDrzgNSIT8rlE3K0AI':
        for w in config.root[:]:
            if message.from_user.username == w:
                player = findplayer(message.reply_to_message.from_user)
                if player.task:
                    if player.task_status == 0:
                        player.task_status = 1
                        player.task_completed -= 1
                        bot.send_message(message.chat.id, "НЕ, АДМИНАМ НЕ НРАВИТСЯ")
    else: bot.send_message(message.chat.id, message.sticker.file_id, reply_to_message_id = message.message_id) #del

@bot.message_handler(content_types=["text"])
def message_parsing(message):
    for w in active_players[:]:
        if w.informed == False:
            if w.task.time:
                if time.time() - w.last_task_time >  w.task.time * 3600:
                    bot.send_message(debug_chat_id, players.to_string(w) + '\nВремя задания истекло! Оцените!')
                    w.informed = True
            if w.task.messages:
                if message.message_id - w.last_task_mssg >  w.task.messages:
                    bot.send_message(debug_chat_id, players.to_string(w) + '\nВсе сообщения написаны! Оцените!')
                    w.informed = True

    if message.text == 'МОЛОДЕЦ!':
        if message.reply_to_message:
            for w in config.root[:]:
                if message.from_user.username == w:
                    player = findplayer(message.reply_to_message.from_user)
                    if player.task_status == 1:
                        player.task_status = 0
                        player.task_completed += 1
                        bot.send_message(message.chat.id, "ЗАДАНИЕ ВЫПОЛНЕНО!\nВСЕГО СДЕЛАНО " + str(player.task_completed) + " ЗАДАНИЙ", reply_to_message_id = message.reply_to_message.message_id)
    elif message.text == 'ТЫ ДУРА?':
        if message.reply_to_message:
            for w in config.root[:]:
                if message.from_user.username == w: 
                    player = findplayer(message.reply_to_message.from_user)
                    if player.task_status == 1:
                        player.task_status = 2
                        bot.send_message(message.chat.id, "ЗАДАНИЕ ПРОВАЛЕНО!", reply_to_message_id = message.reply_to_message.message_id)
                    

if __name__ == '__main__':
    f = open('players.json', 'r')
    active_players[:] = json.load(f, object_hook=obj)
    f.close()
    random.seed()
    bot.polling(none_stop=True)