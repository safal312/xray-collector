import sys
import os

sys.path.append('../')

import pandas as pd
import numpy as np

from XrayScraper import XrayScraper
from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

from utils.general import extract_remaining

xscraper = XrayScraper(headless=False, workers=2)

# change the target dir to scrape different links
TARGET_DIR = AFTER_2020

# check if the storage location exists, if not create it
METADATA_DIR = "../data/3_metadata"
if not os.path.exists(os.path.join(METADATA_DIR, TARGET_DIR)): os.mkdir(os.path.join(METADATA_DIR, TARGET_DIR))

PARSED_LINKS = f"../data/2_metadata/{TARGET_DIR}/sub_clean_meta_en_prime.csv"
df = pd.read_csv(PARSED_LINKS, encoding='utf-8')
# get only entries that aren't already downloaded
extract_df = extract_remaining(df, TARGET_DIR)
# check = pd.read_csv("check.csv")
# extract_df = df[df['fname'].isin(check['file'].str.replace(".html", ""))]

xscraper.run_workers(extract_df, FOR="metadata", SAVE_DIR=TARGET_DIR)