# c790922c42f776cb
# http://www.name-prism.com/api_token/eth/json/[API_token]/Barack%20Obama
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
    def __init__(self):
        self.URL = "http://www.name-prism.com/api_token/eth/json/c790922c42f776cb/"
        self.infile = "all_people.csv"
        self.outfile = "all_people_ethnicity.csv"
        self.df_in = pd.read_csv(self.infile)
        self.SAVE_CHECKPOINT = 5
        self.df_sub = self.df_in 

        if os.path.exists(self.outfile):     
            try:
                df_out = pd.read_csv(self.outfile)
                self.df_sub = self.df_in[~self.df_in['name_id'].isin(df_out['name_id'])]
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
            name = row['person']
            print(f"{index}/{len(self.df_sub)} {row['person']}...")

            try:
                url = self.get_url(name)
                result = self.call(url)

                result['name_id'] = row['name_id']
                result['person'] = row['person']

                temp_df = pd.DataFrame(result, index=[0])
                all_df.append(temp_df)
            except:
                pass

            counter += 1
            if counter % self.SAVE_CHECKPOINT == 0: 
                self.save_to_file(all_df)
                all_df = []
        
        if len(all_df) > 0: self.save_to_file(all_df)

nprism = NamePrism()
nprism.get_ethnicities()