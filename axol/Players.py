# -*- coding: utf-8 -*-
import time

class Player_state :
    def __init__(self, user):
        self.user = user
        self.task_status = 0 #0 - without task; 1 - in progress; 2 - failed.
        self.last_task = 0 #time when last task had taken.
        self.task_completed = 0

    def to_string(self):
        res = self.user.first_name + ' ' + self.user.last_name + ' @' + self.user.username + '\n'
        secs = time.time() - self.last_task
        res += 'Time: ' + str(secs // 3600) +'h ' + str(secs // 60 % 60) +'m ' + str(secs // 1 % 60) +'s'
        #add current task name.
        return res
