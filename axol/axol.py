# -*- coding: utf-8 -*-
import config
import os
import telebot
import random
import players
import time
import json
from requests.exceptions import ReadTimeout
from threading import Timer

bot = telebot.TeleBot(str(os.environ['TOKEN']))
active_players = []

day = 24 * 60 * 60

vip_chat_id = -1001145739506
debug_chat_id = -1001107497089
igroklub_chat = -1001108031278
alukr_chat = -1001031232765
allow_chats = [vip_chat_id, debug_chat_id, -1001149068208, igroklub_chat, alukr_chat]
all_timers = []
current_task_funcs = []


def zrena():
    bot.send_sticker(vip_chat_id, 'CAADAgADtAADP_vRD1iCbwT85WNIAg')
    bot.send_message(vip_chat_id, 'ХАЛЯВНЫЙ ЗАРЯД! ГО ПИЛИТЬ РАНДОМЩИКОВ!')
    timer = Timer(day, zrena)
    timer.start()


def zrena_timers_init():
    cur_time = time.localtime(time.time())
    mins = cur_time.tm_min
    sec = cur_time.tm_sec
    hours = cur_time.tm_hour
    tim = (day + 55 * 60 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena)
    timer.start()
    tim = (day + 30 * 60 + 9 * 3600 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena)
    timer.start()
    tim = (day + 20 * 60 + 20 * 3600 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena)
    timer.start()
    tim = (day + 25 * 60 + 14 * 3600 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena)
    timer.start()


def jsonDefault(object):
    return object.__dict__


# find and append players
def findplayer(user):
    for player in active_players:
        if player.user.id == user.id:
            player.user = user
            return player
    player = players.Player(user)
    active_players.append(player)
    return player


# check_functions
def deep_check(message, player, data):
    # init
    if not data:
        data.append([])
        data.append([])
    if not message.text:
        return
    words = message.text.split()
    for word in words:
        i = len(word)
        for i in range(1, len(word)):
            if not word[i].isalpha() and word[i] != '_' and not word[i].isdigit():
                i -= 1
                break
        if len(word[:i+1]) == 1:
            continue

        if message.from_user.id != player.user.id and word[0] == '/' and word[:i+1] not in data[0]:
            data[0].append(word[:i+1])

        if message.from_user.id == player.user.id and word[0] == '/' and word[:i+1] in data[0] and word[:i+1] not in data[1]:
            data[1].append(word[:i+1])
    if len(data[0]) == len(data[1]) and message.message_id - player.last_task_mssg > 300:
        return "+"


def gdvll_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    glsn = "AEOIUУЫАЕОИЮЭЁ"
    text = message.text.upper()
    for char in glsn:
        if char in text:
            return "-"
    if time.time() - player.last_task_time > 3600 * 3:
        return "+"


def iioo_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    counter = 0
    sglsn = "QWRTPSDFGHJKLZXCVBNMЙЦКНГШЩЗХФВПРЛДЖЧСМТБ"
    text = message.text.upper()
    words = text.split()
    for word in words:
        for char in word:
            if char in sglsn:
                counter += 1
        if counter > 2:
            return "-"
        else:
            counter = 0

    if time.time() - player.last_task_time > 3600 * 3:
        return "+"


def tribbl_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    text = message.text
    if text[-1].isalpha() or text[-1].isdigit():
        return "-"
    words = text.split()
    for word in words:
        for char in word[1:]:
            if char.isupper():
                return "-"


def liira_check(message, player, data):
    if message.from_user.id != 265419583 or not message.text or not message.reply_to_message\
            or not message.reply_to_message.from_user.id != player.user.id:
        return
    if "КРАСИВО" in message.text.upper():
        return "+"


def super_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    counter = True
    for char in message.text:
        if not char.isalpha() and ord(char) > 100:
            counter = False
    if counter:
        return "-"
    if time.time() - player.last_task_time > 3600 * 3:
        return "+"


def bumaga_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text or not message.reply_to_message:
        return
    player = findplayer(message.reply_to_message.from_user)
    if "ПОБЕЖДАЮ" in message.text.upper() and 20 in player.task_id:
        return "+"


def kamen_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text or not message.reply_to_message:
        return
    player = findplayer(message.reply_to_message.from_user)
    if "ПОБЕЖДАЮ" in message.text.upper() and 21 in player.task_id:
        return "+"


def nozhn_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text or not message.reply_to_message:
        return
    player = findplayer(message.reply_to_message.from_user)
    if "ПОБЕЖДАЮ" in message.text.upper() and 19 in player.task_id:
        return "+"


def fylhtq_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    kirill = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    text = message.text.lower()
    for char in kirill:
        if char in text:
            return "-"
    if time.time() - player.last_task_time > 3600 * 3:
        return "+"


def fober_check(message, player, data):
    if not data:
        data.append(0.0)
    if message.from_user.id != player.user.id and message.text and player.user.username and \
            ("@" + player.user.username) in message.text and not data[0]:
        data[0] = [time.time()]
        return
    elif message.from_user.id != player.user.id:
        return
    if not data[0]:
        return
    if message.from_user.id == player.user.id and time.time() - data[0] > 10 * 60:
        return "-"
    else:
        data[0] = 0.0

    if time.time() - player.last_task_time > 3600 * 6:
        return "+"


def mozg_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    for i in range(len(message.text)):
        if message.text[i].isalpha() and message.text[i+1] and message.text[i+1] != ' ':
            return "-"
    if time.time() - player.last_task_time > 3600 * 3:
        return "+"


def malefika_check(message, player, data):
    if message.from_user.id != player.user.id:
        return

    if message.from_user.id == player.user.id and message.text and message.reply_to_message \
       and "ПРЕДСКАЗЫВАЮ" in message.text.upper() and not data:
        enemy = findplayer(message.reply_to_message.from_user)
        data.append(enemy.last_task_mssg)
        data.append(enemy.user)
        data.append(enemy.task_completed)

    if message.from_user.id == player.user.id and data:
        enemy = findplayer(data[1])
        if enemy.last_task_mssg == data[0] and enemy.task_status == 1:
            return
        elif enemy.task_completed == data[2]:
            return "+"
        elif enemy.task_completed > data[2]:
            return "-"


def katissa_check(message, player, data):
    if message.from_user.id == player.user.id:
        return "-"
    if time.time() - player.last_task_time > 3600 * 6:
        return "+"


def patricia_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    words = message.text.split()
    if len(words) < 20:
        return "-"
    if time.time() - player.last_task_time > 3600 * 3:
        return "+"


def all4u_check(message, player, data):
    if not data:
        data.append(0.0)
    if data[0] and time.time() - data[0] > 30 * 60:
        return "+"
    if message.from_user.id == player.user.id:
        data[0] = time.time()
    else:
        data[0] = 0.0


def zoloto_check(message, player, data):
    if message.from_user.id != player.user.id:
        return
    if not message.sticker:
        return "-"
    if time.time() - player.last_task_time > 3600 * 6:
        return "+"

task_funcs = {"deep_check": deep_check, "gdvll_check": gdvll_check, "iioo_check": iioo_check,
              "tribbl_check": tribbl_check, "liira_check": liira_check, "super_check": super_check,
              "bumaga_check": bumaga_check, "kamen_check": kamen_check, "nozhn_check": nozhn_check,
              "fylhtq_check": fylhtq_check, "fober_check": fober_check, "mozg_check": mozg_check,
              "malefika_check": malefika_check, "katissa_check": katissa_check, "patricia_check": patricia_check,
              "all4u_check": all4u_check, "zoloto_check": zoloto_check}


def infinity_check(message, player, data):
    return False


def check_func_costruct(player, func):
    data = []

    def check_func(message, need_result):
        if need_result:
            result = func(message, player, data)
        else:
            result = 0
        return player, result
    return check_func
# check functions

root_log = ""
def logging(message):
    global root_log
    cur_time = time.localtime(time.time())
    root_log += str(cur_time.tm_hour) + ':' + str(cur_time.tm_min) + ' '
    root_log += message.from_user.username + ' сделал '
    if message.text:
        root_log += message.text
    elif message.sticker:
        root_log += message.sticker.file_id
    if message.reply_to_message and message.reply_to_message.from_user.username:
        root_log += ' на ' + message.reply_to_message.from_user.username
    root_log += '\n'


@bot.message_handler(commands=["get_logs"])
def log_output(message):
    global root_log
    if message.from_user.username in config.root and root_log:
        bot.send_message(debug_chat_id, root_log)
        root_log = ""


@bot.message_handler(content_types=["new_chat_member"])
def new_member(message):
    if message.new_chat_member.id in config.whitelist:
        bot.send_message(message.chat.id, "ОУРА!", reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, "ОНЕТ!", reply_to_message_id=message.message_id)


@bot.message_handler(content_types=["left_chat_member"])
def left_member(message):
    try:
        if message.left_chat_member.id in config.whitelist:
            bot.send_message(message.chat.id, "ОНЕТ!", reply_to_message_id=message.message_id)
        elif message.left_chat_member.id == 409875476:
            bot.send_message(message.chat.id, "ОНЕТ! ВЕРНИТЕ В ЧАТИК МОЕГО МНОГОСТРАДАЛЬНОГО БРАТИШКУ КАК ВЫ СМЕЕТЕ "
                                              "НИНАВИЖУ ВАС ПЛАК-ПЛАК :(", reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, "ОУРА!", reply_to_message_id=message.message_id)
    except telebot.apihelper.ApiException:
        bot.send_message(debug_chat_id, "КОГО-ТО КИКНУЛИ, ЕСЛИ ВАМ ЭТО ИНТЕРЕСНО")


@bot.message_handler(commands=["IGRO", "igro"])
def axol_igrovoice(message):
    if message.from_user.username in config.root:
        text = str(message.text[6:])
        if text:
            bot.send_message(igroklub_chat, text)


@bot.message_handler(commands=["mess", "MESS"])
def axol_voice(message):
    if message.from_user.username in config.root:
        text = str(message.text[6:])
        if text:
            bot.send_message(vip_chat_id, text)
            logging(message)


@bot.message_handler(commands=["SAVE", "save"])
def save(message):
    if message.from_user.username in config.root and message.reply_to_message:
        bot.forward_message(debug_chat_id, message.chat.id, message.reply_to_message.message_id)
        logging(message)


@bot.message_handler(commands=["fwd", "FWD"])
def fwd(message):
    if message.from_user.username in config.root and message.reply_to_message:
        bot.forward_message(vip_chat_id, message.chat.id, message.reply_to_message.message_id)
        logging(message)


@bot.message_handler(commands=["clean"])
def clean(message):
    if message.from_user.username in config.root:
        for player in active_players:
            if time.time() - player.last_task_time > config.seconds_in_day * 7:
                player.task_status = 0
                player.task_id = []
                player.task = None


@bot.message_handler(commands=["gnom"])
def gnom(message):
    if message.chat.id == -1001269697180:
        player = findplayer(message.from_user)
        text = str(message.text[6:])
        if '9' in text:
            player.gnome_status = 1
        elif '11' in text:
            player.gnome_status = 2
        elif "ВСЕГДА" in text.upper():
            player.gnome_status = 3
        elif "НЕ" in text.upper():
            player.gnome_status = 0


@bot.message_handler(commands=["gnoms"])
def gnoms(message):
    list9 =[]
    list11 = []
    list911 = []
    list0 = []
    for player in active_players:
        if player.gnome_status == 1:
            list9.append(player)
        elif player.gnome_status == 2:
            list11.append(player)
        elif player.gnome_status == 3:
            list911.append(player)
        elif player.gnome_status == 0:
            list0.append(player)
    answer = "СТОЛ 9\n"
    for player in list9:
        if player.user.first_name:
            answer += str(player.user.first_name) + '\t'
        if player.user.last_name:
            answer += str(player.user.last_name) + '\t'
        if player.user.username:
            answer += '@' + str(player.user.username) + '.\t'
        answer += '\n'
    answer += 'СТОЛ 11\n'
    for player in list11:
        if player.user.first_name:
            answer += str(player.user.first_name) + '\t'
        if player.user.last_name:
            answer += str(player.user.last_name) + '\t'
        if player.user.username:
            answer += '@' + str(player.user.username) + '.\t'
        answer += '\n'
    answer += 'ДВАСТОЛА\n'
    for player in list911:
        if player.user.first_name:
            answer += str(player.user.first_name) + '\t'
        if player.user.last_name:
            answer += str(player.user.last_name) + '\t'
        if player.user.username:
            answer += '@' + str(player.user.username) + '.\t'
        answer += '\n'
    answer += 'АНТИРЕГ\n'
    for player in list0:
        if player.user.first_name:
            answer += str(player.user.first_name) + '\t'
        if player.user.last_name:
            answer += str(player.user.last_name) + '\t'
        if player.user.username:
            answer += '@' + str(player.user.username) + '.\t'
        answer += '\n'
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=["new_gnoms"])
def new_gnoms(message):
    if message.from_user.username == "Deepwarrior":
        for player in active_players:
            player.gnome_status = -1


@bot.message_handler(commands=["long"])
def long_cat(message):
    text = str(message.text[6:])
    if not text:
        return
    try:
        num = int(text)
    except ValueError:
        bot.send_message(message.chat.id, "ТЫ ИЛИ ЦИФЕРКА, ИЛИ ГЛУПЫЙ")
        return

    if num > 15 and not message.from_user.id == config.cifr_chat:
        bot.send_message(message.chat.id, "ТЫ НЕ ЦИФЕРКА!")
        return
    if num > 100:
        bot.send_message(message.chat.id, "1", reply_to_message_id=message.message_id)
        return
    if num < 2:
        bot.send_message(message.chat.id, "ЗАЧЕМ ТЕБЕ КОТ-ИНВАЛИД?")
        return
    bot.send_sticker(message.chat.id, random.choice(config.cats[0]))
    for i in range(1, num - 1):
        bot.send_sticker(message.chat.id, random.choice(config.cats[1]))
    tail = random.choice(config.cats[2])
    bot.send_sticker(message.chat.id, tail)
    if tail == 'CAADAgADeAAD2VJTDNSJtyPtKqeKAg':
        bot.send_sticker(message.chat.id, 'CAADAgADlgIAAmMr4glN9I0DbTqtTgI')


@bot.message_handler(commands=["send_deep"])
def send_deep(message):
    text = str(message.text[10:])
    if not text:
        return
    text = ': ' + text
    if message.from_user.last_name:
        text = message.from_user.last_name + text
    if message.from_user.first_name:
        text = message.from_user.first_name + ' ' + text
    bot.send_message(config.deep_chat, text)


@bot.message_handler(commands=["send_all"])
def send_all(message):
    text = str(message.text[9:])
    if not text or message.from_user.username not in config.root:
        return
    for player in active_players:
        try:
            bot.send_message(player.user.id, text)
        except telebot.apihelper.ApiException:
            continue


@bot.message_handler(commands=["send_uhi"])
def send_uhi(message):
    text = str(message.text[9:])
    if not text:
        return
    text = ': ' + text
    if message.from_user.last_name:
        text = message.from_user.last_name + text
    if message.from_user.first_name:
        text = message.from_user.first_name + ' ' + text
    bot.send_message(config.citrus_chat, text)


@bot.message_handler(commands=["send"])
def send(message):
    text = str(message.text[6:])
    if not text or text == "rakon_bot":
        bot.send_message(message.chat.id, "НЕТ, НЕТ, НУЖНО ПИСАТЬ ПИСЬМО ПРОВЕРЯТОРАМ В ТОМ ЖЕ СООБЩЕНИИ, ЧТО И /send")
        return
    text = ': ' + text
    if message.from_user.last_name:
        text = message.from_user.last_name + text
    if message.from_user.first_name:
        text = message.from_user.first_name + ' ' + text
    try:
        bot.send_message(-1001246951967, text)
    except telebot.apihelper.ApiException:
        bot.send_message(debug_chat_id, text)


@bot.message_handler(commands=["on"])
def messages_on(message):
    if message.from_user.id == message.chat.id:
        player = findplayer(message.from_user)
        player.mess_sended = False
        player.mess_from_bot = True
        bot.send_message(message.chat.id, "ПОЛУЧИЛОСЬ")


@bot.message_handler(commands=["off"])
def messages_off(message):
    if message.from_user.id == message.chat.id:
        player = findplayer(message.from_user)
        player.mess_from_bot = False
        bot.send_message(message.chat.id, "ВЕРНИ КАК БЫЛО")


@bot.message_handler(commands=["femka", "FEMKA"])
def femka(message):
    text = str(message.text[7:])
    text = text.upper()
    if not text or text == "rakon_bot":
        bot.send_message(message.chat.id, "ЭАЛЛО, СЛОВО-ТО НАПИШИ")
        return
    if " " in text:
        bot.send_message(message.chat.id, "Я ЧО, ПОХОЖ НА ПАТРИСИЮ? НАПИШИ ОДНО СЛОВО!")
        return
    if not text.isalpha():
        bot.send_message(message.chat.id, "ПРИВЕТ, ЦИФЕРКА! 0/")
        return

    last_char = text[-1]  # You can do switch by value of this variable.
    if last_char in "ИЫ" and text not in config.exception_spisok:
        the_end = config.ends[:]
    else:
        the_end = config.end[:]

    if last_char in "АЯ":
        bot.send_message(message.chat.id, "СЛОВО «" + text + "» ИДЕАЛЬНО!")
    else:
        text = text[:-1]
        for i in range(len(config.ends)):
            if last_char in "ИЫ" and text + last_char not in config.exception_spisok:
                # for i in range(len(config.ends)) and not in [0, 2, 5]:
                #    the_end[i] = last_char + the_end[i]
                if not(i == 0 or i == 2 or i == 5):
                    the_end[i] = last_char + the_end[i]
            else:
                if last_char in "КГ":
                    if i == 1:
                        the_end[i] = "ЧКА"
                    else:
                        the_end[i] = last_char + the_end[i]

                elif last_char in "ОЕУ" or text + last_char in config.exception_spisok:
                    if not (i == 0 or i == 2 or i == 5):
                        the_end[i] = last_char + the_end[i]

                elif last_char == "Ь":
                    if not (i == 2 or i == 4 or i == 5):
                        the_end[i] = last_char + the_end[i]
                else:
                    the_end[i] = last_char + the_end[i]

        ideal_spisok = "ДЕРЖИ ИДЕАЛЬНЫЕ СЛОВА:" + '\n' * 2
        for i in the_end:
            ideal_spisok += text + i.upper() + '\n'
        bot.send_message(message.chat.id, ideal_spisok)


@bot.message_handler(commands=["love_reg"])
def love_reg(message):
    if message.from_user.id == message.chat.id:
        player = findplayer(message.from_user)
        player.islove = True
        bot.send_message(message.chat.id, "СПАСИБО ЗА РЕГИСТРАЦИЮ, КОТИК \u2764 \u2764 \u2764")

@bot.message_handler(commands=["love_send"])
def love_send(message):
    text = str(message.text[11:])
    if not message.from_user.id == message.chat.id:
        return
    if not text or text == "rakon_bot":
        bot.send_message(message.chat.id, "НЕ СТЕСНЯЙСЯ, ВЫРАЗИ СВОИ ЧУВСТВА!")
        return
    text = "#валентинка" + "\n" + text
    try:
        bot.send_message(vip_chat_id, text)
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, "НЕ ВЫШЛО ОТПРАВИТЬ СООБЩЕНИЕ :(")

@bot.message_handler(commands=["love_set"])
def love_set(message):
    players_in_love = []
    for player in active_players:
        if player.islove:
            try:
                status = bot.get_chat_member(vip_chat_id, player.user.id)
            except telebot.apihelper.ApiException:
                continue
            if status and status.status in ["member", "creator", "administrator"] and not player.user.username == "rakon_bot":
                players_in_love.append(player)
    random.shuffle(players_in_love)
    lovers = len(players_in_love)
    for i in range(lovers):
        player = players_in_love[i]
        pair = players_in_love[(i+1) % lovers]
        player.pair = ""
        if player.user.first_name:
            player.pair += str(pair.user.first_name) + '\t'
        if player.user.last_name:
            player.pair += str(pair.user.last_name) + '\t'
        if player.user.username:
            player.pair += '@' + str(pair.user.username) + '\t'
        player.love_task = random.choice(config.love_tasks)
        try:
            bot.send_message(player.user.id, 'АКСОЛОТЛЬ-КУПИДОН НАУДАЧУ ЗАПУСТИЛ'
                                            ' СВОЮ СТРЕЛУ. ТВОЯ ВТОРАЯ ПОЛОВИНКА '
                                      + player.pair + ' УЖЕ ЖДЁТ ОТ ТЕБЯ ЗНАКА ВНИМАНИЯ!')
            bot.send_sticker(player.user.id, 'CAADAgADUgADsjRGHr5CgRYMzRQNAg')
            bot.send_message(player.user.id, player.love_task + ' \u2764 \u2764 \u2764')
        except telebot.apihelper.ApiException:
            continue

@bot.message_handler(commands=["love"])
def love(message):
    answer = "LOVE IS EVERYWHERE: \n"
    if message.from_user.username in config.root:
        for player in active_players:
            if player.islove:
                try:
                    status = bot.get_chat_member(vip_chat_id, player.user.id)
                except telebot.apihelper.ApiException:
                    continue
                if status and status.status in ["member", "creator",
                                            "administrator"] and not player.user.username == "rakon_bot":
                    if player.user.first_name:
                        answer += str(player.user.first_name) + '\t'
                    if player.user.last_name:
                        answer += str(player.user.last_name) + '\t'
                    if player.user.username:
                        answer += '@' + str(player.user.username) + '.\t'
                    answer += '\n'
        bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=["love_all"])
def love_all(message):
    if message.from_user.id == message.chat.id and message.from_user.username in config.root:
        list = ""
        for player in active_players:
            if player.islove:
                try:
                    status = bot.get_chat_member(vip_chat_id, player.user.id)
                except telebot.apihelper.ApiException:
                    continue
                if status and status.status in ["member", "creator",
                                            "administrator"] and not player.user.username == "rakon_bot":
                    if player.user.first_name:
                        list += str(player.user.first_name) + '\t'
                    if player.user.last_name:
                        list += str(player.user.last_name) + '\t'
                    if player.user.username:
                        list += '@' + str(player.user.username) + '\t'
                    list += "И ПОЛОВИНКА " + player.pair + '\t'
                    list += "С ЗАДАНИЕМ "
                    list += player.love_task + '.\t'
                    list += '\n'*2
        bot.send_message(message.chat.id, list)

@bot.message_handler(commands=["new_year"])
def new_year_reg(message):
    if message.from_user.id == message.chat.id:
        player = findplayer(message.from_user)
        player.new_year = True
        bot.send_message(message.chat.id, "ТЕПЕРЬ ЖДИ НОВОГОДНЕЕ ЗАДАНИЕ")


@bot.message_handler(commands=["ng"])
def new_year_reg_get(message):
    answer = "СПИСОК ТЕХ, КТО ГОТОВ ПРОВЕСТИ ОСТАТОК СТАРОГО ГОДА В МУЧЕНИЯХ: \n"
    if message.from_user.username in config.root:
        for player in active_players:
            if player.new_year:
                if player.user.first_name:
                    answer += str(player.user.first_name) + '\t'
                if player.user.last_name:
                    answer += str(player.user.last_name) + '\t'
                if player.user.username:
                    answer += '@' + str(player.user.username) + '.\t'
                answer += '\n'
        bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=["panteon"])
def panteon(message):
    answer = ""
    top = []
    for i in range(1, 10):
        max_tasks = 0
        for player in active_players:
            if player not in top and player.task_completed % 50 >= max_tasks:
                max_tasks = player.task_completed % 50
        for player in active_players:
            if player not in top and player.task_completed % 50 == max_tasks:
                answer += str(i) + '.\t'
                if player.user.first_name:
                    answer += '<b>' + str(player.user.first_name) + '</b>' + '\t'
                if player.user.last_name:
                    answer += '<b>' + str(player.user.last_name) + '</b>' + '\t'
                if player.user.username:
                    answer += '@' + str(player.user.username) + '.\t'
                answer += 'Сделано:' + str(max_tasks) + '\n'
                top.append(player)
                break
    bot.send_message(message.chat.id, answer, parse_mode="HTML")


@bot.message_handler(commands=["top_pozora"])
def pozor(message):
    text = "ТОП ПОЗОРА: \n"
    i = 1

    for player in active_players:
        if time.time() - player.last_task_time > 3600 * 500:
            try:
                user = bot.get_chat_member(message.chat.id, player.user.id)
            except telebot.apihelper.ApiException:
                continue
            if user and user.status in ["member", "creator", "administrator"] and not user.user.username == "rakon_bot"\
                    and not user.user.username == "uhi_official":
                text += str(i) + '. '
                if user.user.first_name:
                    text += '<b>' + str(user.user.first_name) + '</b>' + ' '
                if user.user.last_name:
                    text += '<b>' + str(user.user.last_name) + '</b>' + ' '
                if user.user.username:
                    text += '@' + str(user.user.username) + '.\t'
                text += '\n'
                i += 1
    bot.send_message(message.chat.id, text, parse_mode="HTML")


@bot.message_handler(commands=["top_sarastie"])
def sarasti(message):
    text = "ТОП САРАСТИ:\n-1. АРУЛУТ\n1. САРАСТИ\n2.САРАСТИШЕЧКА\n3. РАСТИШИШКА\n4. s a r A S I S k a\n5. СИСЕНИКА\n" \
           "6. САРАСТАТАЛО"
    try:
        bot.send_voice(message.chat.id, 'AwADAgAD0QADNxYpSFb3d6KS2tHAAg', caption=text)
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["my_task"])
def task_status(message):
    player = findplayer(message.from_user)
    answer = ""
    tm = 0
    if player.task_completed < 100:
        tasks = config.tasks
    else:
        tasks = config.black_tasks
    if player.task_status == 1:
        if player.task_completed % 100 < 40:
            if hasattr(player, "task_id") and len(player.task_id):
                answer += tasks[player.task_id[0]][1] + "\n"
            elif player.task:
                answer += player.task.text + "\n"
        else:
            answer += ")))\n"
        if hasattr(player, "task_id") and len(player.task_id):
            for idx in player.task_id:
                task = tasks[idx]
                if (task[2] * 60 - ((time.time() - player.last_task_time) // 60)) > tm:
                    tm = task[2] * 60 - ((time.time() - player.last_task_time) // 60)
        elif player.task and player.task.time:
            tm = player.task.time * 60 - ((time.time() - player.last_task_time) // 60)
        if tm > 0:
            answer += "Осталось времени: " + str('{:.0f}'.format(tm // 60)) + " часов и " + \
                      str('{:.0f}'.format(tm % 60)) + " минут\n"
        else:
            answer += "ВЫПОЛНЯЙ, ПОКА НЕ ЗАСЧИТАЮТ!\n"
    answer += "Всего сделано: " + str(player.task_completed % 50) + ".\n"
    tm = config.seconds_in_day // 60 - ((time.time() - player.last_task_time) // 60)
    if tm > 0:
        tm += 1  # 1 min more
        answer += "До следующего задания: " + str('{:.0f}'.format(tm // 60)) + " часов и " + \
                  str('{:.0f}'.format(tm % 60)) + " минут\n"
    try:
        bot.send_message(message.chat.id, answer, reply_to_message_id=player.last_task_mssg)
    except telebot.apihelper.ApiException:
        try:
            bot.send_message(message.chat.id, answer)
        except telebot.apihelper.ApiException:
            print("my_task failed")


def remove_task_check(user, message):
    for func in current_task_funcs:
        player, result = func(message, False)
        if player == user:
            current_task_funcs.remove(func)


# collect players and give them tasks
@bot.message_handler(commands=["get_task"])
def get_task(message):
    if message.chat.id not in allow_chats:
        bot.send_message(message.chat.id, "ПО ЛИЧКАМ ШУШУКАЕТЕСЬ? НЕ ТОТ ЧЯТИК!",
                         reply_to_message_id=message.message_id)
    else:
        player = findplayer(message.from_user)
        if time.time() - player.last_task_time > config.seconds_in_day:
            player.task_status = 0
            player.task_id = []
            player.task = None
            remove_task_check(player, message)
        if player.task_status == 1:
            bot.send_message(message.chat.id, "ТЫ УЖЕ ЧТО-ТО ДЕЛАЕШЬ!", reply_to_message_id=message.message_id)
        elif player.task_status == 2:
            bot.send_message(message.chat.id, "ТЫ УЖЕ НЕ СМОГ!", reply_to_message_id=message.message_id)
        elif player.task_status == 0:
            if time.time() - player.last_task_time < config.seconds_in_day:
                bot.send_message(message.chat.id, "НОВОЕ ЗАДАНИЕ БУДЕТ НЕСКОРО!",
                                 reply_to_message_id=message.message_id)

            else:
                if player.task_completed < 100:
                    tasks = config.tasks
                else:
                    tasks = config.black_tasks
                player.task_status = 1
                player.last_task_time = time.time()
                player.last_task_mssg = message.message_id
                player.message = message

                rand = random.randint(1, 500)
                if rand == 237 and player.task_completed < 100:
                    task = ['CAADAgADaQADP_vRD78igQttLbufAg', 'КОЛДУЮ, КОЛДУЮ... ВЖУХ! И ТЫ ПИДОР ДНЯ.', 0, 0]
                    bot.send_sticker(message.chat.id, task[0])
                    bot.send_message(message.chat.id, task[1])
                else:
                    rand = random.randint(0, len(tasks) - 1)
                    task = tasks[rand]
                    player.task_id.append(rand)
                    bot.send_sticker(message.chat.id, task[0])
                    if player.task_completed % 100 < 40:
                        bot.send_message(message.chat.id, task[1])
                    else:
                        text = random.choice(["ТЫ УЖЕ БОЛЬШОЙ, САМ РАЗБЕРЕШЬСЯ", "<СПОЙЛЕРЫ>", "Я ПОЗАБЫЛ ВСЕ СЛОВА",
                                              "ЗДЕСЬ БЫЛО ЧТО-ТО ДЛИННОЕ ЕЩЁ"])
                        bot.send_message(message.chat.id, text)
                    player.informed = False
                    player.mess_sended = False

                    if 99 >= player.task_completed >= 70 or player.task_completed >= 150:
                        bot.send_message(message.chat.id, "А ВОТ ЕЩЁ ТЕБЕ...")
                        if player.task_completed >= 150:
                            tasks = config.tasks
                        rand = random.randint(0, len(tasks) - 1)
                        bot.send_sticker(message.chat.id, tasks[rand][0])
                        player.task_id.append(rand)
                    if player.task_completed % 100 == 99:
                        rand = random.randint(0, len(tasks) - 1)
                        bot.send_sticker(message.chat.id, tasks[rand][0])
                        player.task_id.append(rand)
                        rand = random.randint(0, len(tasks) - 1)
                        bot.send_sticker(message.chat.id, tasks[rand][0])
                        player.task_id.append(rand)
                        bot.send_message(message.chat.id, "АЗАЗА, УДАЧИ")

                    backup(None)

                    for task_id in player.task_id:
                        if len(tasks[task_id]) > 4:
                            current_task_funcs.append(check_func_costruct(player, task_funcs[tasks[task_id][4]]))
                        else:
                            current_task_funcs.append(check_func_costruct(player, infinity_check))


# root command. See all players with tasks.
@bot.message_handler(commands=["all_tasks"])
def all_tasks(message):
    if message.from_user.username in config.root:
        for player in active_players:
            if (player.task or (hasattr(player, "task_id") and len(player.task_id))) and player.task_status == 1:
                bot.send_message(message.chat.id, players.to_string(player))
        logging(message)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, random.choice(config.help_list), reply_to_message_id=message.message_id)


@bot.message_handler(commands=["donate"])
def donate(message):
    bot.send_message(message.chat.id, random.choice(config.donate_list), reply_to_message_id=message.message_id)


@bot.message_handler(commands=["backup"])
def backup(message):
    file = open('players.json', 'w')
    json.dump(active_players, file, default=jsonDefault, indent=2)
    file.close()


def react(reaction, message):
    if message.from_user.id == message.chat.id:
        return
    rand = random.randint(1, len(reaction[3]) + len(reaction[4]))
    if rand > len(reaction[3]):
        rand -= len(reaction[3])
        bot.send_sticker(message.chat.id, reaction[4][rand - 1], reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, reaction[3][rand - 1], reply_to_message_id=message.message_id)


def task_rework(reaction, message):
    if message.from_user.username in config.root and message.reply_to_message:
        player = findplayer(message.reply_to_message.from_user)
        if player.task or hasattr(player, "task_id") and len(player.task_id):
            if player.task_status == 0:
                player.task_status = 1
                player.task_completed -= 1
                bot.send_message(message.chat.id, "НЕ, АДМИНАМ НЕ НРАВИТСЯ")

                if player.task_completed < 100:
                    tasks = config.tasks
                else:
                    tasks = config.black_tasks
                for task_id in player.task_id:
                    if len(tasks[task_id]) > 4:
                        current_task_funcs.append(check_func_costruct(player, task_funcs[tasks[task_id][4]]))
                    else:
                        current_task_funcs.append(check_func_costruct(player, infinity_check))
        logging(message)


def task_fail(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        if player.task_status == 1:
            player.task_status = 2
            remove_task_check(player, message)
            bot.send_message(message.chat.id, "ЗАДАНИЕ ПРОВАЛЕНО!",
                             reply_to_message_id=message.reply_to_message.message_id)
            if player.mess_from_bot:
                bot.send_message(player.user.id, "К СОЖАЛЕНИЮ, ЗАДАНИЕ ПРОВАЛЕНО.")
        logging(message)


def task_complete(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        logging(message)
        player = findplayer(message.reply_to_message.from_user)
        if player.task_status == 1:
            player.task_status = 0
            remove_task_check(player, message)
            player.task_completed += 1
            if player.task_completed == 50:
                bot.send_message(player.user.id, "АЗАЗА, ТЫ УМИР")
            elif player.task_completed == 100:
                bot.send_message(player.user.id, "СГОРИ ДОТЛА! КАК И ВСЕ ТВОИ ОЧКИ")
            elif player.task_completed == 150:
                bot.send_message(player.user.id, "УРА УРА СУИЦИД")
            if player.task_completed % 50 == 0:
                bot.send_message(message.chat.id, "ЗАДАНИЕ ВЫПОЛНЕНО!\nВСЕГО СДЕЛАНО 50 ЗАДАНИЙ!",
                                 reply_to_message_id=message.reply_to_message.message_id)
                time.sleep(3)
                bot.send_message(message.chat.id, "ХОТЯЯЯЯ...")
                time.sleep(1)
                mess = "АНТИКЛАЦ!\n"
                for player in range(49):
                    mess += "АНТИКЛАЦ!\n"
                bot.send_message(message.chat.id, mess)
                return
            bot.send_message(message.chat.id, "ЗАДАНИЕ ВЫПОЛНЕНО!\nВСЕГО СДЕЛАНО " + str(player.task_completed % 50) +
                             " ЗАДАНИЙ", reply_to_message_id=message.reply_to_message.message_id)

            if player.mess_from_bot:
                bot.send_message(player.user.id, "ХЭЭЭЙ! ТЕБЕ ЗАСЧИТАЛИ!")
            if player.task_completed % 50 == 20:
                stick = random.choice(config.bonus_20)
                bot.send_message(player.user.id, "ПОЗДРАВЛЯЮ! \n МНОГО ЗАДАНИЙ УЖЕ СДЕЛАНО, НО МНОГО БУДЕТ И ВПЕРЕДИ \n"
                                                 "А ПОКА ТЫ ВЫИГРАЛ СЕКРЕТНЫЙ ДУРНИРНЫЙ СТИКЕР, ИСПОЛЬЗУЙ ЕГО С УМОМ")
                bot.send_sticker(player.user.id, stick)
            if player.task_completed == 60:
                bot.send_message(message.chat.id, "ТЕБЯ ВЕДЬ УЖЕ ОБНУЛИЛИ... ЗАЧЕМ ТЫ ПРОДОЛЖАЕШЬ ИХ ДЕЛАТЬ?")


def message_above(reaction, message):
    i = 1
    while i > 0:
        try:
            if message.reply_to_message:
                k = random.randint(0, len(config.mssg_bv) - 1)
                bot.send_message(message.chat.id, config.mssg_bv[k], reply_to_message_id=message.reply_to_message.message_id - i)
                break
        except telebot.apihelper.ApiException:
            i += 1

secret_santa = [336595041]
sherif = [347438021]


@bot.message_handler(commands=["send_ng_tasks"])
def send_ng_tasks(message):
    if message.from_user.id == message.chat.id and message.from_user.username in config.root:
        for player in active_players:
            if player.new_year and player.user.id not in secret_santa and player.user.id not in sherif:
                try:
                    n = random.randint(0, len(config.ng_tasks) - 1)
                    task = config.ng_tasks[n]
                    player.ng_task_id = n
                    bot.send_sticker(player.user.id, 'CAADAgADJQADsjRGHuRrNOA7RLqJAg')
                    bot.send_message(player.user.id, task)
                except telebot.apihelper.ApiException:
                    continue
            elif player.user.id in secret_santa:
                try:
                    player.ng_task_id = -1
                    bot.send_sticker(player.user.id, 'CAADAgADJQADsjRGHuRrNOA7RLqJAg')
                    bot.send_message(player.user.id, "ТЫ ТАЙНЫЙ САНТА. ПОБЕДИШЬ, ЕСЛИ НИКТО НЕ ОТГАДАЕТ ТВОЮ РОЛЬ ДО "
                                                     "НОВОГО ГОДА.")
                except telebot.apihelper.ApiException:
                    continue
            elif player.user.id in sherif:
                try:
                    player.ng_task_id = -2
                    bot.send_sticker(player.user.id, 'CAADAgADJQADsjRGHuRrNOA7RLqJAg')
                    bot.send_message(player.user.id,
                                     "ТЫ ОЛЕНЬ. КТО-ТО ИЗ ВЗЯВШИХ НОВОГОДНЕЕ ЗАДАНИЕ - ТАЙНЫЙ САНТА. ТВОЯ "
                                     "ЗАДАЧА - ЕГО ОТЫСКАТЬ. У ТЕБЯ ОДНА ПОПЫТКА. ОТВЕТ ПРИСЫЛАТЬ ЧЕРЕЗ В "
                                     "ЛИЧКУ @Deepwarrior ИЛИ @Uhi_Official.")
                except telebot.apihelper.ApiException:
                    continue


@bot.message_handler(commands=["all_ng"])
def all_ng_tasks(message):
    if message.from_user.id == message.chat.id and message.from_user.username in config.root:
        spisok = ""
        for player in active_players:
            if player.new_year:
                if player.user.first_name:
                    spisok += str(player.user.first_name) + '\t'
                if player.user.last_name:
                    spisok += str(player.user.last_name) + '\t'
                if player.user.username:
                    spisok += '@' + str(player.user.username) + '.\t'
                if player.user.id not in secret_santa and player.user.id not in sherif:
                    spisok += config.ng_tasks[player.ng_task_id]
                elif player.user.id in secret_santa:
                    spisok += "ТАЙНЫЙ САНТА"
                elif player.user.id in sherif:
                    spisok += "ШЕРИФ"
                spisok += '\n'
        bot.send_message(message.chat.id, spisok)


def task_extra(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        logging(message)
        player = findplayer(message.reply_to_message.from_user)
        player.task_completed += 1
        bot.send_message(message.chat.id, "ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ ВЫПОЛНЕНО!",
                         reply_to_message_id=message.reply_to_message.message_id)
        if player.task_completed % 50 == 20:
            stick = random.choice(config.bonus_20)
            bot.send_message(player.user.id, "ПОЗДРАВЛЯЮ! \n МНОГО ЗАДАНИЙ УЖЕ СДЕЛАНО, НО МНОГО БУДЕТ И ВПЕРЕДИ \n "
                                             "А ПОКА ТЫ ВЫИГРАЛ СЕКРЕТНЫЙ ДУРНИРНЫЙ СТИКЕР, ИСПОЛЬЗУЙ ЕГО С УМОМ")
            bot.send_sticker(player.user.id, stick)


def anti_task(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        logging(message)
        player = findplayer(message.reply_to_message.from_user)
        player.task_completed -= 1
        bot.send_message(message.chat.id, "ОТМЕНА, ОТМЕНА!", reply_to_message_id=message.reply_to_message.message_id)


def drig(arg):
    bot.send_message(arg, "ДРЫГАЙТЕ, ЧЕРТИ!")


def vbuena(arg):
    bot.send_sticker(arg, 'CAADAgADJwADP_vRD_M5_IJz9qzxAg')
    timer = Timer(60, drig, [arg])
    timer.start()
    all_timers.append(timer)


def natalka(reaction, message):
    cur_time = time.localtime(time.time())
    minutes = cur_time.tm_min
    seconds = cur_time.tm_sec
    rand = random.randint(0, 4)
    if rand:
        bot.send_sticker(message.chat.id, config.numbers[((minutes + rand + 1) % 60) // 10],
                         reply_to_message_id=message.message_id)
        bot.send_sticker(message.chat.id, config.numbers[((minutes + rand + 1) % 60) % 10],
                         reply_to_message_id=message.message_id)

        timer = Timer(60 * rand - seconds, vbuena, [message.chat.id])
        timer.start()
        all_timers.append(timer)
    else:
        react(reaction, message)


def kick_bots(reaction, message):
    targets = [208343353, 88135026, 280982408, 200164142, 226543640, 121913006, 199378994, 110193686, 346903988,
               29664231, 135069175]
    for target in targets:
        try:
            bot.kick_chat_member(message.chat.id, target)
            time.sleep(2)
        except telebot.apihelper.ApiException:
            time.sleep(1)


def kick_lyuds(reaction, message):
    try:
        bot.restrict_chat_member(message.chat.id, message.from_user.id, 2 * 60 * 60, False, False, False, False)
    except telebot.apihelper.ApiException:
        time.sleep(1)


def mem_react(reaction, message):
    rand = random.randint(0, 10)
    if rand < 10:
        bot.send_message(message.chat.id, 'МУМЫРИ!', reply_to_message_id=message.message_id)
    else:
        react(reaction, message)


def set_admin(reaction, message):
    if message.from_user.username in config.root:
        try:
            bot.promote_chat_member(message.chat.id, message.from_user.id,
                                    True, False, False, True, True, True, True, True)
            bot.send_message(message.chat.id, 'ЗВЕЗДА У НОГ ТВОИХ!', reply_to_message_id=message.message_id)
            logging(message)
        except telebot.apihelper.ApiException:
            time.sleep(1)


def whois(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        if (player.task or (hasattr(player, "task_id") and len(player.task_id))) and player.task_status == 1:
            bot.send_message(message.chat.id, players.to_string(player))
        else:
            bot.send_message(message.chat.id, "ТЫ НИКТО, АЗАЗА")


def stop_natalka(reaction, message):
    for timer in all_timers:
        timer.cancel()


def kick_citrus(reaction, message):
    try:
        time.sleep(7)
        bot.kick_chat_member(message.chat.id, config.citrus_chat)
        bot.unban_chat_member(message.chat.id, config.citrus_chat)
        bot.send_sticker(message.chat.id, 'CAADAgADGQADsjRGHmj0-DDbQgexAg')
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, "ТЫ НА КОГО ПАСТЬ ОТКРЫВАЕШЬ, СОБАКА ТРУСЛИВАЯ?!")


def kick_rels(reaction, message):
    try:
        bot.kick_chat_member(message.chat.id, config.rels_chat)
        bot.unban_chat_member(message.chat.id, config.rels_chat)
    except telebot.apihelper.ApiException:
        time.sleep(1)


def kick_misha(reaction, message):
    try:
        bot.kick_chat_member(message.chat.id, config.misha_chat)
        bot.unban_chat_member(message.chat.id, config.misha_chat)
        bot.send_message(message.chat.id, "МNША ЗАПРЕЩЁН И РЕКРАЩЁН.")
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, "ДА КАК ТЫ СМЕЕШЬ ТАК С МАТЕРЬЮ РАЗГОВАРИВАТЬ?!")


reaction_funcs = {"task_rework": task_rework, "task_fail": task_fail, "task_complete": task_complete,
                  "task_extra": task_extra, "natalka": natalka, "kick_bots": kick_bots, "kick_lyuds": kick_lyuds,
                  "mem_react": mem_react, "anti_task": anti_task, "set_admin": set_admin, "whois": whois,
                  "stop_natalka": stop_natalka, "kick_citrus": kick_citrus, "kick_rels": kick_rels,
                  "kick_misha": kick_misha, "message_above": message_above}


def notify(message):
    for player in active_players:
        if player.mess_from_bot and not player.mess_sended \
                and time.time() - player.last_task_time > config.seconds_in_day:
            try:
                bot.send_message(player.user.id, "МОЖНО ВЗЯТЬ И СДЕЛАТЬ НОВОЕ ЗАДАНИЕ!")
            except telebot.apihelper.ApiException:
                player.mess_from_bot = False
                print("notify failed.")
            finally:
                player.mess_sended = True


def task_check(message):
    # return #remove this
    if message.chat.id not in [vip_chat_id]:
        return
    for func in current_task_funcs:
        player, result = func(message, True)
        if result == "+":
            current_task_funcs.remove(func)
            other_tasks = False
            for func in current_task_funcs:
                task_owner, result = func(message, False)
                if task_owner == player:
                    other_tasks = True
            if not other_tasks:
                try:
                    bot.send_message(message.chat.id, "ТЕСТОВЫЙ АВТОЗАЧЁТ!", reply_to_message_id=player.last_task_mssg)
                except telebot.apihelper.ApiException:
                    bot.send_message(message.chat.id, "ТЕСТОВЫЙ АВТОЗАЧЁТ!")
        elif result == "-":
            try:
                bot.send_message(message.chat.id, "ТЕСТОВЫЙ АВТОБАЯЗИД!", reply_to_message_id=player.last_task_mssg)
            except telebot.apihelper.ApiException:
                bot.send_message(message.chat.id, "ТЕСТОВЫЙ АВТОБАЯЗИД!")
            current_task_funcs.remove(func)
            remove_task_check(player, message)


@bot.message_handler(content_types=["sticker"])
def sticker_parsing(message):
    notify(message)
    for reaction in config.reactions:
        if not reaction[2] or message.from_user.id == reaction[2]:
            if message.sticker.file_id in reaction[1]:
                if len(reaction) > 5:
                    reaction_funcs[reaction[5]](reaction, message)
                else:
                    react(reaction, message)
    if message.chat.id == debug_chat_id or message.chat.id == config.cifr_chat:
        bot.send_message(message.chat.id, '\'' + message.sticker.file_id + '\'', reply_to_message_id=message.message_id)
    task_check(message)


@bot.message_handler(content_types=["text"])
def message_parsing(message):
    notify(message)
    for reaction in config.reactions:
        if not reaction[2] or message.from_user.id == reaction[2]:
            if message.text.upper() in reaction[0]:
                if len(reaction) > 5:
                    reaction_funcs[reaction[5]](reaction, message)
                else:
                    react(reaction, message)
    task_check(message)


@bot.message_handler(content_types=["voice"])
def voice_parsing(message):
    if message.chat.id == debug_chat_id:
        bot.send_message(message.chat.id, '\'' + message.voice.file_id + '\'', reply_to_message_id=message.message_id)


if __name__ == '__main__':
    f = open('players.json', 'r')
    templist = json.load(f)
    for x in templist:
        active_players.append(players.Player(**x))
    f.close()
    zrena_timers_init()
    random.seed()

    # bot.send_message(debug_chat_id, '*CAADAgADMgADsj* _RGHiKRfQaAeEsnAg_', parse_mode="Markdown")
    for chat in allow_chats:
        try:
            # bot.send_sticker(chat, 'CAADAgADhQADP_vRD-Do6Qz0fkeMAg')
            print('1')
        except telebot.apihelper.ApiException:
            continue
    while True:
        try:
            bot.polling(none_stop=True)
        except ReadTimeout:
            print("die?")
            time.sleep(60)
            if root_log:
                bot.send_message(debug_chat_id, root_log)
        finally:
            backup(None)
