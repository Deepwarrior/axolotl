# -*- coding: utf-8 -*-
import time
import config
from argparse import Namespace

class Player:
    def __init__(self, user=None, task_status=0, last_task_time=0, last_task_mssg=0, task_completed=0, task=None,
                 task_id=[], informed=False, mess_from_bot=False, mess_sended=False):
        self.user = Namespace(**user) if isinstance(user, dict) else user
        self.task_status = task_status           # 0 - without task; 1 - in progress; 2 - failed.
        self.last_task_time = last_task_time     # time when last task had taken.
        self.last_task_mssg = last_task_mssg     # message when task had taken.
        self.task_completed = task_completed
        self.task = Namespace(**task) if task else None
        self.task_id = task_id
        self.informed = informed                 # Message about task expiration was sent in debug chat.
        self.mess_from_bot = mess_from_bot       # Subscribe for messages from bot
        self.mess_sended = mess_sended           # Message about taking new task was sent to player.


def to_string(self):
    res = str(self.user.first_name) + ' ' + str(self.user.last_name) + ' @' + str(self.user.username) + '\n'
    secs = time.time() - self.last_task_time
    res += 'Time: ' + str(secs // 3600) + 'h ' + str(secs // 60 % 60) + 'm ' + str(secs // 1 % 60) + 's\n'

    if hasattr(self, "task_id") and len(self.task_id):
        for idx in self.task_id:
            res += config.tasks[idx][1] + '\n'
    elif self.task:
        res += self.task.text + '\n'
    return res
