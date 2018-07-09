# -*- coding: utf-8 -*-
import config
import os
import telebot
import random
import players
import tasks
import time
import json

bot = telebot.TeleBot(str(os.environ['TOKEN']))
active_players = []

vip_chat_id = -1001145739506
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

@bot.message_handler(content_types=["new_chat_member"])                  
def new_member(message):
    if message.new_chat_member.id in config.whitelist:
        bot.send_message(message.chat.id, "ОУРА!", reply_to_message_id = message.message_id)
    else: bot.send_message(message.chat.id, "ОНЕТ!", reply_to_message_id = message.message_id)

@bot.message_handler(content_types=["left_chat_member"])                  
def left_member(message):
    if message.left_chat_member.id in config.whitelist:
        bot.send_message(message.chat.id, "ОНЕТ!", reply_to_message_id = message.message_id)
    else: bot.send_message(message.chat.id, "ОУРА!", reply_to_message_id = message.message_id)

@bot.message_handler(commands=["mess", "MESS"])
def axol_voice(message):
    if message.from_user.username in config.root:
        text = str(message.text[6:])
        if text:
            bot.send_message(vip_chat_id, str(message.text[6:])) #replace with vip_chat_id

@bot.message_handler(commands=["my_task"])
def task_status(message):
    player = findplayer(message.from_user)
    answer = ""
    if player.task_status == 1:
        if player.task:
            answer += player.task.text + "\n"
            if player.task.time:
                tm = player.task.time * 60 - ((time.time() - player.last_task_time)// 60)
                answer += "Осталось времени: " + str('{:.0f}'.format(tm // 60)) + " часов и " + str('{:.0f}'.format(tm % 60)) + " минут\n"
#            if player.task.messages:
#                answer += "Осталось около " + str(player.last_task_mssg + player.task.messages - message.message_id) + " сообщений чата.\n"
    answer += "Всего сделано: " + str(player.task_completed) +".\n"
    tm = config.seconds_in_day // 60 - ((time.time() - player.last_task_time)// 60)
    if tm > 0:
        answer += "До следующего задания: " + str('{:.0f}'.format(tm // 60)) + " часов и " + str('{:.0f}'.format(tm % 60)) + " минут\n"
    bot.send_message(message.chat.id, answer)

#collect players and give them tasks
@bot.message_handler(commands=["get_task"])
def task_send(message):
    if message.chat.id != vip_chat_id and  message.chat.id != debug_chat_id:
        bot.send_message(message.chat.id, "ПО ЛИЧКАМ ШУШУКАЕТЕСЬ? НЕ ТОТ ЧЯТИК!", reply_to_message_id = message.message_id)
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
                bot.send_message(message.chat.id, "НОВОЕ ЗАДАНИЕ БУДЕТ НЕСКОРО!", reply_to_message_id = message.message_id)
            else:
                f = open('players1.json', 'w')
                json.dump(active_players, f, default=jsonDefault)
                f.close()
                player.task_status = 1
                player.last_task_time = time.time()
                player.last_task_mssg = message.message_id
                task = random.choice(config.tasks)
                bot.send_sticker(message.chat.id, task[0])
                bot.send_message(message.chat.id, task[1])
                player.task = tasks.Task(*task)
                player.informed = False

# root command. See all players with tasks.
@bot.message_handler(commands=["all_tasks"])
def all_tasks(message):
    for w in config.root[:]:
        if message.from_user.username == w:
            for x in active_players[:]:
                if x.task and x.task_status == 1:
                    bot.send_message(message.chat.id, players.to_string(x)) 

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, random.choice(config.help_list), reply_to_message_id = message.message_id)

@bot.message_handler(commands=["donate"])
def donate(message):
    bot.send_message(message.chat.id, random.choice(config.donate_list), reply_to_message_id = message.message_id)

@bot.message_handler(commands=["backup"])
def backup(message):
    f = open('players1.json', 'w')
    json.dump(active_players, f, default=jsonDefault)
    f.close()

#CHANGE CHAT IN LEVEL_UP(), NO() AND message_parsing_to_bday_game(message)!!1
level = -1
def level_up():
    global level
    level += 1
    print(level)
    if level <= len(config.questions)-1:
        question = "ДЕРЖИ ЕЩЁ ВОПРОС:\n" + config.questions[level]
        bot.send_message(debug_chat_id, question)
    elif level == len(config.questions):
        bot.send_message(debug_chat_id, "ТЫ ПОДЕБИЛ")

@bot.message_handler(commands=["NEXT", "next"])
def next_level(message):
    if message.from_user.username in config.root:
        level_up()

@bot.message_handler(commands=["no", "NO"])
def send_fuck(message):
    if message.from_user.username in config.root:
        bot.send_sticker(debug_chat_id, random.choice(config.fuck_list))

@bot.message_handler(content_types=["text"])
def message_parsing_to_bday_game(message):
    if message.chat.id == debug_chat_id:
        text = message.text.upper()
        if level < len(config.questions)-1:
            if text == config.answers[level]:
                level_up()

@bot.message_handler(content_types=["sticker"])
def sticker_parsing(message):
    for w in active_players[:]:
        if w.task and not w.informed:
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
    elif message.sticker.file_id == 'CAADAgADZgADhzHUD8vWtQEsl3zaAg':
        bot.send_message(message.chat.id, 'УЛЕЙ')
    if message.chat.id == debug_chat_id: 
        bot.send_message(debug_chat_id, message.sticker.file_id, reply_to_message_id = message.message_id)

@bot.message_handler(content_types=["text"])
def message_parsing(message):
    for w in active_players[:]:
        if w.task and  not w.informed:
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
    if os.path.isfile('players1.json'):
        f = open('players1.json', 'r')
        active_players[:] = json.load(f, object_hook=obj)
        f.close()
    else:
        active_players = []
    random.seed()
    bot.polling(none_stop=True)