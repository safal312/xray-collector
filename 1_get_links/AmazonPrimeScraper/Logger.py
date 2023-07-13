import os

class Logger():
    def __init__(self, log_location):
        self.loc = log_location

    def save_log(self, string):
        mode = 'a' if os.path.exists(self.loc) else 'w'

        with open(self.loc, mode) as f:
            f.write(string)