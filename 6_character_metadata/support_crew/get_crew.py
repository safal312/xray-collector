import os
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import pandas.io.common
from imdb import Cinemagoer

ia = Cinemagoer()

df_in = pd.read_csv("../movies_with_ids.csv", dtype={"movie_id": str})
df_in = df_in[~df_in['movie_id'].isna()]
df_sub = df_in[~df_in['movie_id'].duplicated()]
# df_sub = df_in

outfile = "movies_support_crew.csv"
df_out = pd.DataFrame()

if os.path.exists(outfile):
    try:
        df_out = pd.read_csv(outfile, dtype={"movie_id": str})
        df_sub = df_in[~df_in['movie_id'].isin(df_out['movie_id'])]
    except pandas.errors.EmptyDataError:
        print("Warning: The output file is empty")

# # check duplicates
# df_check = df_sub[df_sub['movie_id'].isin(df_sub[df_sub['movie_id'].duplicated()]['movie_id'])]
# df_check.sort_values(by='movie_id')[['file','movie_id']].to_csv("check_duplicate_ids.csv", index=False)

def handler(df_sub, lock):
    counter = 0
    checkpoint = 5

    data = []
    for index, row in df_sub.iterrows():
        print("Index:", index, "Movie:", row['title'])
        # nr = dict(row)
        movie_id = row['movie_id']

        all_people = ia.get_movie_full_credits(movie_id)['data']
        
        if type(all_people) != type(None):
            for dep in all_people.keys():

                people  = all_people[dep]
                for p in people:
                    # add movie name/title also later
                    nr = {'movie_id': movie_id, 'file': row['file'], 'role': None,'person_id': None, 'name': None, 'long_canonical_name': None, 'headshot': None}
                    nr['role'] = dep
                    
                    if p.get('name'):
                        nr['name'] = p['name']
                    else: continue
                    
                    if p.get('long imdb canonical name'):
                        nr['long_canonical_name'] = p['long imdb canonical name']
                    
                    if p.get('headshot'):
                        nr['headshot'] = p['headshot']
                    
                    if hasattr(p, 'personID'):
                        if p.personID:
                            nr['person_id'] = p.personID
                    else: continue
        
                    # print(nr)
                    data.append(nr)
        # exit()

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