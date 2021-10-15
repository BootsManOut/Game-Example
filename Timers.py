import time

class Timer():
    def __init__(self,Duration):
        self.StartTime=time.time()
        self.Duration=Duration
        self.running=True
    def IsExpired(self):
        if time.time()-self.StartTime >= self.Duration and self.running:
            self.running=False
            return True
    def Start(self,Duration):
        self.StartTime=time.time()
        self.Duration=Duration
        self.running=True