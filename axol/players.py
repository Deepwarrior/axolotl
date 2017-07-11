# -*- coding: utf-8 -*-
import time

class Player_state :
    def __init__(self, user):
        self.user = user
        self.task_status = 0 #0 - without task; 1 - in progress; 2 - failed.
        self.last_task_time = 0 #time when last task had taken.
        self.last_task_mssg = 0 #message when task had taken.
        self.task_completed = 0
        self.task = None
        self.informed = False

def to_string(self):
    res = str(self.user.first_name) + ' ' + str(self.user.last_name) + ' @' + str(self.user.username) + '\n'
    secs = time.time() - self.last_task_time
    res += 'Time: ' + str(secs // 3600) +'h ' + str(secs // 60 % 60) +'m ' + str(secs // 1 % 60) +'s\n'
    res += self.task.text
    return res
