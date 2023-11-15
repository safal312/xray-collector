import os
import csv

class UserInput:
    def __init__(self, init_file=None, export_file=None):
        self.outfile = export_file
    
    def handle_match(self):
        return (1, '', '')

    def handle_nonmatch(self):
        try:
            alt_id = input("Alternative IDs:")
            notes = input("Any notes? ")
            return (0, alt_id, notes)
        except:
            print("Error in inputting alternative id")

    def ask_assessment(self, row):
        res = dict(row)
        res['match'] = ''
        res['alt_id'] = ''
        res['notes'] = ''

        print(f"Movie: {row['title']}, Year: {row['year']} imdbID: {row['movie_id']}")
        print("Description: ", row['synopsis'])
        
        try:
            match = input("\nWas this a match?: ")
            match = int(match)
        except:
            print("Error in input, try again.")
        
        if match == 0:
            response = self.handle_nonmatch()
            res['match'] = response[0]
            res['alt_id'] = response[1]
            res['notes'] = response[2]
        
        if match == 1:
            response = self.handle_match()
            res['match'] = response[0]
        # self.save_response(response, row)

        return res