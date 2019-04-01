import config


def femka_init(bot):
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
