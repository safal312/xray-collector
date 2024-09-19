import os
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import pandas.io.common
from imdb import Cinemagoer

ia = Cinemagoer()

METADATA_DIR = "../data/6_character_metadata"

# you need all people with duplicates because if you remove the duplicates, you won't get all characters from each movie when subsetting
all_people = pd.read_csv(f"{METADATA_DIR}/all_people_with_duplicates.csv")
df_in = pd.read_csv(f"{METADATA_DIR}/movies_with_cast_manual.csv")
df_in = df_in[~df_in['title'].isna()]

df_sub = df_in
outfile = f"{METADATA_DIR}/movies_with_ids.csv"
df_out = pd.DataFrame()

if os.path.exists(outfile):
    try:
        df_out = pd.read_csv(outfile, encoding='utf-8',  encoding_errors='ignore')
        df_sub = df_in[~df_in['file'].isin(df_out['file'])]
    except pandas.errors.EmptyDataError:
        print("Warning: The output file is empty")

def handler(df_sub, lock):
    counter = 0
    checkpoint = 5

    data = []
    for index, row in df_sub.iterrows():
        # get the details of the movie based on the title
        print("Index:", index, "Movie:", row['title'])
        # get top 5 results
        search_results = ia.search_movie(row['title'])

        # get all the people of the movie from our x-ray data
        movie_cast = all_people[all_people["file"] == row['file']]['name_id'].values

        nr = dict(row)
        nr['imdb_id'] = None
        nr['match_error'] = None        # how many cast were matched
        
        # iterate over each search result
        for s in search_results[:5]:
            cast_data = ia.get_movie_full_credits(s.movieID)['data']
            # check if the movie has cast data at all
            if 'cast' in cast_data:
                # only get the top 5 cast
                cast = cast_data['cast'][:5]
            else:
                continue
            
            # no. of people listed on imdb for the movie
            cast_ids = ["nm" + item.personID for item in cast]
            nr['cast_num'] = len(cast_ids)

            errors = 0
            for ci in cast_ids:
                # count cases where the cast member is not in our x-ray data
                if ci not in movie_cast:
                    errors += 1 
            
            # calculate proportion of imdb cast that is in our x-ray data, if there's at least 1 match we save the result
            # we perform manual validation later to check how good the matching is
            if (len(cast_ids) - errors) / len(cast_ids) > 0:
                nr['imdb_id'] = s.movieID
                nr['match_error'] = errors
                print("Found match:", s.movieID)
                break
        
        data.append(nr)

        counter += 1

        # save data every 5 iterations
        if counter % checkpoint == 0:
            df = pd.DataFrame(data)
            with lock:
                df.to_csv(outfile, mode='a', header=not os.path.exists(outfile), index=False)
            data = []

    if data:
        df = pd.DataFrame(data)
        with lock:
            df.to_csv(outfile, mode='a', header=not os.path.exists(outfile), index=False)

# start matching in parallel with 3 workers
def scrape_concurrent(main_df, WORKERS=1):
    lock = Lock()

    files = np.array_split(main_df, WORKERS)

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        executor.map(handler, files, [lock] * WORKERS)

scrape_concurrent(df_sub)