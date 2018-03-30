# -*- coding: utf-8 -*-
import time
import config
from argparse import Namespace

class Player:
    def __init__(self, user=None, task_status=0, last_task_time=0, last_task_mssg=0, task_completed=0, task=None,
                 task_id=[], informed=False, mess_from_bot=False, mess_sended=False, alpha=0.0,
                 new_year=False, ng_task_id=-1,
                 islove=False, love_task=None, pair=None, gnome_status=-1, message=None,
                 dura_status=0, dura_num=0, isdura=False, has_a_shield=False, can_get_a_shield=True):
        self.user = Namespace(**user) if isinstance(user, dict) else user
        self.task_status = task_status           # 0 - without task; 1 - in progress; 2 - failed.
        self.last_task_time = last_task_time     # time when last task had taken.
        self.last_task_mssg = last_task_mssg     # message when task had taken.
        self.message = Namespace(**message) if task else None
        self.task_completed = task_completed
        self.task = Namespace(**task) if task else None
        self.task_id = task_id
        self.informed = informed                 # Message about task expiration was sent in debug chat.
        self.mess_from_bot = mess_from_bot       # Subscribe for messages from bot
        self.mess_sended = mess_sended           # Message about taking new task was sent to player.
        self.new_year = new_year
        self.ng_task_id = ng_task_id
        self.islove = islove                     # Does player participate
        self.love_task = love_task
        self.pair = pair
        self.gnome_status = gnome_status
        self.alpha = alpha
        self.dura_status = dura_status
        self.dura_num = dura_num
        self.isdura = isdura
        self.has_a_shield = has_a_shield
        self.can_get_a_shield = can_get_a_shield
def to_string(self):
    res = str(self.user.first_name) + ' ' + str(self.user.last_name) + ' @' + str(self.user.username) + '\n'
    secs = time.time() - self.last_task_time
    res += 'Time: ' + str(secs // 3600) + 'h ' + str(secs // 60 % 60) + 'm ' + str(secs // 1 % 60) + 's\n'

    if self.task_completed < 100:
        tasks = config.tasks
    else:
        tasks = config.black_tasks

    if self.task_completed >= 150 and len(self.task_id):
        res += config.black_tasks[self.task_id[0]][1] + '\n'
        res += config.tasks[self.task_id[1]][1] + '\n'
    elif len(self.task_id):
        for idx in self.task_id:
            res += tasks[idx][1] + '\n'

    return res
