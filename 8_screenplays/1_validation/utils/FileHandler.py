import pandas as pd

class FileHandler:
    def __init__(self, curr, fname):
        self.fname = fname
        self.df = pd.read_csv(self.fname, dtype={'imdb_id': str, 'alt_id': str})
        self.current = curr
        self.rows = self.df.shape[0]

    def get_link_next(self):
        if self.current < self.rows:
            row = self.df.loc[self.current]
            self.current += 1
            
            imdb_url = "https://imdb.com/title/tt" + str(row['imdb_id'])
            return (imdb_url, row['script_url']), row
        return None

    def reset_pointer(self):
        self.current = 0