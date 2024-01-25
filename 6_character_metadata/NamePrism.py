import os
import re
import requests
import json
import asyncio
import pandas as pd
import pandas.io.common
from unidecode import unidecode
from ratelimit import limits, sleep_and_retry

class NamePrism:
    def __init__(self, token, infile, outfile, name_id="name_id", name_col="person"):
        """
        token (str): API token
        infile (str): input file with names and unique name IDs
        outfile (str): File to save to
        name_id (str): Column name of unique name IDs
        name_col (str): Column name of people names
        """
        self.URL = f"http://www.name-prism.com/api_token/eth/json/{token}/"
        self.infile = infile
        self.outfile = outfile
        self.person_id = name_id
        self.name_col = name_col

        self.SAVE_CHECKPOINT = 5
        
        self.df_in = pd.read_csv(self.infile, dtype={self.person_id: str})
        self.df_sub = self.df_in

        if os.path.exists(self.outfile):     
            try:
                df_out = pd.read_csv(self.outfile, dtype={self.person_id: str})
                self.df_sub = self.df_in[~self.df_in[self.person_id].isin(df_out[self.person_id])]
            except pandas.errors.EmptyDataError:
                print("Warning: The output file is empty")
    
    @sleep_and_retry
    @limits(calls=59, period=60)
    def call(self, url):
        response = requests.get(url)
        return response.json()
    
    def get_url(self, name):
        name = unidecode(name)
        name = re.sub("[/-]", "", name)

        return self.URL + name

    def save_to_file(self, all_df):
        out_df = pd.concat(all_df)

        header = False
        if not os.path.exists(self.outfile):
            header = True
        else:
            if len(self.outfile) == 0: header = True
            
        out_df.to_csv(self.outfile, mode='a', index=False, header=header)

    def get_ethnicities(self):
        counter = 0
        all_df = []
        for index, row in self.df_sub.iterrows():
            name = row[self.name_col]
            print(f"{index}/{len(self.df_sub)} {row[self.name_col]}...")

            try:
                url = self.get_url(name)
                result = self.call(url)
                
                # check if the person id starts with nm or not
                result[self.person_id] = row[self.person_id]
                result[self.name_col] = row[self.name_col]

                temp_df = pd.DataFrame(result, index=[0])
                all_df.append(temp_df)
            except:
                pass

            counter += 1
            if counter % self.SAVE_CHECKPOINT == 0: 
                self.save_to_file(all_df)
                all_df = []
        
        if len(all_df) > 0: self.save_to_file(all_df)
