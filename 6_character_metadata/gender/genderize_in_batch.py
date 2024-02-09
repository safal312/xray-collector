import os
import dotenv
import json
import pandas as pd
import requests
import time
dotenv.load_dotenv()

df = pd.read_csv("parsed_names_all_unique_crew_for_inference.csv", dtype={"person_id": str})

try:
    with open("crew_genderize_data.json", "r") as f:
        out = json.load(f)
except FileNotFoundError:
    out = []

name_list = list(map(lambda x: x['name_id'], out))
df_sub = df[~df['person_id'].isin(name_list)]

# Iterate over the DataFrame in chunks of 10 rows
chunk_size = 10
for index, chunk in df_sub.groupby(df_sub.index // chunk_size):
    # Use the process_chunk function on each chunk
    print(f"Processing chunk {index}")
    names = chunk['name_parsed'].apply(lambda x: "name[]=" + x.split()[0])
    names = "&".join(names)
    
    max_tries = 5
    for try_count in range(max_tries):
        try:
            res = requests.get(f"https://api.genderize.io?{names}&apikey={os.getenv('GENDERIZE_API')}")
            
            content = res.json()
            if 'error' in content:
                print(content['error'])
                break

            for index, c in enumerate(content):
                c['name_id'] = chunk.iloc[index]['person_id']

                print(res.status_code, index, c['name_id'], chunk.iloc[index]['name_parsed'], c['gender'])

            if res.status_code == 200:
                out = out + (content)
                break
        except:
            if try_count < max_tries - 1:
                print(f"Retrying... Attempt {try_count + 2}")
                time.sleep(1)  # Wait for 1 second before retrying
            else:
                raise Exception("Failed to get response after multiple tries")

    with open("crew_genderize_data.json", "w") as f:
        f.write(json.dumps(out, indent=4))