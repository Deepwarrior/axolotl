class Task:
    def __init__(self, sticker, text, time, messages, func=None):
        self.sticker = sticker    # sticker id
        self.text = text          # task
        self.time = time          # task duration in hours
        self.messages = messages  # task duration
        self.handler = func       # function for checking task processing
