import config
import telebot
import random

bot = telebot.TeleBot(config.token)

random.seed(0)

@bot.message_handler(content_types=["sticker"])
def sticker_parsing(message): 
    if message.from_user.username == "Deepwarrior":
        bot.send_message(message.chat.id, "Hello creator")
    elif message.from_user.username == "random_answer":
        for w in config.hi_stickers[:]:
            if message.sticker.file_id == w:
                bot.send_message(message.chat.id, random.choice(config.hi_citrus))
    bot.send_message(message.chat.id, message.sticker.file_id)

@bot.message_handler(content_types=["text"])
def message_parsing(message):
    if message.text == '/get_task':
        task = random.choice(config.tasks)
        bot.send_sticker(message.chat.id, task[0])
        bot.send_message(message.chat.id, task[1])
    if message.text == 'МОЛОДЕЦ!':
        if message.reply_to_message:
            for w in config.root[:]:
                if message.from_user.username == w:
                    bot.send_message(message.chat.id, "ТЫ ВЫПОЛНИЛ ЗАДАНИЕ!", reply_to_message_id = message.reply_to_message.message_id)

if __name__ == '__main__':
    bot.polling(none_stop=True)