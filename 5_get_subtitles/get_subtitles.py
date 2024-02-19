import pandas as pd
import requests
import os

import sys
sys.path.append("../")

from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020
TARGETS = [CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020]

# check and create subtitles directory
SUBTITLES_DIR = "../data/5_subtitles/"
if not os.path.exists(SUBTITLES_DIR): os.mkdir(SUBTITLES_DIR)
if not os.path.exists(SUBTITLES_DIR + "/subtitles"): os.mkdir(SUBTITLES_DIR + "/subtitles")

rows = []

# iterate over each sub-directory
for TARGET in TARGETS:
    df = pd.read_csv(f"../data/4_parsed_xrays/{TARGET}_sub_movies_with_xrays.csv")

    # check and create the sub-directory, like com, in2010s, etc.
    if not os.path.exists(f"{SUBTITLES_DIR}/subtitles/{TARGET}"): os.mkdir(f"{SUBTITLES_DIR}/subtitles/{TARGET}")

    for index, row in df.iterrows():
        temp_r = dict(row.copy())
        
        temp_r['subtitle'] = None
        # first we check if SDH-type subtitle is present, we download it if available
        # else we try to get the subtitle in English 
        # note: there were cases where we got SDH in a non-English language. In such cases, the SDH and the english subtitle are both downloaded 
        if not pd.isnull(row['sdh_sub_lang']):
            url = row["url"]
            temp_r['subtitle'] = 'SDH'
        elif not pd.isnull(row['en_url']):
            url = row['en_url']
            temp_r['subtitle'] = 'EN'
        
        if temp_r['subtitle'] is None:
            rows.append(temp_r)
            continue
        
        # check if the movie directory exists
        directory = f"{SUBTITLES_DIR}/subtitles/{TARGET}/{row['file']}"
        if not os.path.exists(directory): os.mkdir(directory)
        
        sub_file_name = f"{SUBTITLES_DIR}/subtitles/{TARGET}/{row['file']}/{row['file']}.ttml2"

        print(index, f"Downloading {row['file']}...")
        
        # the subtitle is SDH, we first download it then we check if it is in english or not
        # if SDH not in english, we download the english version as well
        if temp_r['subtitle'] == 'SDH':
            # download the SDH file
            sub = requests.get(url)
            with open(sub_file_name, "wb") as f:
                f.write(sub.content)

            # if the SDH subtitle language is not english, try looking for an english subtitle
            if 'en-' not in row['sdh_sub_lang']:
                sub_file_name = f"{SUBTITLES_DIR}/subtitles/{TARGET}/{row['file']}/{row['file']}_en.ttml2"
                
                # if the english URL exists
                if not pd.isnull(row['en_url']):
                    temp_r['subtitle'] = 'SDH_EN'
                    url = row['en_url']
                else:
                    rows.append(temp_r)
                    continue
        
        rows.append(temp_r)
        # if the file exists, don't download and move forward
        if os.path.exists(sub_file_name): continue
        
        
        # download the english subtitle if it's the only one present or if SDH is not in English
        if temp_r['subtitle'] == 'SDH_EN' or temp_r['subtitle'] == 'EN':
            sub = requests.get(url)
            with open(sub_file_name, "wb") as f:
                f.write(sub.content) 

pd.DataFrame(rows).to_csv(f"{SUBTITLES_DIR}/subtitles_collected.csv", index=False)