import pandas as pd
import os
import csv
import sys
sys.path.append("../")

from consts import CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

for TARGET_DIR in [CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020]:
    xrays_dir = f"../data/3_get_xray/xrays/{TARGET_DIR}"

    # i'm assuming that movies without any files are paid
    # 0 files could also mean that the video is tagged as not available in the location
    # and movies that only one playback resources are failures

    movies_without_xrays = []
    movies_paid = []

    files = os.listdir(xrays_dir)
    for dir in files:
        files = os.listdir(os.path.join(xrays_dir, dir))
        if len(files) < 2:
            if len(files) == 0: movies_paid.append(dir)
            if len(files) == 1: movies_without_xrays.append(dir)

    df = pd.read_csv(f"./metadata_with_xray/{TARGET_DIR}/meta_en_prime.csv")

    if not os.path.exists(f"missing_data/{TARGET_DIR}"): os.mkdir(f"missing_data/{TARGET_DIR}")
    mxdf = df[df['file'].str.replace(".html", "").isin(movies_without_xrays)]
    mxdf.to_csv(f"missing_data/{TARGET_DIR}/movies_without_xrays.csv", index=False)

    mpdf = df[df['file'].str.replace(".html", "").isin(movies_paid)]
    mpdf.to_csv(f"missing_data/{TARGET_DIR}/movies_paid.csv", index=False)