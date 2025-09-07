import os
import sys
sys.path.append('../')

from AmazonPagesHandler import AmazonPagesHandler
from consts import ALL_LINKS_DIR, CLEAN_BASE_DIR, BEFORE_2010_DIR, IN_2010S,AFTER_2020

METADATA_DIR = "../data/2_metadata"
for TARGET_DIR in [BEFORE_2010_DIR]:

    if not os.path.exists(METADATA_DIR): os.mkdir(METADATA_DIR)
    if not os.path.exists(f"{METADATA_DIR}/{TARGET_DIR}"): os.mkdir(f"{METADATA_DIR}/{TARGET_DIR}")
    aph = AmazonPagesHandler(path=os.path.join(ALL_LINKS_DIR, TARGET_DIR), save_to=f"{METADATA_DIR}/{TARGET_DIR}/meta_en_prime.csv")
    aph.parse_files()