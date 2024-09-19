import os
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import pandas.io.common
from imdb import Cinemagoer

ia = Cinemagoer()

# import the final metadata file
METADATA_DIR = "../../data/6_character_metadata"
df_in = pd.read_csv(f"{METADATA_DIR}/final_validated_metadata.csv", dtype={"imdb_id": str})
df_in = df_in[~df_in['imdb_id'].isna()]
df_sub = df_in[~df_in['imdb_id'].duplicated()]
# df_sub = df_in

outfile = f"{METADATA_DIR}/movies_support_crew_with_manual.csv"
df_out = pd.DataFrame()

# get last checkpoint
if os.path.exists(outfile):
    try:
        df_out = pd.read_csv(outfile, dtype={"imdb_id": str})
        df_sub = df_in[~df_in['imdb_id'].isin(df_out['imdb_id'])]
    except pandas.errors.EmptyDataError:
        print("Warning: The output file is empty")

def handler(df_sub, lock):
    counter = 0
    checkpoint = 5

    data = []
    for index, row in df_sub.iterrows():
        print("Index:", index, "Movie:", row['title'])
        movie_id = row['imdb_id']

        # get all credits from imdb
        all_people = ia.get_movie_full_credits(movie_id)['data']
        
        if type(all_people) != type(None):
            for dep in all_people.keys():

                people  = all_people[dep]
                for p in people:
                    # save data of everyone along with their role
                    nr = {'imdb_id': movie_id, 'file': row['file'], 'role': None,'name_id': None, 'person': None, 'long_canonical_name': None, 'headshot': None}
                    nr['role'] = dep
                    
                    if p.get('name'):
                        nr['person'] = p['name']
                    else: continue
                    
                    if p.get('long imdb canonical name'):
                        nr['long_canonical_name'] = p['long imdb canonical name']
                    
                    if p.get('headshot'):
                        nr['headshot'] = p['headshot']
                    
                    if hasattr(p, 'personID'):
                        if p.personID:
                            nr['name_id'] = "nm" + str(p.personID)
                    else: continue
        
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

# scrape concurrently with 3 workers by default
def scrape_concurrent(main_df, WORKERS=3):
    lock = Lock()

    files = np.array_split(main_df, WORKERS)

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        executor.map(handler, files, [lock] * WORKERS)

scrape_concurrent(df_sub)