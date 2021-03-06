import config
from argparse import Namespace
import time
import random
import telebot

class TaskSet:
    def __init__(self, tasks=[], modifier=-1, message=None, status=0):
        self.tasks = [Task(**t) for t in tasks] if tasks else []
        self.modifier = modifier
        self.message = Namespace(**message) if message else None
        if message:
            self.message.chat = Namespace(**self.message.chat)
        self.status = status

    def get_task_duration(self):
        if self.message:
            return time.time() - self.message.date
        else:
            # TEMP
            return 99999999

    def get_task_mess(self):
        return self.message.message_id

    def clean(self):
        for task in self.tasks[:]:
            if task.required:
                self.tasks.remove(task)
        self.status = 0

    def new(self, task_type, req):
        self.tasks.append(Task(task_type, req))

    def check_normal(self):
        for task in self.tasks:
            if task.required:
                return True
        return False


class Task:
    def __init__(self, task_type, required, id=-1):
        self.task_type = task_type
        self.id = id if id != -1 else random.randint(0, len(self.task_list()) - 1)
        self.required = required

    def task_list(self):
        if self.task_type == 'normal':
            return config.tasks
        elif self.task_type == 'black':
            return config.black_tasks
        elif self.task_type == 'ng':
            return config.ng_tasks
        elif self.task_type == 'love':
            return config.love_tasks
        elif self.task_type == 'long':
            return config.long_tasks

    def to_text(self):
        return self.task_list()[self.id][1]

    def full_info(self):
        return self.task_list()[self.id]
