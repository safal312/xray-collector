import sys
import os

sys.path.append('../')

import pandas as pd
import numpy as np

from AmazonPrimeScraper import Logger
from XrayScraper import XrayScraper
from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

from utils.general import extract_remaining

xscraper = XrayScraper(headless=False, workers=2)
lgr = Logger("log.txt")

# change the target dir to scrape different links
TARGET_DIR = AFTER_2020

# check if the storage location exists, if not create it
if not os.path.exists(os.path.join("./metadata", TARGET_DIR)): os.mkdir(os.path.join("./metadata", TARGET_DIR))

df = pd.read_csv(f"../2_parse_links/metadata/{TARGET_DIR}/sub_clean_meta_en_prime.csv", encoding='utf-8')
# get only entries that aren't already downloaded
extract_df = extract_remaining(df, TARGET_DIR)
# check = pd.read_csv("check.csv")
# extract_df = df[df['fname'].isin(check['file'].str.replace(".html", ""))]

xscraper.run_workers(extract_df, FOR="metadata", SAVE_DIR=TARGET_DIR)