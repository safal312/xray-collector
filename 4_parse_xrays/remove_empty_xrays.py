import os
import sys
sys.path.append("../")

from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

import pandas as pd

for TARGET_DIR in [CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020]:
    df_target = pd.read_csv(f"../data/4_parsed_xrays/{TARGET_DIR}/movies_with_xrays.csv")

    target_path = f"../data/4_parsed_xrays/{TARGET_DIR}"
    empty_xrays = []
    for movie in os.listdir(target_path):
        if ".csv" in movie: continue
        
        people = os.path.join(target_path, movie, "people.csv") 
        # condition if the file is not present, this could mean xray file is not extracted or available
        if not os.path.exists(people):
            empty_xrays.append(movie)
            continue

        # condition if file is empty: this means that timestampped info is not present
        if os.stat(people).st_size <= 2:
            empty_xrays.append(movie)
            
    sub_df = df_target[~df_target['file'].isin(empty_xrays)]

    sub_df.to_csv(f"../data/4_parsed_xrays/{TARGET_DIR}_sub_movies_with_xrays.csv", index=False)