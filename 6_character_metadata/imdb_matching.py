import os
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import pandas.io.common
from imdb import Cinemagoer

ia = Cinemagoer()

# you need all people with duplicates because if you remove the duplicates, you won't get all characters from each movie when subsetting
all_people = pd.read_csv("all_people_with_duplicates.csv")
df_in = pd.read_csv("movies_with_cast_manual.csv")
df_in = df_in[~df_in['title'].isna()]

df_sub = df_in
outfile = "movies_with_ids.csv"
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
        print("Index:", index, "Movie:", row['title'])
        search_results = ia.search_movie(row['title'])

        movie_cast = all_people[all_people["movie"] == row['file']]['name_id'].values

        nr = dict(row)
        nr['movie_id'] = None
        nr['match_error'] = None
        
        for s in search_results[:5]:
            print(s)
            cast_data = ia.get_movie_full_credits(s.movieID)['data']
            if 'cast' in cast_data:
                cast = cast_data['cast'][:5]
            else:
                continue
            cast_ids = ["nm" + item.personID for item in cast]
            nr['cast_num'] = len(cast_ids)

            errors = 0
            for ci in cast_ids:
                print(ci)
                if ci not in movie_cast:
                    errors += 1
                    # if errors > 2:
                    #     print("Didn't match")
                    #     break 
            
            if (len(cast_ids) - errors) / len(cast_ids) > 0:
                nr['movie_id'] = s.movieID
                nr['match_error'] = errors
                print("Found match:", s.movieID)
                break
            
        data.append(nr)

        counter += 1

        if counter % checkpoint == 0:
            df = pd.DataFrame(data)
            with lock:
                df.to_csv(outfile, mode='a', header=not os.path.exists(outfile), index=False)
            data = []

    if data:
        df = pd.DataFrame(data)
        with lock:
            df.to_csv(outfile, mode='a', header=not os.path.exists(outfile), index=False)

def scrape_concurrent(main_df, WORKERS=3):
    lock = Lock()

    files = np.array_split(main_df, WORKERS)

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        executor.map(handler, files, [lock] * WORKERS)

scrape_concurrent(df_sub)