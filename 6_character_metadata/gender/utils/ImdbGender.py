import csv
import os
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import pandas.io.common
from selenium.webdriver.common.by import By

class ImdbGender:
    def __init__(self, scraper=None):
        self.WORKERS = 3
        self.URL = "https://www.imdb.com/name/"
        self.scraper = scraper

        self.infile = "../all_people.csv"
        self.outfile = "all_people_gender.csv"
        self.df_in = pd.read_csv(self.infile, encoding_errors='ignore')
        self.SAVE_CHECKPOINT = 50
        self.df_sub = self.df_in 

        if os.path.exists(self.outfile):     
            try:
                df_out = pd.read_csv(self.outfile, encoding='utf-8',  encoding_errors='ignore')
                self.df_sub = self.df_in[~self.df_in['name_id'].isin(df_out['name_id'])]
            except pandas.errors.EmptyDataError:
                print("Warning: The output file is empty")
    
    def write_to_file(self, new_rows):
        with open(self.outfile, "a", newline='') as file:
            writer = csv.writer(file)
            # writer.writerow(['id','person','character','movie','name_id','gender'])

            writer.writerows(new_rows)
    
    def scrape_metadata(self, df, driver, lock):
        counter = 0
        new_rows = []
        for index, row in df.iterrows():
            name_id = row['name_id']
            driver.get(self.URL + str(name_id))
            print(f"{index}/{len(self.df_sub)} {row['person']}...")

            try:
                attributes = driver.find_element(By.XPATH, "//h1[@data-testid='hero__pageTitle']/following-sibling::ul")
                lis = attributes.find_elements(By.TAG_NAME, "li")
                texts = [li.text for li in lis]
            except:
                texts = []

            nr = list(row)
            nr.append('/'.join(texts))

            new_rows.append(nr)
            counter += 1
            if counter % self.SAVE_CHECKPOINT == 0: 
                with lock:
                    self.write_to_file(new_rows)
                    new_rows = []
        
        if len(new_rows) > 0:
            with lock:
                self.write_to_file(new_rows)
    
    def scrape_concurrent(self, WORKERS=3):
        self.WORKERS = WORKERS
        lock = Lock()

        files = np.array_split(self.df_sub, WORKERS)
        drivers = [self.scraper.get_driver() for _ in range(WORKERS)]

        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            handler = self.scrape_metadata
            executor.map(handler, files, drivers, [lock] * WORKERS)