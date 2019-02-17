import telebot
from threading import Timer
import time

vip_chat_id = -1001145739506
fur_fur_fur_chat = -1001132289884
dlan_chat = -1001172376896

zrenki = [vip_chat_id, -1001345532965, fur_fur_fur_chat, dlan_chat, -1001117989911, -1001200533121]
day = 24 * 60 * 60


def zrena(args):
    bot = args[0]
    for chat in zrenki:
        try:
            bot.send_sticker(chat, 'CAADAgADtAADP_vRD1iCbwT85WNIAg')
            bot.send_message(chat, 'ХАЛЯВНЫЙ ЗАРЯД! ГО ПИЛИТЬ РАНДОМЩИКОВ!')
        except telebot.apihelper.ApiException:
            print("zreno to " + str(chat) + " failed")
    timer = Timer(day, zrena)
    timer.start()


def zrena_timers_init(bot):
    cur_time = time.localtime(time.time())
    mins = cur_time.tm_min
    sec = cur_time.tm_sec
    hours = cur_time.tm_hour
    tim = (day + 55 * 60 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena, [bot])
    timer.start()
    tim = (day + 5 * 60 + 9 * 3600 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena, [bot])
    timer.start()
    tim = (day + 5 * 60 + 19 * 3600 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena, [bot])
    timer.start()
    tim = (day + 5 * 60 + 14 * 3600 - hours * 3600 - mins * 60 - sec) % day
    timer = Timer(tim, zrena, [bot])
    timer.start()
