import config
import telebot

vip_chat_id = -1001145739506
debug_chat_id = -1001107497089
igroklub_chat = -1001108031278


def mail_init(bot):
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
            mess = text.split(' ', 1)
            try:
                chat = int(mess[0])
                bot.send_message(chat, mess[1])
            except (ValueError, telebot.apihelper.ApiException):
                bot.send_message(vip_chat_id, text)

    @bot.message_handler(commands=["SAVE", "save"])
    def save(message):
        if message.from_user.username in config.root and message.reply_to_message:
            bot.forward_message(debug_chat_id, message.chat.id, message.reply_to_message.message_id)
            # logging(message)

    @bot.message_handler(commands=["fwd", "FWD"])
    def fwd(message):
        if message.from_user.username in config.root and message.reply_to_message:
            text = str(message.text[5:])
            try:
                chat = int(text)
                bot.forward_message(chat, message.chat.id, message.reply_to_message.message_id)
            except (ValueError, telebot.apihelper.ApiException):
                bot.forward_message(vip_chat_id, message.chat.id, message.reply_to_message.message_id)
                # logging(message)

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
            bot.send_message(-1001479011046, text)
        except telebot.apihelper.ApiException:
            bot.send_message(debug_chat_id, text)
