class task:
    def __init__(self, sticker, text, time, messages, func):
        self.sticker = sticker   #sticker id
        self.text = text         #task
        self.handler = func      #function for checking task processing
        self.time = time         #task duration
        self.messages = messages #task duration


