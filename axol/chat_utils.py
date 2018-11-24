import telebot

def send_stickers(self, chat, stickers, *args):
    if isinstance(stickers, list):
        for sticker in stickers:
            self.send_sticker(chat, sticker, *args)
    elif isinstance(stickers, str):
        self.send_sticker(chat, stickers, *args)



