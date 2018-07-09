import config
from argparse import Namespace


class TaskSet:
    def __init__(self, tasks=[], modifier=None, message=None, status=0):
        self.tasks = tasks
        self.modifier = modifier
        self.message = Namespace(**message) if message else None
        self.status = status

    def get_task_time(self):
        return self.message.date

    def get_task_mess(self):
        return self.message.message_id


class Task:
    def __init__(self, task_type, id, required):
        self.type = task_type
        self.id = id

    def task_list(self):
        if self.type == 'normal':
            return config.tasks
        elif self.type == 'black':
            return config.black_tasks
        elif self.type == 'ng':
            return config.ng_tasks
        elif self.type == 'love':
            return config.love_tasks

    def to_text(self):
        return self.task_list(self.id[1])

