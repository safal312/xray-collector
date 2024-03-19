import os
import csv

class UserInput:
    def __init__(self, exportf):
        self.exportf = exportf
    
    def get_current_position(self):
        try:
            with open(self.exportf, 'r') as f:
                lines = f.readlines()
                return len(lines)
        except:
            return 0
    
    def handle_match(self):
        return (1, '', '')

    def handle_nonmatch(self):
        try:
            alt_id = input("Alternative IDs:")
            notes = input("Any notes? ")
            return (0, alt_id, notes)
        except:
            print("Error in inputting alternative id")

    def save_response(self, response, row):
        mode = 'w' if not os.path.exists(self.exportf) else 'a'

        rowc = row.copy()

        with open(self.exportf, mode, newline='') as f:
            writer = csv.writer(f)
            
            rowc['match'] = response[0]
            rowc['alt_id'] = response[1]
            rowc['notes'] = response[2]
            
            writer.writerow(rowc)

    def ask_assessment(self, row):
        try:
            match = input("Was this a match?: ")
            match = int(match)
        except:
            print("Error in input, try again.")
        
        response = ''
        if match == 0:
            response = self.handle_nonmatch()
        
        if match == 1:
            response = self.handle_match()

        self.save_response(response, row)

        return response