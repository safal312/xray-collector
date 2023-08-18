import os
import sys
sys.path.append("../")

from utils.PrimeVideoPageHandler import PrimeVideoPageHandler
from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

# Change this to scrape different links
TARGET_DIR=AFTER_2020
if not os.path.exists(f"./parsed_metadata/{TARGET_DIR}"): os.mkdir(f"./parsed_metadata/{TARGET_DIR}")
pvph = PrimeVideoPageHandler(path=f"./metadata/{TARGET_DIR}", save_to=f"./parsed_metadata/{TARGET_DIR}/meta_en_prime.csv")
pvph.parse_files()