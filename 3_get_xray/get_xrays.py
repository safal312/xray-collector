import sys
import os

sys.path.append('../')

import pandas as pd
import numpy as np

from AmazonPrimeScraper import Logger
from XrayScraper import XrayScraper
from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

from utils.general import get_remaining_xrays

xscraper = XrayScraper(headless=False, workers=2)
lgr = Logger("log.txt")

TARGET_DIR = CLEAN_SCRAPE_DIR

METADATA_DIR = "../data/3_metadata_with_xray"

METAFILE = f"{METADATA_DIR}/{TARGET_DIR}/meta_en_prime.csv"
# METAFILE = f"./missing_data/{TARGET_DIR}/movies_without_xrays.csv"
# METAFILE = f"./missing_data/{TARGET_DIR}/movies_paid.csv"

df = pd.read_csv(METAFILE, encoding='utf-8')
df['fname'] = df['file'].str.replace(".html", "")

# get only entries that aren't already downloaded
PARENT_SAVE_DIR = f"../data/3_xrays"
if not os.path.exists(PARENT_SAVE_DIR): os.mkdir(PARENT_SAVE_DIR)

extract_df = get_remaining_xrays(df, TARGET_DIR, xray_dir=PARENT_SAVE_DIR)

xscraper.run_workers(df, FOR="xrays", SAVE_DIR=TARGET_DIR, PARENT_DIR=PARENT_SAVE_DIR)
