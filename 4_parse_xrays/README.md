**Order of Execution**
- `main.py`: This file reads the playback and xray files downloaded from the `3_get_xray` module and parses it.
- `remove_empty_xrays.py`: This script removes all the movies that don't have the breakdown of people in scenes i.e. the `../data/4_parsed_xrays/{target_dir}/{movie_dir}/people_in_scenes.csv` file is not existent or empty.

**Files**
- `main.py`:
    - `Inputs`:
        - `../data/3_xrays/{target_dir}/{movie_dir}/PlaybackResources.json` & `../data/3_xrays/{target_dir}/{movie_dir}/Xray.json`: These are the Playback resource and Xray files for each movie.
    - `Outputs`:
        -  `../data/4_parsed_xrays/{target_dir}/{movie_dir}`:
            - `/people_in_scenes.csv`: This file has a list of all the scenes with the cast in it. The file includes `scene, start, end, person_id, timestamp`. `scene` has the scene identifier in the movie, basically scene number. `start` and `end` are the times (in milliseconds) where the scene starts and ends. `person_id` is the unique identifier of a cast member used in xray; it has the name ID of the person from IMDb. `timestamp` is the time a particular character appears in the scene. 
            - `/people.csv`: This file has the list of all people in a movie. It has `id, person, character` where `id` is the unique identifier of the person, `person` is the actual name of the cast, and `character` is the name of the character in the movie.
            - `/scenes.csv`: This file has the list of all scenes with the scene ID and the start and end timestamps. The columns are:`scene, start, end`.
        
        - `../data/4_parsed_xrays/{target_dir}/movies_with_xrays.csv`: This file has the list of all movies that were parsed. It includes `file, title,  entityType, runtimeSeconds, synopsis, rating_count, rating,en_type, en_url, sdh_sub_lang,url`. These columns are as follows: 
            - `file`- unique movie file identifier
            - `title` - title of movie
            - `entityType` - Movie or TV show
            - `runtimeSeconds` - runtime of movie in Seconds
            - `synopsis` - description of movie
            - `rating_count` - total rating count on Amazon
            - `rating` - rating out of 5 on Prime
            - `en_type` - type of the english subtitle (whether it is 'SDH' or 'Subtitle')
            - `en_url` - link to the english subtitle
            - `sdh_sub_lang` - language of the subtitle that is of SDH type
            - `url` - link to the subtitle of SDH type.

- `inspect_empty_xray_data.py`: This is a utility script that calculates how many movies have missing `people.csv` files or `people_in_scenes.csv` files. This helps you to strategize how to remove the movies without valid xrays.

- `remove_empty_xrays.py`:
    - `Inputs`:
        - `../data/4_parsed_xrays/{target_dir}/`: We check if the `people_in_scenes.csv` file is present in each movie directory and is non-empty. Then, we only keep such entries from the `movies_with_xrays.csv` file.
    - `Outputs`"
        - `../data/4_parsed_xrays/{batch_name}_sub_movies_with_xrays.csv`: Has the same columns as `movies_with_xrays.csv`.