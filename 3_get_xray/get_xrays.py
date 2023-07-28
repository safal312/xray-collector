import sys
import os

sys.path.append('../')

import pandas as pd
import numpy as np

from AmazonPrimeScraper import Logger
from XrayScraper import XrayScraper

from utils.general import get_remaining_xrays

xscraper = XrayScraper(headless=False, workers=2)
lgr = Logger("log.txt")

df = pd.read_csv("./metadata_with_xray/com/meta_en_prime.csv", encoding='utf-8')
# get only entries that aren't already downloaded
extract_df = get_remaining_xrays(df)

xscraper.run_workers(extract_df, FOR="xrays")
