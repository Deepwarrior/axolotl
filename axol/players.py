# -*- coding: utf-8 -*-
import time
import config
from argparse import Namespace
import task

class Player:
    def __init__(self, user=None, task_status=0, last_task_time=0, last_task_mssg=0, task_completed=0,
                 task_id=[], antitask_id=-1, informed=False, mess_from_bot=False, mess_sended=False, alpha=0.0,
                 new_year=False, ng_task_id=-1, last_mess=0,
                 islove=False, love_task=None, pair=None, gnome_status=-1, message=None,
                 dura_status=0, dura_num=0, isdura=False, has_a_shield=False, can_get_a_shield=True, dura_task=None,
                 dura_started=False, taskset=None, last_optional_task=0):
        self.love_task = None
        self.user = Namespace(**user) if isinstance(user, dict) else user
        self.task_completed = task_completed
        self.last_mess = last_mess
        self.informed = informed                 # Message about task expiration was sent in debug chat.
        self.mess_from_bot = mess_from_bot       # Subscribe for messages from bot
        self.mess_sended = mess_sended           # Message about taking new task was sent to player.
        self.new_year = new_year
        self.islove = islove                     # Does player participate
        self.pair = pair
        self.gnome_status = gnome_status
        self.alpha = alpha
        self.dura_status = dura_status
        self.dura_num = dura_num
        self.isdura = isdura
        self.has_a_shield = has_a_shield
        self.can_get_a_shield = can_get_a_shield
        self.dura_task = dura_task
        self.dura_started = dura_started
        self.taskset = task.TaskSet(**taskset) if taskset else task.TaskSet()
        self.last_optional_task = last_optional_task


def to_string(self):
    res = str(self.user.first_name) + ' ' + str(self.user.last_name) + ' @' + str(self.user.username) + '\n'
    secs = self.taskset.get_task_duration()
    res += 'Time: ' + str(secs // 3600) + 'h ' + str(secs // 60 % 60) + 'm ' + str(secs // 1 % 60) + 's\n'

    for task in self.taskset.tasks:
        if task.required:
            res += task.to_text() + '\n'

    if self.taskset.modifier != -1:
        res += config.anti_tasks[self.taskset.modifier] + '\n'

    return res
