import os
import pandas as pd
import pandas.io.common

class FileHandler:
    def __init__(self, INIT_FILE, OUTFILE):
        self.df_in = pd.read_csv(INIT_FILE, dtype={"movie_id": str})
        self.outfile = OUTFILE
        self.df_sub = self.df_in
        if os.path.exists(OUTFILE):
            try:
                df_out = pd.read_csv(OUTFILE, encoding='utf-8')
                self.df_sub = self.df_in[~self.df_in['file'].isin(df_out['file'])]
            except pandas.errors.EmptyDataError:
                print("Warning: The output file is empty")
    
    def get_df(self):
        return self.df_sub
            
    def save_data(self, row):
        df = pd.DataFrame([row])
        
        df.to_csv(self.outfile, mode='a', header=not os.path.exists(self.outfile), index=False)