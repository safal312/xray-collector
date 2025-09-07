import os
import sys
sys.path.append("../")

from consts import CLEAN_BASE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

import pandas as pd
import pandas.io.common

counter = 0
df_temp = pd.DataFrame()

SAVE_DIR = "../data/6_character_metadata"
if not os.path.exists(SAVE_DIR): os.mkdir(SAVE_DIR) 

for DIR in [CLEAN_BASE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020]:
    TARGET_DIR = f"../data/4_parsed_xrays/"
    df_meta = pd.read_csv(f"{TARGET_DIR}/{DIR}_sub_movies_with_xrays.csv")

    for index, row in df_meta.iterrows():
        item = row['file']

        people_path = os.path.join(TARGET_DIR, DIR, item, "people.csv")
        if not os.path.exists(people_path):
            print("path doesn't exist")
            counter += 1
            continue
        
        try:
            df = pd.read_csv(people_path, encoding='utf-8')
            df['file'] = item
            df_temp = pd.concat([df_temp, df])
        except pandas.errors.EmptyDataError:
            print("empty data error")
            counter += 1

print("Missing Xray data: ", counter)
# Save the file with duplicates so we have all the people in every movie
# We have 207 missing files so it reduces the actual movie number to 3567
df_temp.to_csv(f"{SAVE_DIR}/all_people_with_duplicates.csv", index=False)

# Remove duplicates based on name_id
df_temp = df_temp[~df_temp['name_id'].duplicated()]
df_temp.to_csv(f"{SAVE_DIR}/all_people.csv", index=False)