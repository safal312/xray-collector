import sys
import os

sys.path.append('../')

import pandas as pd
import numpy as np

from AmazonPrimeScraper import Logger
from XrayScraper import XrayScraper

from utils.general import extract_remaining

xscraper = XrayScraper(headless=False)
lgr = Logger("log.txt")

df = pd.read_csv("./missing_data/com/after2020/movies_paid.csv", encoding='utf-8')
# get only entries that aren't already downloaded
# extract_df = extract_remaining(df)

# xscraper.run_workers(extract_df, FOR="metadata")

driver = xscraper.get_driver()
xscraper.sign_in("https://www.amazon.com/gp/sign-in.html", driver)

for index, row in df.iterrows():
    print(index, row['link'])
    driver.get("https://www.amazon.com/" + row['link'])
    status = input("Is it unavailable or available? (0 or 1)")
    df.loc[index,'status'] = status

df.to_csv('./missing_data/com/checked_movies_paid.csv', index=False)
driver.quit()