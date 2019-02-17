# -*- coding: utf-8 -*-
import config
import os
import telebot
import random
import players
import time
import json
import socket
import urllib3
from requests.exceptions import ReadTimeout
from threading import Timer
import operator
import math
import chat_utils
import types
from femka import femka_init
from zrena import zrena_timers_init
from mail import mail_init


def sxor(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

bot = telebot.TeleBot(str(os.environ['TOKEN']))
bot.send_stickers = types.MethodType(chat_utils.send_stickers, bot)
opentoken = sxor(str(os.environ['TOKEN']), '\x00\x06\x08\n\x01\r\x0c\x0e\x04\x00\x00\x00\x0fA?\x0fDv"5!g\x1f\x18\x16\x05\x0cl\x1c\x12Z&\x13\x1d~!/$0\x008\x03<::'
)
rrena_bot = telebot.TeleBot(opentoken)

femka_init(bot)
zrena_timers_init(bot)
zrena_timers_init(rrena_bot)
mail_init(bot)

active_players = []

vip_chat_id = -1001145739506
debug_chat_id = -1001107497089
igroklub_chat = -1001108031278
alukr_chat = -1001031232765
tipa_tri_skobki_chat = -1001246951967
bitva_magov_chat = -1001272922314
chto_chat = -1001479011046
allow_chats = [vip_chat_id, debug_chat_id, -1001149068208, igroklub_chat, alukr_chat, chto_chat]
all_timers = []
current_task_funcs = []
dura_chat = [bitva_magov_chat]
fur_fur_fur_chat = -1001132289884
dlan_chat = -1001172376896
spy_chat = -1001231436175

last_mess = 0

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

        if message.from_user.id != player.user.id and word[0] == '/' \
                and word[:i+1] not in data[0]:
            data[0].append(word[:i+1])

        if message.from_user.id == player.user.id and word[0] == '/' \
                and word[:i+1] in data[0] and word[:i+1] not in data[1]:
            data[1].append(word[:i+1])
    if len(data[0]) == len(data[1]) and \
        message.message_id - player.taskset.get_task_mess() > 300:
        return "+"


def gdvll_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    glsn = "AEOIUУЫАЕОИЮЭЁ"
    text = message.text.upper()
    for char in glsn:
        if char in text:
            return "-"
    if player.taskset.get_task_duration() > 3600 * 3:
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

    if player.taskset.get_task_duration() > 3600 * 3:
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
    if player.taskset.get_task_duration() > 3600 * 3:
        return "+"


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
    if player.taskset.get_task_duration() > 3600 * 3:
        return "+"


def bumaga_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text or not message.reply_to_message:
        return
    player = findplayer(message.reply_to_message.from_user)
    if "ПОБЕЖДАЮ" in message.text.upper():
        for task in player.taskset.tasks:
            if 20 == task.id and task.type == 'normal':
                return "+"


def kamen_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text or not message.reply_to_message:
        return
    player = findplayer(message.reply_to_message.from_user)
    if "ПОБЕЖДАЮ" in message.text.upper():
        for task in player.taskset.tasks:
            if 21 == task.id and task.type == 'normal':
                return "+"


def nozhn_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text or not message.reply_to_message:
        return
    player = findplayer(message.reply_to_message.from_user)
    if "ПОБЕЖДАЮ" in message.text.upper():
        for task in player.taskset.tasks:
            # У МИШИ НЕ 19
            if 19 == task.id and task.type == 'normal':
                return "+"


def fylhtq_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    kirill = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    text = message.text.lower()
    for char in kirill:
        if char in text:
            return "-"
    if player.taskset.get_task_duration() > 3600 * 3:
        return "+"


def fober_check(message, player, data):
    if not data:
        data.append(0)
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

    if player.taskset.get_task_duration() > 3600 * 6:
        return "+"


def mozg_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    for i in range(len(message.text)):
        if message.text[i].isalpha() and len(message.text) > i + 1 and message.text[i+1] != ' ':
            return "-"
    if player.taskset.get_task_duration() > 3600 * 3:
        return "+"


def malefika_check(message, player, data):
    if message.from_user.id != player.user.id:
        return

    if message.from_user.id == player.user.id and message.text and message.reply_to_message \
       and "ПРЕДСКАЗЫВАЮ" in message.text.upper() and not data:
        enemy = findplayer(message.reply_to_message.from_user)
        data.append(enemy.taskset.message)
        data.append(enemy.user)
        data.append(enemy.task_completed)

    if message.from_user.id == player.user.id and data:
        enemy = findplayer(data[1])
        if enemy.taskset.message == data[0] and enemy.task_status == 1:
            return
        elif enemy.task_completed == data[2]:
            return "+"
        elif enemy.task_completed > data[2]:
            return "-"


def katissa_check(message, player, data):
    if message.from_user.id == player.user.id:
        return "-"
    if player.taskset.get_task_duration() > 3600 * 6:
        return "+"


def patricia_check(message, player, data):
    if message.from_user.id != player.user.id or not message.text:
        return
    words = message.text.split()
    if len(words) < 20:
        return "-"
    if player.taskset.get_task_duration() > 3600 * 3:
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
    if player.taskset.get_task_duration() > 3600 * 6:
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
    try:
        if message.from_user.username in config.root and root_log:
            bot.send_message(debug_chat_id, root_log)
    except telebot.apihelper.ApiException:
        bot.send_message(debug_chat_id, "log failed")
    finally:
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




@bot.message_handler(commands=["whereisthisfuckingpredmetattime"])
def find_item(message):
    if message.from_user.username in config.root:
        text = str(message.text[len("whereisthisfuckingpredmetattime")+2:])
        try:
            time = int(text)
            path = math.e * time
            diag = 4
            path -= math.floor(path / diag) * diag
            path -= diag/2
            path = abs(path)/2
            x = str(1-path) + ','
            bot.send_message(message.chat.id, x+x+x+x[:-1])
        except (ValueError, telebot.apihelper.ApiException):
            bot.send_message(message.chat.id, "НЕ ЗНАЮ. СПРОСИ У МИШИ")


@bot.message_handler(commands=["clean"])
def clean(message):
    if message.from_user.username in config.root:
        for player in active_players:
            if player.taskset.get_task_duration() > config.seconds_in_day * 14:
                player.taskset.clean()


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


def ping(arg):
    target = random.choice(active_players)
    found = False
    for chat_id in allow_chats:
        try:
            status = bot.get_chat_member(chat_id, target.user.id)
        except telebot.apihelper.ApiException:
            continue
        if status and status.status in ["member", "creator",
                                        "administrator"] and not target.user.username == "rakon_bot":
            found = True
            break
    if found and target.user.username:
        diff = time.time() - target.last_mess
        if diff < 60:
            how_davno = "СОВСЕМ ЧУТОК"
        elif diff > 3600:
            how_davno = "ОЧЕНЬ ДАВНО"
        else:
            how_davno = str(int(diff // 60)) + " МИНУТ"

        target_name = "@" + target.user.username
        reaction = random.choice(config.pings)
        bot.send_message(chat_id, reaction[0] + target_name + reaction[1] + how_davno + reaction[2])
    timer = Timer(300, ping, [0])
    timer.start()


@bot.message_handler(commands=["ping_start"])
def ping_start(message):
    timer = Timer(300, ping, [0])
    timer.start()


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


'''
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
'''
@bot.message_handler(commands=["kill", "KILL"])
def kill(message):
    player = findplayer(message.from_user)
    if player.isdura:
        has_murder_been_done = False
        has_arrow_been_thrown = False
        how_many_victims = 0
        winner_check = False
        if player.dura_status == 2:
            player.dura_status = 0
            killer = ''
            if player.user.username:
                killer += '@' + str(player.user.username)
            else:
                if player.user.first_name:
                    killer += str(player.user.first_name) + '\t'
                if player.user.last_name:
                    killer += str(player.user.last_name)
            text = str(message.text[6:])
            if not text:
                chance = random.randint(0, 2)
                if chance == 0:
                    for chat in dura_chat:
                        bot.send_message(chat, killer + " УРОНИЛ ВЕРХОВНУЮ СТРЕЛУ МАГИИ, "
                                                               "ОНА ОТСКОЧИЛА ОТ ПОЛА И УДАРИЛА В ЛЮСТРУ. "
                                                               "ЛЮСТРА УПАЛА НА ИГРОКА И УБИЛА ЕГО. НЯПОКА.")
                    player.dura_status = 3
                    player.isdura = False
                    player.has_a_shield = False
                    winner_check = True
                else:
                    if chance == 1:
                        for chat in dura_chat:
                            bot.send_message(chat, killer +
                                             " УРОНИЛ ВЕРХОВНУЮ СТРЕЛУ МАГИИ И ПОТЕРЯЛ ЕЁ, АЗАЗА.")
                    else:
                        for chat in dura_chat:
                            bot.send_message(chat, killer +
                                             " ДЕЛАЕТ ТАК:")
                            bot.send_document(chat, 'CgADAgADaQEAAtmjWUtJal60t9pcOwI')

                    player.dura_status = 0
                    player.can_get_a_shield = True
                    return
            try:
                num = int(text)
            except ValueError:
                if text:
                    bot.send_message(message.chat.id, "ТЫ ДУРА?")
                    player.dura_status = 2
                    return
                else:
                    num = player.dura_num
            try:
                bot.send_message(player.user.id, "ВЫБОР СДЕЛАН, ПУЩЕНА СТРЕЛА.")
            except telebot.apihelper.ApiException:
                bot.send_message(message.chat.id, "ВЫБОР СДЕЛАН, ПУЩЕНА СТРЕЛА.", reply_to_message_id=message.message_id)
            for victim in active_players:
                if victim.isdura:
                    how_many_victims += 1
                    if victim.dura_num == num:
                        name = ""
                        if victim.user.username:
                            name += '@' + str(victim.user.username)
                        else:
                            if victim.user.first_name:
                                name += str(victim.user.first_name) + '\t'
                            if victim.user.last_name:
                                name += str(victim.user.last_name)
                        if not victim.has_a_shield:
                            has_murder_been_done = True
                            victim.isdura = False
                            victim.dura_status = 3
                            for chat in dura_chat:
                                bot.send_message(chat, killer + " СТРЕЛЯЕТ ВЕРХОВНОЙ СТРЕЛОЙ "
                                                                        "МАГИИ. ТЕБЯ УБИЛИ, " + name + " :(")
                        else:
                            victim.has_a_shield = False
                            for chat in dura_chat:
                                bot.send_message(chat, killer + " СТРЕЛЯЕТ. CТРЕЛА УДАРЯЕТСЯ О ЩИТ И ЛОМАЕТСЯ, "
                                                   "А ЩИТ ПАДАЕТ НА ПОЛ И РАЗБИВАЕТСЯ НА МЕЛКИЕ КУСОЧКИ. " + name + " ВЫЖИЛ.")
                            has_arrow_been_thrown = True
            if has_murder_been_done or has_arrow_been_thrown:
                player.can_get_a_shield = True
            if how_many_victims == 2 and has_murder_been_done or how_many_victims == 1 and winner_check:
                winner_name = ''
                for winner in active_players:
                    if winner.isdura:
                        if winner.user.first_name:
                            winner_name += str(winner.user.first_name) + " "
                        if winner.user.last_name:
                                winner_name += str(winner.user.last_name) + " "
                        if winner.user.username:
                            winner_name += '@' + str(winner.user.username) + " "
                for chat in dura_chat:
                    bot.send_message(chat, winner_name + "ПОДЕБИЛ В ЭТОЙ ЖЕСТОКОЙ ИГРЕ! ОУРА, ТОВАРИЩИ!")
                try:
                    bot.send_message(tipa_tri_skobki_chat, "ТОВАРИЩИ ПРОВЕРЯТОРЫ, ТУТ ЧЕЛОВЕЧКА НАГРАДИТЬ НУЖНО, ЭТО " +
                                 winner_name)
                except telebot.apihelper.ApiException:
                    bot.send_message(debug_chat_id, "ТОВАРИЩИ ПРОВЕРЯТОРЫ, ТУТ ЧЕЛОВЕЧКА НАГРАДИТЬ НУЖНО, ЭТО " +
                                     winner_name)
            if not has_murder_been_done and not winner_check and not has_arrow_been_thrown:
                player.dura_status = 2
                bot.send_message(message.chat.id, 'ЧТО-ТО ПОШЛО НЕ ТАК, УМНАЯ СТРЕЛА ВЕРНУЛАСЬ ОБРАТНО. '
                                                  'ПЕПЕБРОСЬ.', reply_to_message_id=message.message_id)
                return
        else:
            bot.send_message(message.chat.id, 'ТЫ НЕ МОЖЕШЬ НИКОГО УБИТЬ!', reply_to_message_id=message.message_id)


@bot.message_handler(commands=["net_ty", "NET_TY"])
def shield(message):
    player = findplayer(message.from_user)
    if player.isdura:
        if not player.has_a_shield and player.dura_status == 2:
            if player.can_get_a_shield:
                player.has_a_shield = True
                player.dura_status = 0
                player.can_get_a_shield = False
                bot.send_message(message.chat.id, 'ТЕПЕРЬ ТЫ ЗАЩИЩЁН ОТ ОДНОЙ АТАКИ.',
                                                                                reply_to_message_id=message.message_id)
                name = ""
                if player.user.username:
                    name += '@' + str(player.user.username)
                else:
                    if player.user.first_name:
                        name += str(player.user.first_name) + '\t'
                    if player.user.last_name:
                        name += str(player.user.last_name)
                for chat in dura_chat:
                    bot.send_message(chat, name + " ВЗЯЛ ЩИТ.")
                return
            else:
                bot.send_message(message.chat.id, 'ТЫ НЕ МОЖЕШЬ ЗАЩИЩАТЬСЯ 2 РАЗА ПОДРЯД. ВРЕМЯ АТАКОВАТЬ!',
                                                                                reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, 'ОБОЙДЁШЬСЯ.', reply_to_message_id=message.message_id)


@bot.message_handler(commands=["dura", "DURA"])
def dura_reg(message):
    if message.from_user.id == message.chat.id:
        player = findplayer(message.from_user)
        if not player.isdura:
            if player.dura_status == 3:
                return
            if player.dura_started:
                bot.send_message(message.chat.id, 'ТЫ НЕ ДУРА, ТЫ ТОРМОЗ.', reply_to_message_id=message.message_id)
                return
            player.isdura = True
            bot.send_message(message.chat.id, random.choice(["ДОРОГИ НАЗАД НЕ БУДЕТ, ТЫ В КУРСЕ?",
                                                             "НАДЕЮСЬ, ТЫ КАК СЛЕДУЕТ ПРОКАЧАЛ МЕТКОСТЬ.",
                                                             "ОТЛИЧНО! ТЕПЕРЬ ЖДИ НАЧАЛА ИГРЫ."]))
    else:
        bot.send_message(message.chat.id, 'ТЫ СОБРАЛСЯ РЕГАТЬСЯ У ВСЕХ НА ВИДУ? ГО КО МНЕ В ЛИЧКУ ;)',
                         reply_to_message_id=message.message_id)


def dura_approve(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        if player.dura_status == 1:
            answer = ""
            player.dura_status = 2
            list = ""
            for victim in active_players:
                if victim.isdura:
                    if victim.user.first_name:
                        list += str(victim.user.first_name) + '\t'
                    if victim.user.last_name:
                        list += str(victim.user.last_name) + '\t'
                    if victim.user.username:
                        list += '@' + str(victim.user.username) + '\t'
                    if victim.has_a_shield:
                        list += "(ЩИТ)" + '\t'
                    list += "(" + str(victim.dura_num) + ")"
                    list += '\n'
            answer += "У ТЕБЯ ПОЯВИЛАСЬ ВОЗМОЖНОСТЬ ИЗБАВИТЬСЯ ОТ ЛЮБОГО ИЗ ТВОИХ СОПЕРНИКОВ!\n" + list
            answer += "\nОТПРАВЬ КОМАНДУ /kill n (ГДЕ n = НОМЕР ЖЕРТВЫ ИЗ СПИСКА)."
            if not player.has_a_shield:
                answer += "\nА ЕЩЁ ТЫ МОЖЕШЬ ВЗЯТЬ ЩИТ КОМАНДОЙ /net_ty, НО НЕЛЬЗЯ ДЕРЖАТЬ ПРИ СЕБЕ БОЛЕЕ ОДНОГО " \
                          "ЩИТА. ЩИТ ЛОМАЕТСЯ, КОГДА ТЕБЯ ПЫТАЮТСЯ УБИТЬ."
            try:
                bot.send_message(player.user.id, answer)
            except telebot.apihelper.ApiException:
                bot.send_message(message.chat.id, answer, reply_to_message_id=message.message_id)


@bot.message_handler(commands=["get_nums"])
def get_dura_nums(message):
    if message.from_user.username in config.root:
        answer = ""
        does_someone_participate = False
        for player in active_players:
             if player.isdura:
                does_someone_participate = True
                if player.user.first_name:
                    answer += str(player.user.first_name) + '\t'
                if player.user.last_name:
                    answer += str(player.user.last_name) + '\t'
                if player.user.username:
                    answer += '@' + str(player.user.username) + '.\n'
        if does_someone_participate:
            bot.send_message(message.chat.id, answer)
        else:
            answer = "ПОКА ЧТО ЗАРЕГИСТРИРОВАВШИХСЯ НЕТ. БУДЬ ПЕРВЫМ, НАЖМИ /dura!"
            bot.send_message(message.chat.id, answer)


def dura_fail(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        if player.dura_status == 1:
            player.dura_status = 0
            player.dura_task = None
            bot.send_message(message.chat.id, "ЛАДНО, НИЧТОЖЕСТВО, БЕРИ ДРУГОЕ ЗАДАНИЕ.",
                                                                reply_to_message_id=message.reply_to_message.message_id)

@bot.message_handler(commands=["start_dura"])
def start_dura(message):
    num = 1
    for player in active_players:
        if player.isdura:
            player.dura_status = 0
            player.dura_num = num
            num += 1
            try:
                bot.send_message(player.user.id, "ЕСЛИ ТЕБЕ ПРИШЛО ЭТО СООБЩЕНИЕ, ЗНАЧИТ ТЫ РЕГИСТРИРОВАЛСЯ НА "
                                 "<b>БИТВУ МАГОВ</b>. ИГРА НАЧАЛАСЬ!", parse_mode="HTML")
            except telebot.apihelper.ApiException:
                continue
        player.dura_started = True
    for chat in dura_chat:
        bot.send_message(chat, "ИГРА НАЧАЛАСЬ! НАЖИМАЙТЕ /dura_task И СПАСАЙТЕСЬ, ГЛУПЦЫ!")

@bot.message_handler(commands=["clean_dura"])
def clean_dura_list(message):
    for player in active_players:
        player.dura_started = False
        player.dura_task = None
        player.dura_status = 0
        player.isdura = False
        player.can_get_a_shield = True
        player.has_a_shield = False

def random_task():
    task = ''
    task += "ТЫ " + random.choice(config.dura_who) + ". "
    task += random.choice(config.dura_do) + " "
    task += random.choice(config.dura_what) + " "
    task += random.choice(config.dura_how) + "."

    return task


@bot.message_handler(commands=["dura_task"])
def get_dura_task(message):
    player = findplayer(message.from_user)
    if player.isdura and player.dura_started:
        if player.dura_status == 1:
            bot.send_message(message.chat.id, 'ТЫ ДУРА? У ТЕБЯ УЖЕ ЕСТЬ ЗАДАНИЕ.', reply_to_message_id=message.message_id)
        if player.dura_status == 0:
            if message.from_user.id == message.chat.id:
                bot.send_message(message.chat.id, 'ТЫ ДУРА? БЕРИ ЗАДАНИЕ У ВСЕХ НА ВИДУ!',
                                                                                reply_to_message_id=message.message_id)
                return
            player.dura_status = 1
            sticker = random.choice(config.dura_stickers)
            try:
                bot.send_sticker(message.chat.id, sticker)
            except telebot.apihelper.ApiException:
                print("STICKER WAS NOT SEND", sticker)
            task = random_task()
            bot.send_message(message.chat.id, task)
            player.dura_task = task
        if player.dura_status == 2:
            bot.send_message(message.chat.id, "ПРЕЖДЕ ЧЕМ ВЗЯТЬ НОВОЕ ЗАДАНИЕ, НУЖНО КОГО-ТО УБИТЬ!",
                                                                                reply_to_message_id=message.message_id)
    if player.dura_status == 3:
        bot.send_message(message.chat.id, "УСПОКОЙСЯ, ТЫ УЖЕ НИЧЕГО НЕ РЕШАЕШЬ.", reply_to_message_id=message.message_id)


@bot.message_handler(commands=["my_dura"])
def check_my_dura_task(message):
    player = findplayer(message.from_user)
    if player.isdura and player.dura_status == 0:
        bot.send_message(message.chat.id, "НАЖМИ /dura_task!", reply_to_message_id=message.message_id)
    if player.dura_status == 1:
        bot.send_message(message.chat.id, player.dura_task,  reply_to_message_id=message.message_id)
    if player.dura_status == 2:
        bot.send_message(message.chat.id, "ПОКА ЧТО У ТЕБЯ НЕТ ЗАДАНИЯ.", reply_to_message_id=message.message_id)
    if player.dura_status == 3:
        bot.send_message(message.chat.id, "УСПОКОЙСЯ, ТЫ УЖЕ НИЧЕГО НЕ РЕШАЕШЬ.", reply_to_message_id=message.message_id)


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


@bot.message_handler(commands=["alpha_samka"])
def alpha_samka(message):
    answer = "ИЕРАРХИЯ РАКОНОВ:\n"
    i = 1
    newlist = sorted(active_players, key=lambda xxx: xxx.alpha, reverse=True)
    for player in newlist:
        if player.alpha:
            answer += str(i) + '.\t'
            if player.user.first_name:
                answer += '<b>' + str(player.user.first_name) + '</b>' + '\t'
            if player.user.last_name:
                answer += '<b>' + str(player.user.last_name) + '</b>' + '\t'
            if player.user.username:
                answer += '@' + str(player.user.username) + '.\t'
            if player.alpha > 0:
                answer += '\nАЛЬФАЧЕСТВО:           <b>' + str(player.alpha) + '</b>\n'
            else:
                answer += '\nОМЕЖЕСТВО:             <b>' + str(player.alpha) + '</b>\n'
            i += 1
    bot.send_message(message.chat.id, answer, parse_mode="HTML")


@bot.message_handler(commands=["top_pozora"])
def pozor(message):
    text = "ТОП ПОЗОРА: \n"
    i = 1

    for player in active_players:
        if player.taskset.get_task_duration() > 3600 * 500:
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
    if player.taskset.status == 1:
        if player.task_completed % 100 < 40 and player.task_completed < 200\
                or player.task_completed >= 300:
            for task in player.taskset.tasks:
                if task.required:
                    answer += task.to_text() + "\n"
        else:
            answer += ")))\n"
        for task in player.taskset.tasks:
            if task.required:
                task_full = task.full_info()
                if task_full[2] * 60 - player.taskset.get_task_duration() // 60 > tm:
                    tm = task_full[2] * 60 - player.taskset.get_task_duration() // 60
        if tm > 0:
            answer += "Осталось времени: " + str('{:.0f}'.format(tm // 60)) + " часов и " + \
                      str('{:.0f}'.format(tm % 60)) + " минут\n"
        else:
            answer += "ВЫПОЛНЯЙ, ПОКА НЕ ЗАСЧИТАЮТ!\n"
    answer += "Всего сделано: " + str(player.task_completed % 50) + ".\n"
    if player.task_completed < 300:
        left = config.seconds_in_day
    else:
        left = config.seconds_in_day * 7
    tm = left // 60 - player.taskset.get_task_duration() // 60
    if tm > 0:
        tm += 1  # 1 min more
        answer += "До следующего задания: " + str('{:.0f}'.format(tm // 60)) + " часов и " + \
                  str('{:.0f}'.format(tm % 60)) + " минут\n"
    try:
        if player.taskset.message and player.taskset.message.chat.id == message.chat.id:
            bot.send_message(message.chat.id, answer, reply_to_message_id=player.taskset.message.message_id)
        else:
            raise telebot.apihelper.ApiException("Wrong chat", "my_task", "Exception")
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


def give_task(player, task_type, chat):
    if task_type in ['normal', 'black', 'long']:
        req = 1
    player.taskset.new(task_type, req)
    task = player.taskset.tasks[-1].full_info()
    bot.send_stickers(chat, task[0])
    return task


# collect players and give them tasks
@bot.message_handler(commands=["get_task"])
def get_task(message):
    if message.chat.id not in allow_chats:
        bot.send_message(message.chat.id, "ПО ЛИЧКАМ ШУШУКАЕТЕСЬ? НЕ ТОТ ЧЯТИК!",
                         reply_to_message_id=message.message_id)
        return
    
    player = findplayer(message.from_user)
    if player.task_completed < 300 and player.taskset.get_task_duration() > config.seconds_in_day\
            or player.taskset.get_task_duration() > 7 * config.seconds_in_day:
        player.taskset.status = 0
        player.taskset.clean()
        remove_task_check(player, message)
    if player.taskset.status == 1:
        bot.send_message(message.chat.id, "ТЫ УЖЕ ЧТО-ТО ДЕЛАЕШЬ!", reply_to_message_id=message.message_id)
        return
    elif player.taskset.status == 2:
        bot.send_message(message.chat.id, "ТЫ УЖЕ НЕ СМОГ!", reply_to_message_id=message.message_id)
        return
    
    if player.taskset.get_task_duration() < config.seconds_in_day:
        bot.send_message(message.chat.id, "НОВОЕ ЗАДАНИЕ БУДЕТ НЕСКОРО!",
                         reply_to_message_id=message.message_id)
        return

    player.taskset.status = 1
    player.taskset.message = message

    rand = random.randint(1, 500)
    if rand == 237 and player.task_completed < 100:
        task = ['CAADAgADaQADP_vRD78igQttLbufAg', 'КОЛДУЮ, КОЛДУЮ... ВЖУХ! И ТЫ ПИДОР ДНЯ.', 0, 0]
        bot.send_sticker(message.chat.id, task[0])
        bot.send_message(message.chat.id, task[1])
        return
    elif rand == 237:
        task = ['CAADAgADPAADE3yuAgyZWgXL5Kj9Ag', 'ТЫ ЧОРНЫЙ ПИДОР ДНЯ. ЗАЙМИСЬ СЕКСОМ НА '
                                                  'ПРОЕЗЖЕЙ ЧАСТИ.', 0, 0]
        bot.send_sticker(message.chat.id, task[0])
        bot.send_message(message.chat.id, task[1])
        return

    if player.task_completed >= 300:
        task = give_task(player, 'long', message.chat.id)
    elif 300 > player.task_completed >= 100:
        task = give_task(player, 'black', message.chat.id)
    else:
        task = give_task(player, 'normal', message.chat.id)

    if player.task_completed % 100 < 40 and player.task_completed < 200 \
            or player.task_completed >= 300:
        bot.send_message(message.chat.id, task[1])
    else:
        text = random.choice(["ТЫ УЖЕ БОЛЬШОЙ, САМ РАЗБЕРЕШЬСЯ", "<СПОЙЛЕРЫ>", "Я ПОЗАБЫЛ ВСЕ СЛОВА",
                              "ЗДЕСЬ БЫЛО ЧТО-ТО ДЛИННОЕ ЕЩЁ"])
        bot.send_message(message.chat.id, text)
    player.informed = False
    player.mess_sended = False

    if 99 >= player.task_completed >= 70 or 300 > player.task_completed >= 150:
        bot.send_message(message.chat.id, "А ВОТ ЕЩЁ ТЕБЕ...")
        give_task(player, 'normal', message.chat.id)
    if player.task_completed % 100 == 99:
        give_task(player, 'normal', message.chat.id)
        give_task(player, 'normal', message.chat.id)
        bot.send_message(message.chat.id, "АЗАЗА, УДАЧИ")
    if 300 > player.task_completed > 200:
        rand = random.randint(0, len(config.anti_tasks) - 1)
        podtask = config.anti_tasks[rand]
        player.taskset.modifier = rand
        bot.send_message(message.chat.id, podtask)

    backup(None)

    for task in player.taskset.tasks:
        if task.required:
            task_full = task.full_info()
            if len(task_full) > 4:
                current_task_funcs.append(check_func_costruct(player, task_funcs[task_full[4]]))
            else:
                current_task_funcs.append(check_func_costruct(player, infinity_check))


# root command. See all players with tasks.
@bot.message_handler(commands=["all_tasks"])
def all_tasks(message):
    if message.from_user.username in config.root:
        for player in active_players:
            if player.taskset.check_normal() and player.taskset.status == 1:
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


@bot.message_handler(commands=["СКУЧНО"])
def bored(message):
    player = findplayer(message.from_user)
    if player.task_completed < 300 or message.chat.id != player.user.id or \
        time.time() - player.last_optional_task < config.seconds_in_day:
        return

    try:
        task1 = give_task(player, 'black', message.chat.id)
        task2 = give_task(player, 'normal', message.chat.id)
        player.last_optional_task = time.time()
        bot.send_message(debug_chat_id, player.user.username + " СКУЧАЕТ")
        bot.send_stickers(debug_chat_id, [task1[0], task2[0]])
    except telebot.apihelper.ApiException:
        print("boring failed")


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
        if player.taskset.check_normal():
            if player.taskset.status == 0:
                player.taskset.status = 1
                player.task_completed -= 1
                bot.send_message(message.chat.id, "НЕ, АДМИНАМ НЕ НРАВИТСЯ")

                for task in player.taskset.tasks:
                    if task.required:
                        task_full = task.full_info()
                        if len(task_full) > 4:
                            current_task_funcs.append(check_func_costruct(player, task_funcs[task_full[4]]))
                        else:
                            current_task_funcs.append(check_func_costruct(player, infinity_check))

        logging(message)
        backup(None)


def task_fail(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        if player.taskset.status == 1:
            player.taskset.status = 2
            remove_task_check(player, message)
            bot.send_message(message.chat.id, "ЗАДАНИЕ ПРОВАЛЕНО!",
                             reply_to_message_id=message.reply_to_message.message_id)
            if player.mess_from_bot:
                bot.send_message(player.user.id, "К СОЖАЛЕНИЮ, ЗАДАНИЕ ПРОВАЛЕНО.")
        logging(message)
        backup(None)


def task_complete(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        logging(message)
        player = findplayer(message.reply_to_message.from_user)
        if player.taskset.status == 1:
            player.taskset.status = 0
            remove_task_check(player, message)
            player.task_completed += 1
            backup(None)
            if player.task_completed == 50:
                bot.send_message(player.user.id, "АЗАЗА, ТЫ УМИР")
            elif player.task_completed == 100:
                bot.send_message(player.user.id, "СГОРИ ДОТЛА! КАК И ВСЕ ТВОИ ОЧКИ")
            elif player.task_completed == 150:
                bot.send_message(player.user.id, "УРА УРА СУИЦИД")
            elif player.task_completed == 200:
                bot.send_message(player.user.id, "ЧОМУ ТАК ХОЛОДНО МЕНІ\nІ ЩО БОЛИТЬ У ГОЛОВІ\nЯ ДУМАВ ПІСЛЯ СМЕРТІ\n"
                                                 "Я СТАНУ КУПОЮ ЗЕМЛІ")
            elif player.task_completed == 250:
                bot.send_sticker(player.user.id, 'CAADAgADCAIAAqEdYEjI2O5iJkD4qQI')
            elif player.task_completed == 300:
                bot.send_message(player.user.id, "I'LL ESCAPE NOW FROM THAT WORLD\nFROM THE WORLD OF "
                                 + player.user.username + "\nTHERE IS NOWHERE I CAN TURN\nTHERE IS NO WAY TO GO ON")
            elif player.task_completed == 301:
                bot.send_message(player.user.id, "/СКУЧНО? НА САМОМ ДЕЛЕ ТЫ МОЖЕШЬ БРАТЬ ДОПОЛНИТЕЛЬНЫЕ ЗАДАНИЯ. "
                                                 "ПРАВДА, ЗАСЧИТЫВАТЬСЯ ОНИ НЕ БУДУТ, ТАК ЧТО ПРОДОЛЖАЙ ВЫПОЛНЯТЬ ЛОНГИ."
                                                 " АХ ДА, БОЛЬШИНСТВО ПРОВЕРЯТОРОВ ДАЖЕ НЕ ДОГАДЫВАЮТСЯ О ТАКОМ ;)")
            if player.task_completed % 50 == 0:
                bot.send_message(message.chat.id, "ЗАДАНИЕ ВЫПОЛНЕНО!\nВСЕГО СДЕЛАНО 50 ЗАДАНИЙ!",
                                 reply_to_message_id=message.reply_to_message.message_id)
                time.sleep(3)
                bot.send_message(message.chat.id, "ХОТЯЯЯЯ...")
                time.sleep(1)
                mess = "АНТИКЛАЦ!\n"
                for player in range(48):
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

# secret_santa = [336595041]
# sherif = [347438021]
# 
# 
# @bot.message_handler(commands=["send_ng_tasks"])
# def send_ng_tasks(message):
#     if message.from_user.id == message.chat.id and message.from_user.username in config.root:
#         for player in active_players:
#             if player.new_year and player.user.id not in secret_santa and player.user.id not in sherif:
#                 try:
#                     n = random.randint(0, len(config.ng_tasks) - 1)
#                     task = config.ng_tasks[n]
#                     player.ng_task_id = n
#                     bot.send_sticker(player.user.id, 'CAADAgADJQADsjRGHuRrNOA7RLqJAg')
#                     bot.send_message(player.user.id, task)
#                 except telebot.apihelper.ApiException:
#                     continue
#             elif player.user.id in secret_santa:
#                 try:
#                     player.ng_task_id = -1
#                     bot.send_sticker(player.user.id, 'CAADAgADJQADsjRGHuRrNOA7RLqJAg')
#                     bot.send_message(player.user.id, "ТЫ ТАЙНЫЙ САНТА. ПОБЕДИШЬ, ЕСЛИ НИКТО НЕ ОТГАДАЕТ ТВОЮ РОЛЬ ДО "
#                                                      "НОВОГО ГОДА.")
#                 except telebot.apihelper.ApiException:
#                     continue
#             elif player.user.id in sherif:
#                 try:
#                     player.ng_task_id = -2
#                     bot.send_sticker(player.user.id, 'CAADAgADJQADsjRGHuRrNOA7RLqJAg')
#                     bot.send_message(player.user.id,
#                                      "ТЫ ОЛЕНЬ. КТО-ТО ИЗ ВЗЯВШИХ НОВОГОДНЕЕ ЗАДАНИЕ - ТАЙНЫЙ САНТА. ТВОЯ "
#                                      "ЗАДАЧА - ЕГО ОТЫСКАТЬ. У ТЕБЯ ОДНА ПОПЫТКА. ОТВЕТ ПРИСЫЛАТЬ ЧЕРЕЗ В "
#                                      "ЛИЧКУ @Deepwarrior ИЛИ @Uhi_Official.")
#                 except telebot.apihelper.ApiException:
#                     continue
# 
# 
# @bot.message_handler(commands=["all_ng"])
# def all_ng_tasks(message):
#     if message.from_user.id == message.chat.id and message.from_user.username in config.root:
#         spisok = ""
#         for player in active_players:
#             if player.new_year:
#                 if player.user.first_name:
#                     spisok += str(player.user.first_name) + '\t'
#                 if player.user.last_name:
#                     spisok += str(player.user.last_name) + '\t'
#                 if player.user.username:
#                     spisok += '@' + str(player.user.username) + '.\t'
#                 if player.user.id not in secret_santa and player.user.id not in sherif:
#                     spisok += config.ng_tasks[player.ng_task_id]
#                 elif player.user.id in secret_santa:
#                     spisok += "ТАЙНЫЙ САНТА"
#                 elif player.user.id in sherif:
#                     spisok += "ШЕРИФ"
#                 spisok += '\n'
#         bot.send_message(message.chat.id, spisok)


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

        if player.task_completed % 50 == 0:
            player.task_completed -= 1
            bot.send_message(message.chat.id, "АЗАЗА. НЕТ.",
                             reply_to_message_id=message.reply_to_message.message_id)
        backup(None)


def anti_task(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        logging(message)
        player = findplayer(message.reply_to_message.from_user)
        player.task_completed -= 1
        bot.send_message(message.chat.id, "ОТМЕНА, ОТМЕНА!", reply_to_message_id=message.reply_to_message.message_id)
        if player.task_completed % 50 == 49:
            player.task_completed += 1
            bot.send_message(message.chat.id, "АЗАЗА. НЕТ.",
                             reply_to_message_id=message.reply_to_message.message_id)
        backup(None)


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
    rand2 = random.randint(0, 1)
    if not rand2:
        sticker_set = config.numbers
    else:
        sticker_set = config.hermite_gaussian_modes
    if rand:
        bot.send_sticker(message.chat.id, sticker_set[((minutes + rand + 1) % 60) // 10],
                         reply_to_message_id=message.message_id)
        bot.send_sticker(message.chat.id, sticker_set[((minutes + rand + 1) % 60) % 10],
                         reply_to_message_id=message.message_id)

        timer = Timer(60 * rand - seconds, vbuena, [message.chat.id])
        timer.start()
        all_timers.append(timer)
    else:
        react(reaction, message)
    #0⃣1⃣2⃣3⃣4⃣5⃣6⃣7⃣8⃣9⃣🔟


def kick_bots(reaction, message):
    targets = [208343353, 88135026, 280982408, 200164142, 226543640, 121913006, 199378994, 110193686, 346903988,
               29664231, 135069175]
    for target in targets:
        try:
            bot.kick_chat_member(message.chat.id, target)
            time.sleep(2)
        except telebot.apihelper.ApiException:
            time.sleep(1)


def razbanb(arg):
    bot.restrict_chat_member(arg[0], arg[1], 0, True, True, True, True)


def kick_lyuds(reaction, message):
    try:
        bot.restrict_chat_member(message.chat.id, message.from_user.id, 2*60*60, False, False, False, False)
        timer = Timer(2*60*60, razbanb, [[message.chat.id, message.from_user.id]])
        timer.start()
    except telebot.apihelper.ApiException:
        time.sleep(1)


def mem_react(reaction, message):
    rand = random.randint(0, 10)
    if rand < 10:
        bot.send_message(message.chat.id, 'МУМЫРИ!', reply_to_message_id=message.message_id)
    else:
        react(reaction, message)


def set_admin(reaction, message):
    if message.from_user.username in config.root or message.from_user.id in config.alpha_moder:
        try:
            bot.promote_chat_member(message.chat.id, message.from_user.id,
                                    True, False, False, True, True, True, True, True)
            bot.send_message(message.chat.id, 'ЗВЕЗДА У НОГ ТВОИХ!', reply_to_message_id=message.message_id)
            logging(message)
        except telebot.apihelper.ApiException:
            time.sleep(1)


@bot.message_handler(commands=["stop_stickers"])
def stop_stickers(message):
    if message.from_user.username in config.root:
        for player in active_players:
            if player.task_completed < 100 and not player.task_id == 42 or player.task_completed >= 100 and not player.task_id == 10:
                try:
                    bot.restrict_chat_member(message.chat.id, player.user.id, True, True, False, False, False)
                except telebot.apihelper.ApiException:
                    continue


def whois(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        if player.taskset.check_normal() and player.taskset.status == 1:
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


def alpha_change(reaction, message):
    if message.from_user.id in config.alpha_moder and message.reply_to_message:
        player = findplayer(message.reply_to_message.from_user)
        if message.text.upper() == "АЛЬФА":
            player.alpha += 0.1
        elif message.text.upper() == "ОМЕГА":
            player.alpha -= 0.1
        backup(None)


def change_invite_link(arg):
    bot.export_chat_invite_link(vip_chat_id)


def dura_win(reaction, message):
    if message.chat.id == 336595041:
        try:
            link = bot.export_chat_invite_link(vip_chat_id)
            bot.send_message(message.chat.id, link)
            timer = Timer(30, change_invite_link, [vip_chat_id])
            timer.start()
        except telebot.apihelper.ApiException:
            bot.send_message(message.chat.id, "Я ПОТЕРЯЛ ССЫЛКУ, ПИШИ КОМУ-ТО ЕЩЁ")
    elif message.from_user.id == 336595041:
        try:
            bot.promote_chat_member(message.chat.id, message.from_user.id,
                                    True, False, False, True, True, True, True, False)
            bot.send_message(message.chat.id, 'О БОГИНЯ!', reply_to_message_id=message.message_id)
            logging(message)
        except telebot.apihelper.ApiException:
            bot.send_sticker(message.chat.id, 'CAADAgADagADsjRGHmMaqz0X8FMZAg')
    else:
        try:
            try:
                status = bot.get_chat_member(message.chat.id, 336595041)
            except telebot.apihelper.ApiException:
                return
            if status and status.status not in ["member", "creator", "administrator"]:
                return
            bot.restrict_chat_member(message.chat.id, 336595041, 2 * 60 * 60, False, False, False, False)

            bot.send_message(message.chat.id, "ВЫХОДИТЕ.")
            time.sleep(1)
            bot.send_message(message.chat.id, "ДО СВИДАНЬЯ!")
            time.sleep(2)
            bot.kick_chat_member(message.chat.id, 336595041)
            bot.unban_chat_member(message.chat.id, 336595041)
        except telebot.apihelper.ApiException:
            bot.send_sticker(message.chat.id, 'CAADAgAD2QADhzHUD6cgyh0aiKpjAg')


def why_yellow(reaction, message):
    bot.forward_message(message.chat.id, debug_chat_id, 57759)


def grammar_check(reaction, message):
    if not message.chat.id == message.from_user.id:
        text = message.text.upper()
        for word in config.grammar_nazi_dictionary.keys():
            if word in text:
                if not random.randint(0, 3):
                    try:
                        bot.restrict_chat_member(message.chat.id, message.from_user.id, 1 * 60 * 60, False, False, False,
                                                 False)
                        bot.send_message(message.chat.id, "ПОДУМОЙ НАД СВОИМ ПОВЕДЕНИЕМ.",
                                         reply_to_message_id=message.message_id)
                    except telebot.apihelper.ApiException:
                        bot.send_message(message.chat.id, "Я Б ТЕБЯ ЗАБАНИЛ, ДА ЛАПКИ МАРАТЬ НЕОХОТА.",
                                         reply_to_message_id=message.message_id)
                else:
                    str = random.choice(config.grammar_nazi_explanation)
                    answer = str[0] + config.grammar_nazi_dictionary[word] + str[1]
                    bot.send_message(message.chat.id, answer, reply_to_message_id=message.message_id)


reaction_funcs = {"task_rework": task_rework, "task_fail": task_fail, "task_complete": task_complete,
                  "task_extra": task_extra, "natalka": natalka, "kick_bots": kick_bots, "kick_lyuds": kick_lyuds,
                  "mem_react": mem_react, "anti_task": anti_task, "set_admin": set_admin, "whois": whois,
                  "stop_natalka": stop_natalka, "kick_citrus": kick_citrus, "kick_rels": kick_rels,
                  "kick_misha": kick_misha, "message_above": message_above, "alpha_change": alpha_change,
                  "dura_approve": dura_approve, "dura_fail": dura_fail, "dura_win": dura_win, "why_yellow": why_yellow,
                  "grammar_check": grammar_check
}


def notify(message):
    for player in active_players:
        if player.mess_from_bot and not player.mess_sended \
                and player.taskset.get_task_duration() > config.seconds_in_day:
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
                    if player.taskset.message.chat.id == message.chat.id:
                        bot.send_message(message.chat.id, "ТЕСТОВЫЙ АВТОЗАЧЁТ!", reply_to_message_id=player.taskset.message.message_id)
                    else:
                        raise telebot.apihelper.ApiException("Wrong chat", "my_task", "Exception")
                except telebot.apihelper.ApiException:
                    try:
                        bot.send_message(message.chat.id, "ТЕСТОВЫЙ АВТОЗАЧЁТ!")
                    except telebot.apihelper.ApiException:
                        print("+ failed")
        elif result == "-":
            try:
                if player.taskset.message.chat.id == message.chat.id:
                    bot.forward_message(tipa_tri_skobki_chat, player.taskset.message.chat.id, player.taskset.message.message_id)
                    bot.send_message(tipa_tri_skobki_chat, "ТЕСТОВЫЙ АВТОБАЯЗИД!")
                else:
                    raise telebot.apihelper.ApiException("Wrong chat", "my_task", "Exception")
            except telebot.apihelper.ApiException:
                try:
                    bot.send_message(message.chat.id, "ТЕСТОВЫЙ АВТОБАЯЗИД!")
                except telebot.apihelper.ApiException:
                    print("+ failed")
            current_task_funcs.remove(func)
            remove_task_check(player, message)

#CHANGE CHAT IN LEVEL_UP(), NO() AND message_parsing_to_bday_game(message)!!1
level = -1
def level_up():
    global level
    level += 1
    print(level)
    if level <= len(config.questions)-1:
        question = "ДЕРЖИ ВОПРОС:\n" + config.questions[level]
        bot.send_message(vip_chat_id, question)
    elif level == len(config.questions):
        bot.send_message(vip_chat_id, "ТЫ ПОДЕБИЛ")

@bot.message_handler(commands=["NEXT", "next"])
def next_level(message):
    if message.from_user.username in config.root:
        level_up()

@bot.message_handler(commands=["no", "NO"])
def send_fuck(message):
    if message.from_user.username in config.root:
        bot.send_sticker(vip_chat_id, random.choice(config.fuck_list))

@bot.message_handler(commands=["level", "LEVEL"])
def to_level(message):
    text = str(message.text[7:])
    try:
        num = int(text)
        global level
        level = num-1
        if num <= len(config.questions)-1:
            bot.send_message(debug_chat_id, "ЕСЛИ НАЖАТЬ НЕКСТ, ТО В ЧАТ ОТПРАВИТСЯ СЛЕДУЮЩЕЕ ЗАДАНИЕ:\n" +
                             config.questions[level+1])
        else:
            bot.send_message(debug_chat_id, "ЗАДАНИЙ БОЛЬШЕ НЕТ")
    except telebot.apihelper.ApiException:
        bot.send_message(debug_chat_id, "ПЕРЕДЕВЫВАЙ")



@bot.message_handler(commands=["R", "r"])
def fast_reply(message):
    if message.from_user.username in config.root and last_mess:
        text = message.text[3:]
        bot.send_message(last_mess, text)


def bot_AI(message):
    if message.text:
        text = message.text.upper()
    else:
        text = ""
    if message.from_user.id == message.chat.id and "ДЛИНОПУСИЧКА" not in text:
        bot.forward_message(spy_chat, message.chat.id, message.message_id)
        bot.send_message(spy_chat, "/mess " + str(message.from_user.id) + '  ' + message.from_user.first_name)
        global last_mess
        last_mess = message.from_user.id

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
        bot.send_message(message.chat.id, '\'' + message.sticker.file_id + '\'\n',# + message.sticker.set_name,
                         reply_to_message_id=message.message_id)
    task_check(message)
    player = findplayer(message.from_user)
    player.last_mess = time.time()
    bot_AI(message)


@bot.message_handler(content_types=["text"])
def message_parsing(message):
    notify(message)
    for reactions, oper in zip([config.reactions, config.superreactions], [operator.eq, operator.contains]):
        for reaction in reactions:
            if not reaction[2] or message.from_user.id == reaction[2]:
                for text in reaction[0]:
                    if oper(message.text.upper(), text):
                        if len(reaction) > 5:
                            reaction_funcs[reaction[5]](reaction, message)
                        else:
                            react(reaction, message)
                        break
    task_check(message)
    player = findplayer(message.from_user)
    player.last_mess = time.time()
    bot_AI(message)

    if message.chat.id == vip_chat_id:
        text = message.text.upper()
        global level
        if level < len(config.questions) - 1:
            if text == config.answers[level]:
                level_up()



#@bot.message_handler(content_types=["voice"])
def voice_parsing(message):
    if message.chat.id == debug_chat_id:
        bot.send_message(message.chat.id, '\'' + message.voice.file_id + '\'', reply_to_message_id=message.message_id)
    bot_AI(message)

@bot.message_handler(content_types=["document"])
def doc_parsing(message):
    if message.chat.id == debug_chat_id:
        bot.send_message(message.chat.id, '\'' + message.document.file_id + '\'', reply_to_message_id=message.message_id)
    bot_AI(message)


@bot.message_handler(content_types=["photo", "audio", "video", "video_note"])
def other_parsing(message):
    bot_AI(message)

if __name__ == '__main__':
    f = open('players.json', 'r')
    templist = json.load(f)
    for x in templist:
        active_players.append(players.Player(**x))
    f.close()
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
        except (ReadTimeout, socket.timeout, urllib3.exceptions.ReadTimeoutError):
            print("die?")
            time.sleep(60)
            set = bot.get_sticker_set('MexicanAxolotl')
            try:
                bot.send_sticker(debug_chat_id, random.choice(set.stickers).file_id)
                bot.send_sticker(vip_chat_id, random.choice(set.stickers).file_id)
            except telebot.apihelper.ApiException:
                print("My face is hidden behind a mask")
            except (ReadTimeout, socket.timeout, urllib3.exceptions.ReadTimeoutError):
                print("My face is hidden behind a mask. Elon Mask.")

