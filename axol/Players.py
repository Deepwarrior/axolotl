class Player_state :
    def __init__(self, id):
        self.id = id
        self.task_status = 0 #0 - without task; 1 - in progress; 2 - failed.
        self.last_task = 0 #time when last task had taken.
        self.task_completed = 0
