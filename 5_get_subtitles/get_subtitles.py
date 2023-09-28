import pandas as pd
import requests
import os

import sys
sys.path.append("../")

from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020
TARGETS = [CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020]

# check and create subtitles directory
if not os.path.exists("./subtitles"): os.mkdir("./subtitles")

# iterate over each sub-directory
for TARGET in TARGETS:
    df = pd.read_csv(f"../4_parse_xrays/parsed_xrays/{TARGET}_sub_movies_with_xrays.csv")
    # sdh = df[~df['sdh_sub_lang'].isnull()]

    # check and create the sub-directory, like com, in2010s, etc.
    if not os.path.exists(f"./subtitles/{TARGET}"): os.mkdir(f"./subtitles/{TARGET}")

    for index, row in df.iterrows():
        if not pd.isnull(row['sdh_sub_lang']):
            url = row["url"]
        elif not pd.isnull(row['en_url']):
            url = row['en_url']
        else:
            continue

        # check if the file directory exists
        directory = f"./subtitles/{TARGET}/{row['file']}"
        if not os.path.exists(directory): os.mkdir(directory)

        # the filename of the subtitle
        sub_file_name = f"./subtitles/{TARGET}/{row['file']}/{row['file']}.ttml2"
        # if the file exists, don't download and move forward
        if os.path.exists(sub_file_name): continue
        
        print(index, f"Downloading {row['file']}...")
        sub = requests.get(url)
        with open(sub_file_name, "wb") as f:
            f.write(sub.content) 