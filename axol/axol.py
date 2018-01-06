# -*- coding: utf-8 -*-
import config
import os
import telebot
import random
import players
import tasks
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
    tim = (day + 40 * 60 + 9 * 3600 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena)
    timer.start()
    tim = (day + 10 * 60 + 20 * 3600 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena)
    timer.start()
    tim = (day + 35 * 60 + 14 * 3600 - hours * 3600 - mins * 60 - sec) % day
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


root_log = ""


def logging(message):
    global root_log
    cur_time = time.localtime(time.time())
    root_log += str(cur_time.tm_hour) + ':' + str(cur_time.tm_min) + ' '
    root_log += message.from_user.username + ' сделал '
    if message.text:
        root_log += message.text + ' на '
    elif message.sticker:
        root_log += message.sticker.file_id + ' на '
    if message.reply_to_message:
        root_log += message.reply_to_message.from_user.username
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
    if message.left_chat_member.id in config.whitelist:
        bot.send_message(message.chat.id, "ОНЕТ!", reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, "ОУРА!", reply_to_message_id=message.message_id)


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
    bot.send_message(-1001246951967, text)


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

@bot.message_handler(commands=["femka"])
def femka(message):
    text = str(message.text[7:])
    if text.islower():
        text = text.upper()
    if not text or text == "rakon_bot":
        bot.send_message(message.chat.id, "ЭАЛЛО, СЛОВО-ТО НАПИШИ")
        return
    if " " in text:
        bot.send_message(message.chat.id, "Я ЧО, ПОХОЖ НА ПАТРИСИЮ? НАПИШИ ОДНО СЛОВО!")
        return

    if text.endswith("А") or text.endswith("Я"):
        bot.send_message(message.chat.id, "СЛОВО «" + text + "» ИДЕАЛЬНО!")

    if text.endswith("И") or text.endswith("Ы"):
        A = []
        w_len = len(text)
        for i in range(len(config.ends)):
           if i == 0 or i == 2 or i == 5:
               text = text[:w_len-1]
           else:
               text = str(message.text[7:])
           text = text + config.ends[i]
           text = text.upper()
           A.append(text)
        for i in A:
            bot.send_message(message.chat.id, i)
    else:
        A = []
        w_len = len(text)

        if text.endswith("К") or text.endswith("Г"):
            for i in range(len(config.ends)):
                if i == 1:
                    text = text[:w_len-1]
                    config.end[1] = "ЧКА"
                else:
                    text = str(message.text[7:])
                text = text + config.end[i]
                text = text.upper()
                A.append(text)
            for i in A:
                bot.send_message(message.chat.id, i)

        elif text.endswith("О") or text.endswith("Е") or text.endswith("У"):
            for i in range(len(config.ends)):
                if i == 0 or i == 2 or i == 5:
                    text = text[:w_len-1]
                else:
                    text = str(message.text[7:])
                text = text + config.end[i]
                text = text.upper()
                A.append(text)
            for i in A:
                bot.send_message(message.chat.id, i)

        elif text.endswith("Ь"):
            for i in range(len(config.ends)):
                if i == 2 or i == 4 or i == 5:
                    text = text[:w_len-1]
                else:
                    text = str(message.text[7:])
                text = text + config.end[i]
                text = text.upper()
                A.append(text)
            for i in A:
                bot.send_message(message.chat.id, i)
        else:
             for i in range(len(config.ends)):
                 text = text + config.end[i]
                 text = text.upper()
                 A.append(text)
                 text = str(message.text[7:])
             for i in A:
                 bot.send_message(message.chat.id, i)

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
                    answer += str(player.user.first_name) + '\t'
                if player.user.last_name:
                    answer += str(player.user.last_name) + '\t'
                if player.user.username:
                    answer += '@' + str(player.user.username) + '.\t'
                answer += 'Сделано:' + str(max_tasks) + '\n'
                top.append(player)
                break
    bot.send_message(message.chat.id, answer)


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
            if user and user.status in ["member", "creator", "administrator"] and not user.user.username == "rakon_bot" \
                    and not user.user.username == "uhi_official":
                text += str(i) + '. '
                if user.user.first_name:
                    text += str(user.user.first_name) + ' '
                if user.user.last_name:
                    text += str(user.user.last_name) + ' '
                if user.user.username:
                    text += '@' + str(user.user.username) + '.\t'
                text += '\n'
                i += 1
    bot.send_message(message.chat.id, text)


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
    bot.send_message(message.chat.id, answer)


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
                    backup(None)
                    if player.task_completed % 100 >= 70:
                        bot.send_message(message.chat.id, "А ВОТ ЕЩЁ ТЕБЕ...")
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
        logging(message)


def task_fail(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        if player.task_status == 1:
            player.task_status = 2
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
            player.task_completed += 1
            if player.task_completed == 50:
                bot.send_message(player.user.id, "АЗАЗА, ТЫ УМИР")
            if player.task_completed == 100:
                bot.send_message(player.user.id, "СГОРИ ДОТЛА! КАК И ВСЕ ТВОИ ОЧКИ")
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
                  "kick_misha": kick_misha}


def notify(message):
    for player in active_players:
        # if player.task and not player.informed:
        #    if player.task.time:
        #        if time.time() - player.last_task_time > player.task.time * 3600:
        #            player.informed = True
        #           bot.send_message(debug_chat_id, players.to_string(player) + '\nВремя задания истекло! Оцените!')
        #   if player.task.messages:
        #       if message.message_id - player.last_task_mssg > player.task.messages:
        #           player.informed = True
        #            bot.send_message(debug_chat_id, players.to_string(player) + '\nВсе сообщения написаны! Оцените!')
        if player.mess_from_bot and not player.mess_sended \
                and time.time() - player.last_task_time > config.seconds_in_day:
            try:
                bot.send_message(player.user.id, "МОЖНО ВЗЯТЬ И СДЕЛАТЬ НОВОЕ ЗАДАНИЕ!")
            except telebot.apihelper.ApiException:
                player.mess_from_bot = False
                print("notify failed.")
            finally:
                player.mess_sended = True


# def task_check(message):


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
    # task_check(message)


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
    # task_check(message)


@bot.message_handler(content_types=["voice"])
def voice_parsing(message):
    if message.chat.id == debug_chat_id:
        bot.send_message(message.chat.id, '\'' + message.voice.file_id + '\'', reply_to_message_id=message.message_id)


if __name__ == '__main__':
    f = open('players.json', 'r')
    templist = json.load(f)
    for x in templist:
        active_players.append(players.Player(**x))
        # try:
        #    print(x)
        # except UnicodeEncodeError:
        #    print("nohing!")
    f.close()
    zrena_timers_init()
    random.seed()
    # bot.send_sticker(debug_chat_id, 'CAADAgADMgADsjRGHiKRfQaAeEsnAg')
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
        finally:
            backup(None)
