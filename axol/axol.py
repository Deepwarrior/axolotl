import config
import telebot
import random
import Players

bot = telebot.TeleBot(config.token)
active_players = []

@bot.message_handler(content_types=["sticker"])
def sticker_parsing(message): 
    if message.from_user.username == "Deepwarrior":
        bot.send_message(message.chat.id, "#РОЧИТАЛЕСЬАТ")
    elif message.from_user.username == "random_answer":
        for w in config.hi_stickers[:]:
            if message.sticker.file_id == w:
                bot.send_message(message.chat.id, random.choice(config.hi_citrus))
    bot.send_message(message.chat.id, message.sticker.file_id)

#find and append players
def findplayer(id):
     for w in active_players[:]:
        if w.id == id:
            return w
     player = Players.Player_state(id)
     active_players.append(player)
     return player

#collect players and give them tasks
@bot.message_handler(commands=["get_task"])
def task_send(message):
    player = findplayer(message.from_user.id)
    if player.task_status == 1:
        bot.send_message(message.chat.id, "ТЫ УЖЕ ЧТО-ТО ДЕЛАЕШЬ!", reply_to_message_id = message.message_id)
    elif player.task_status == 2:
        bot.send_message(message.chat.id, "ТЫ УЖЕ НЕ СМОГ!", reply_to_message_id = message.message_id)
    elif player.task_status == 0:
        player.task_status = 1
        task = random.choice(config.tasks)
        bot.send_sticker(message.chat.id, task[0])
        bot.send_message(message.chat.id, task[1])

@bot.message_handler(content_types=["text"])
def message_parsing(message):
    if message.text == 'МОЛОДЕЦ!':
        if message.reply_to_message:
            for w in config.root[:]:
                if message.from_user.username == w:
                    player = findplayer(message.reply_to_message.from_user.id)
                    if player.task_status == 1:
                        player.task_status = 0
                        player.task_completed += 1
                        bot.send_message(message.chat.id, "ЗАДАНИЕ ВЫПОЛНЕНО!\nВСЕГО СДЕЛАНО " + str(player.task_completed) + " ЗАДАНИЙ", reply_to_message_id = message.reply_to_message.message_id)
    if message.text == 'ТЫ ДУРА?':
        if message.reply_to_message:
            for w in config.root[:]:
                if message.from_user.username == w:
                    bot.send_message(message.chat.id, "ЗАДАНИЕ ПРОВАЛЕНО!", reply_to_message_id = message.reply_to_message.message_id)  
                    player = findplayer(message.reply_to_message.from_user.id)
                    player.task_status = 2
                    

if __name__ == '__main__':
    random.seed()
    bot.polling(none_stop=True)