import os
import pandas as pd
import pandas.io.common

class FileHandler:
    def __init__(self, INIT_FILE, OUTFILE):
        """
        Class to handle the file operations for the validation process.
        Gets remaining movies to be validated. Also helps saving the data.

        Args:
            INIT_FILE (str): Path to the file containing the initial data.
            OUTFILE (str): Path to the file where the validated data will be saved.
        """
        self.df_in = pd.read_csv(INIT_FILE, dtype={"imdb_id": str})
        self.outfile = OUTFILE
        self.df_sub = self.df_in
        if os.path.exists(OUTFILE):
            try:
                df_out = pd.read_csv(OUTFILE, encoding='utf-8')
                self.df_sub = self.df_in[~self.df_in['file'].isin(df_out['file'])]
            except pandas.errors.EmptyDataError:
                print("Warning: The output file is empty")
    
    def get_df(self):
        """
        Returns the movies with missing imdb IDs to be validated.
        """
        self.df_sub = self.df_sub[self.df_sub['imdb_id'].isnull()]
        return self.df_sub
            
    def save_data(self, row):
        """
        Appends the validated data to the output file.
        """

        df = pd.DataFrame([row])
        
        df.to_csv(self.outfile, mode='a', header=not os.path.exists(self.outfile), index=False)