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

df = pd.read_csv("../2_parse_links/metadata/com/clean_meta_en_prime.csv", encoding='utf-8')
# get only entries that aren't already downloaded
extract_df = extract_remaining(df)

xscraper.run_workers(extract_df, FOR="metadata")