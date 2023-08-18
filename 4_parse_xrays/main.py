import json
import os
import copy
import shutil
import sys
sys.path.append("../")

import pandas as pd

from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

TARGET_DIR = CLEAN_SCRAPE_DIR
xrays_dir = f"../3_get_xray/xrays/{TARGET_DIR}"
playback_file = "PlaybackResources.json"
xray_file = "Xray.json"

dirs = os.listdir(xrays_dir)

PARSED_DIR = f"./parsed_xrays/{TARGET_DIR}"
if not os.path.exists("./parsed_xrays"): os.mkdir("./parsed_xrays")

if not os.path.exists(PARSED_DIR):
    os.mkdir(PARSED_DIR)

# store all the metadata for each of the movies.
items_metadata = []

for dir in dirs:
    if len(os.listdir(os.path.join(xrays_dir, dir))) < 2:
        # shutil.rmtree(os.path.join(xrays_dir, dir))
        print(len(os.listdir(os.path.join(xrays_dir, dir))), dir)
        continue

    # print(f"Parsing Xray for {dir}...")
    pb_filepath = os.path.join(xrays_dir, dir, playback_file)
    xray_filepath = os.path.join(xrays_dir, dir, xray_file)

    folder_path = os.path.join(PARSED_DIR, dir)
    if os.path.exists(folder_path):
        # skipping already parsed content
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)
    
    # this section opens the playback resources file and collects necessary metadata for each of the movies.
    with open(pb_filepath, "r", errors="ignore") as f:
        pb_data = json.load(f)

        meta = {"file": dir}

        try:
            catalog = pb_data["catalogMetadata"]["catalog"]
            meta["title"] = catalog["title"]
            meta["entityType"] = catalog["entityType"]
            meta["runtimeSeconds"] = catalog["runtimeSeconds"]
            meta["synopsis"] = catalog["synopsis"]
            meta["rating_count"] = pb_data["catalogMetadata"]["reviews"]["rating"]["count"]
            meta["rating"] = pb_data["catalogMetadata"]["reviews"]["rating"]["value"]
        except:
            print("Error getting metadata for: ", dir)
        
        try:
            for sub in pb_data["subtitleUrls"]:
                if sub["languageCode"] == "en-us":
                    meta["en_type"] = sub["type"]
                    meta["en_url"] = sub["url"]
                
                if sub["type"] == "sdh":
                    meta["sdh_sub_lang"] = sub["languageCode"]
                    meta["url"] = sub["url"]
        except:
            print("Error getting subtitles for: ", dir)

        items_metadata.append(copy.deepcopy(meta))

    # this section gets necessary information from xray file
    with open(xray_filepath, "r", errors="ignore") as f:
        xray = json.load(f)

        # first we get all the scene information from the xray file
        scenes = []
        try:
            scene_list = xray["page"]["sections"]["center"]["widgets"]["widgetList"][0]["widgets"]["widgetList"][0]["widgets"]["widgetList"][0]["partitionedChangeList"]
            for scene in scene_list:
                item = {}
                item["scene"] = scene["initialItemIds"][0]
                item["start"] = scene["timeRange"]["startTime"]
                item["end"] = scene["timeRange"]["endTime"]

                scenes.append(item)
        except:
            print("Error getting the scene information: ", dir)

        # export the scenes file
        pd.DataFrame(scenes).to_csv(os.path.join(folder_path, "scenes.csv"), index=False)

        # this section stores information all actors in the movie
        all_chars = []
        try:
            people = xray["page"]["sections"]["center"]["widgets"]["widgetList"][0]["widgets"]["widgetList"][0]["widgets"]["widgetList"][1]["items"]

            for person in people:
                item = {}
                if person["item"]["blueprint"]["id"] == "XrayPersonItem":
                    item["id"] = person["id"]
                    item["person"] = person["item"]["textMap"]["PRIMARY"]
                    item["character"] = person["item"]["textMap"]["SECONDARY"]

                    all_chars.append(item)
        except:
            print("Error getting all characters information: ", dir)
        # store the people information
        pd.DataFrame(all_chars).to_csv(os.path.join(folder_path, "people.csv"), index=False)

        # This section is for the people who are involved in each of the scenes
        chars_in_scenes = []
        try:
            all_chars_timestamped = xray["page"]["sections"]["center"]["widgets"]["widgetList"][0]["widgets"]["widgetList"][0]["widgets"]["widgetList"][1]["partitionedChangeList"]

            for index, scene in enumerate(all_chars_timestamped):
                item = {}
                # the number of scenes seem to match the partitionedchangeList
                # so we can assume that it has a one to one mapping
                # the start and end times are also there to verify
                item["scene"] = "/xray/scene/" + str(index + 1)
                item["start"] = scene["timeRange"]["startTime"]
                item["end"] = scene["timeRange"]["endTime"]

                # filter names
                scene["changesCollection"] = list(filter(lambda entry: "/name" in entry["itemId"], scene["changesCollection"]))

                if len(scene["changesCollection"]) == 0:
                    chars_in_scenes.append(item)
                    continue

                for person in scene["changesCollection"]:
                    item["person_id"] = person["itemId"]
                    item["timestamp"] = person["timePosition"]
                    
                    chars_in_scenes.append(copy.deepcopy(item))  
        except:
            print("Error getting timestamped scene with characters: ", dir)
        # store the characters in different scenes
        pd.DataFrame(chars_in_scenes).to_csv(os.path.join(folder_path, "people_in_scenes.csv"), index=False)

# finally output the items metadata
pd.DataFrame(items_metadata).to_csv(os.path.join(PARSED_DIR, "movies_with_xrays.csv"), index=False)