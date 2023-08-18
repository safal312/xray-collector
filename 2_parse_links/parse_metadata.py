import os
import sys
sys.path.append('../')

from AmazonPagesHandler import AmazonPagesHandler
from consts import ALL_LINKS_DIR, CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S,AFTER_2020

TARGET_DIR = AFTER_2020

if not os.path.exists("./metadata"): os.mkdir("./metadata")
if not os.path.exists(f"./metadata/{TARGET_DIR}"): os.mkdir(f"./metadata/{TARGET_DIR}")
aph = AmazonPagesHandler(path=os.path.join("../", "1_get_links", ALL_LINKS_DIR, TARGET_DIR), save_to=f"./metadata/{TARGET_DIR}/meta_en_prime.csv")
aph.parse_files()