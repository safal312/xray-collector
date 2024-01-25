import os
import sys
sys.path.append("../")

from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

import pandas as pd
import pandas.io.common


counter = 0
df_temp = pd.DataFrame()

for DIR in [CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020]:
    TARGET_DIR = f"../4_parse_xrays/parsed_xrays/{DIR}"

    for item in os.listdir(TARGET_DIR):
        # print(item)
        if item.endswith(".csv"): continue
        people_path = os.path.join(TARGET_DIR, item, "people.csv")
        if not os.path.exists(people_path): 
            counter += 1
            continue
        
        try:
            df = pd.read_csv(people_path, encoding='utf-8')
            df['movie'] = item
            df['name_id'] = df['id'].str.extract(r'(nm[0-9]+)', expand=False)
            df_temp = pd.concat([df_temp, df])
        except pandas.errors.EmptyDataError:
            counter += 1
            print(counter)

# there are 207 missing people.csv files, but only 198 missing people_in_scenes.csv
print("Missing Xray data: ", counter)
# df_temp.to_csv("all_people_with_duplicates.csv", index=False)
# df_temp = df_temp[~df_temp['name_id'].duplicated()]
# df_temp.to_csv("all_people.csv", index=False)
    # print(item, len(df))