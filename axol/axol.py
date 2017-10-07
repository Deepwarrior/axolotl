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

bot = telebot.TeleBot(str(os.environ['TOKEN']))
active_players = []

vip_chat_id = -1001145739506
debug_chat_id = -1001107497089
igroklub_chat = -1001108031278
allow_chats = [vip_chat_id, debug_chat_id, -1001149068208, igroklub_chat]



def jsonDefault(object):
    return object.__dict__


# find and append players
def findplayer(user):
    for player in active_players:
        if player.user.id == user.id:
            return player
    player = players.Player(user)
    active_players.append(player)
    return player


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


@bot.message_handler(commands=["mess", "MESS"])
def axol_voice(message):
    if message.from_user.username in config.root:
        text = str(message.text[6:])
        if text:
            bot.send_message(vip_chat_id, text)


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
    bot.send_message(287819651, text)


@bot.message_handler(commands=["send"])
def send(message):
    text = str(message.text[6:])
    if not text:
        bot.send_message(message.chat.id, "НЕТ, НЕТ, НУЖНО ПИСАТЬ ПИСЬМО ПРОВЕРЯТОРАМ В ТОМ ЖЕ СООБЩЕНИИ, ЧТО И /send")
        return
    text = ': ' + text
    if message.from_user.last_name:
        text = message.from_user.last_name + text
    if message.from_user.first_name:
        text = message.from_user.first_name + ' ' + text
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
    bot.send_message(message.chat.id, "ТОП ПОЗОРА: \n1. ХАМПЕР\n2.САРАСТИ\n3. МАБА")


@bot.message_handler(commands=["top_sarasti"])
def sarasti(message):
    bot.send_message(message.chat.id, "ТОП САРАСТИ: \n1. САРАСТИ")


@bot.message_handler(commands=["my_task"])
def task_status(message):
    player = findplayer(message.from_user)
    answer = ""
    tm = 0
    if player.task_status == 1:
        if player.task_completed < 40:
            if hasattr(player, "task_id") and len(player.task_id):
                answer += config.tasks[player.task_id[0]][1] + "\n"
            else:
                answer += player.task.text + "\n"
        else:
            answer += ")))\n"
        if hasattr(player, "task_id") and len(player.task_id):
            for idx in player.task_id:
                task = config.tasks[idx]
                if (task[3] * 60 - ((time.time() - player.last_task_time) // 60)) > tm:
                    tm = task[3] * 60 - ((time.time() - player.last_task_time) // 60)
        elif player.task.time:
            tm = player.task.time * 60 - ((time.time() - player.last_task_time) // 60)
            if tm > 0:
                answer += "Осталось времени: " + str('{:.0f}'.format(tm // 60)) + " часов и " + \
                          str('{:.0f}'.format(tm % 60)) + " минут\n"
            else:
                answer += "ВЫПОЛНЯЙ, ПОКА НЕ ЗАСЧИТАЮТ!\n"
    answer += "Всего сделано: " + str(player.task_completed % 50) + ".\n"
    tm = config.seconds_in_day // 60 - ((time.time() - player.last_task_time) // 60)
    if tm > 0:
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
                player.task_status = 1
                player.last_task_time = time.time()
                player.last_task_mssg = message.message_id
                rand = random.randint(1, 500)
                if rand == 237:
                    task = ['CAADAgADaQADP_vRD78igQttLbufAg', 'КОЛДУЮ, КОЛДУЮ... ВЖУХ! И ТЫ ПИДОР ДНЯ.', 0, 0]
                    bot.send_sticker(message.chat.id, task[0])
                    bot.send_message(message.chat.id, task[1])
                else:
                    rand = random.randint(0, len(config.tasks) - 1)
                    task = config.tasks[rand]
                    player.task_id.append(rand)
                    bot.send_sticker(message.chat.id, task[0])
                    if player.task_completed < 40:
                        bot.send_message(message.chat.id, task[1])
                    else:
                        text = random.choice(["ТЫ УЖЕ БОЛЬШОЙ, САМ РАЗБЕРЕШЬСЯ", "<СПОЙЛЕРЫ>", "Я ПОЗАБЫЛ ВСЕ СЛОВА",
                                              "ЗДЕСЬ БЫЛО ЧТО-ТО ДЛИННОЕ ЕЩЁ"])
                        bot.send_message(message.chat.id, text)
                    player.informed = False
                    player.mess_sended = False
                    backup(None)
                    if player.task_completed >= 70:
                        bot.send_message(message.chat.id, "А ВОТ ЕЩЁ ТЕБЕ...")
                        rand = random.randint(1, len(config.tasks))
                        bot.send_sticker(message.chat.id, config.tasks[rand][0])
                        player.task_id.append(rand)


# root command. See all players with tasks.
@bot.message_handler(commands=["all_tasks"])
def all_tasks(message):
    if message.from_user.username in config.root:
        for player in active_players:
            if (player.task or (hasattr(player, "task_id") and len(player.task_id))) and player.task_status == 1:
                bot.send_message(message.chat.id, players.to_string(player))


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


def task_fail(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        if player.task_status == 1:
            player.task_status = 2
            bot.send_message(message.chat.id, "ЗАДАНИЕ ПРОВАЛЕНО!",
                             reply_to_message_id=message.reply_to_message.message_id)
            if player.mess_from_bot:
                bot.send_message(player.user.id, "К СОЖАЛЕНИЮ, ЗАДАНИЕ ПРОВАЛЕНО.")


def task_complete(reaction, message):
    if message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        if player.task_status == 1:
            player.task_status = 0
            player.task_completed += 1
            if player.task_completed == 50:
                bot.send_message(player.user.id, "АЗАЗА, ТЫ УМИР")
                bot.send_message(message.chat.id, "ЗАДАНИЕ ВЫПОЛНЕНО!\nВСЕГО СДЕЛАНО " + str(player.task_completed) +
                                 " ЗАДАНИЙ", reply_to_message_id=message.reply_to_message.message_id)
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
            if player.task_completed == 20:
                stick = random.choice(config.bonus_20)
                bot.send_message(player.user.id, "ПОЗДРАВЛЯЮ! \n МНОГО ЗАДАНИЙ УЖЕ СДЕЛАНО, НО МНОГО БУДЕТ И ВПЕРЕДИ \n"
                                                 " А ПОКА ТЫ ВЫИГРАЛ СЕКРЕТНЫЙ ДУРНИРНЫЙ СТИКЕР, ИСПОЛЬЗУЙ ЕГО С УМОМ")
                bot.send_sticker(player.user.id, stick)
            if player.task_completed == 60:
                bot.send_message(message.chat.id, "ТЕБЯ ВЕДЬ УЖЕ ОБНУЛИЛИ... ЗАЧЕМ ТЫ ПРОДОЛЖАЕШЬ ИХ ДЕЛАТЬ?")


def task_extra(reaction, message):
    if message.text == 'КЛАЦ!' and message.reply_to_message and message.from_user.username in config.root:
        player = findplayer(message.reply_to_message.from_user)
        player.task_completed += 1
        bot.send_message(message.chat.id, "ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ ВЫПОЛНЕНО!",
                         reply_to_message_id=message.reply_to_message.message_id)
        if player.task_completed == 20:
            stick = random.choice(config.bonus_20)
            bot.send_message(player.user.id, "ПОЗДРАВЛЯЮ! \n МНОГО ЗАДАНИЙ УЖЕ СДЕЛАНО, НО МНОГО БУДЕТ И ВПЕРЕДИ \n "
                                             "А ПОКА ТЫ ВЫИГРАЛ СЕКРЕТНЫЙ ДУРНИРНЫЙ СТИКЕР, ИСПОЛЬЗУЙ ЕГО С УМОМ")
            bot.send_sticker(player.user.id, stick)


def natalka(reaction, message):
    cur_time = time.localtime(time.time())
    minutes = cur_time.tm_min
    rand = random.randint(0, 4)
    if rand:
        text = 'НАТАЛЬЯ '
        if ((minutes + rand + 1) % 60) < 10:
            text += '0'
        text += str((minutes + rand + 1) % 60)
        bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)
    else:
        react(reaction, message)

reaction_funcs = [task_rework, task_fail, task_complete, task_extra, natalka]
    

def notify(message):
    for player in active_players:
        if player.task and not player.informed:
            if player.task.time:
                if time.time() - player.last_task_time > player.task.time * 3600:
                    player.informed = True
                    bot.send_message(debug_chat_id, players.to_string(player) + '\nВремя задания истекло! Оцените!')
            if player.task.messages:
                if message.message_id - player.last_task_mssg > player.task.messages:
                    player.informed = True
                    bot.send_message(debug_chat_id, players.to_string(player) + '\nВсе сообщения написаны! Оцените!')
        if player.mess_from_bot and not player.mess_sended \
                and time.time() - player.last_task_time > config.seconds_in_day:
            try:
                bot.send_message(player.user.id, "МОЖНО ВЗЯТЬ И СДЕЛАТЬ НОВОЕ ЗАДАНИЕ!")
            except telebot.apihelper.ApiException:
                player.mess_from_bot = False
            finally:
                player.mess_sended = True


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
    if message.chat.id == debug_chat_id:
        bot.send_message(debug_chat_id, message.sticker.file_id, reply_to_message_id=message.message_id)


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


if __name__ == '__main__':
    f = open('players.json', 'r')
    templist = json.load(f)
    for x in templist:
        active_players.append(players.Player(**x))
    f.close()
    random.seed()
    while True:
        try:
            bot.polling(none_stop=True)
        except ReadTimeout:
            print("die?")
            time.sleep(60)
        finally:
            backup(None)
