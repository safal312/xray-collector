import os
import csv

class UserInput:
    def __init__(self, export_file=None):
        """
        Class to handle the user input for the validation process.
    
        Args:
            export_file (str): Path to the file where the validated data will be saved.
        """
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
        """
        Handles the questions and user input for the validation process.

        Args:
            row (dict): A row from the dataframe.
        
        Returns:
            dict: The row with the user input.
        """
        res = dict(row)
        res['match'] = ''
        res['alt_id'] = ''
        res['notes'] = ''

        # print the movie details for validating
        print(f"Movie: {row['title']}, Year: {row['year']} imdbID: {row['movie_id']}")
        print("Description: ", row['synopsis'])
        
        try:
            # did the imdb ID collected match the movie shown on prime video?
            match = input("\nWas this a match? (0 or 1): ")
            match = int(match)
        except:
            print("Error in input, try again.")
        
        # if not a match
        if match == 0:
            response = self.handle_nonmatch()
            res['match'] = response[0]
            res['alt_id'] = response[1]
            res['notes'] = response[2]
        
        # if a match, just save the response
        if match == 1:
            response = self.handle_match()
            res['match'] = response[0]

        return res