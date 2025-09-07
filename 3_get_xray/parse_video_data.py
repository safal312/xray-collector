import os
import sys
sys.path.append("../")

from utils.PrimeVideoPageHandler import PrimeVideoPageHandler
from consts import CLEAN_BASE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

# Change this to collect for different batches
for TARGET_DIR in [CLEAN_BASE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020]:
    print("Collecting for:", TARGET_DIR)
    HTML_FILES_DIR = "../data/3_metadata_movie_pages"
    PARSED_METADATA_DIR = "../data/3_metadata_movie_pages_parsed"
    if not os.path.exists(PARSED_METADATA_DIR): os.mkdir(PARSED_METADATA_DIR)

    if not os.path.exists(f"{PARSED_METADATA_DIR}/{TARGET_DIR}"): os.mkdir(f"{PARSED_METADATA_DIR}/{TARGET_DIR}")
    pvph = PrimeVideoPageHandler(path=f"{HTML_FILES_DIR}/{TARGET_DIR}", save_to=f"{PARSED_METADATA_DIR}/{TARGET_DIR}/meta_en_prime.csv")
    pvph.parse_files()