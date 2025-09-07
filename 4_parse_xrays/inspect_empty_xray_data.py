import os
import sys
sys.path.append("../")

from consts import CLEAN_BASE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

import pandas as pd
import pandas.io.common


people_counter = []
people_in_scenes_counter = []
both = []
df_temp = pd.DataFrame()

for DIR in [CLEAN_BASE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020]:
    TARGET_DIR = f"../data/4_parsed_xrays/{DIR}"

    for item in os.listdir(TARGET_DIR):
        if item.endswith(".csv"): continue
        people_path = os.path.join(TARGET_DIR, item, "people.csv")
        people_in_scenes_path = os.path.join(TARGET_DIR, item, "people_in_scenes.csv")
        
        PEOPLE = True
        if not os.path.exists(people_path): 
            PEOPLE = False
        elif os.stat(people_path).st_size <= 2:
            PEOPLE = False
        
        PEOPLE_IN_SCENES = True
        if not os.path.exists(people_in_scenes_path):
            PEOPLE_IN_SCENES = False
        elif os.stat(people_in_scenes_path).st_size <= 2:
            PEOPLE_IN_SCENES = False
        
        if not PEOPLE and not PEOPLE_IN_SCENES:
            both.append(item)
        else:
            if not PEOPLE:
                people_counter.append(item)
            if not PEOPLE_IN_SCENES:
                people_in_scenes_counter.append(item)

# Print instances where only people file is missing or empty but people_in_scenes is present
print("People: ", len(people_counter))
# Print instances where people_in_scenes file is missing or empty but people is present
print("People in scenes: ", len(people_in_scenes_counter))
# Print instances where both are missing or empty
print("Both: ", len(both))

print("People:")
print(people_counter)

print("People in scenes:")
print(people_in_scenes_counter)

print("Both:")
print(both)