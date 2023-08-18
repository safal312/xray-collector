import os
import csv

class Logger():
    def __init__(self, log_location):
        self.loc = log_location

    def save_log(self, strings_list):
        if type(strings_list) == 'str': strings_list = [strings_list]
        
        mode = 'a' if os.path.exists(self.loc) else 'w'

        with open(self.loc, mode) as f:
            writer = csv.writer(f)
            writer.writerow(strings_list)
            # f.write(string + "\n")