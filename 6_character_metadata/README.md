**Order of Execution**
- `extract_names.py`: This script gathers all the names from the remaining movies that have valid x-rays into one file.
- `get_valid_movies.ipynb`: This notebook gets the metadata for all the remaining valid movies that have at least one person in the movie.
- `imdb_matching.py`: This script runs the algorithm to find the correct imdb id of a movie based on the cast list. We search movies first based on the title and get top 5 results. Now, we check for intersection between the cast list from our x-ray data and the imdb listing. Among the 5 results, we iteratively look for an imdb listing that has at least one person that intersects.

**Files**
- `extract_names.py`:
    - `Inputs`:
        - `../data/4_parsed_xrays/{target_dir}/{target_dir}_sub_movies_with_xrays.csv`: We make use of the metadata of movies with valid xrays, generated from `4_parse_xrays` module. Using the file names from the `file` column, we open each movie's respective `people.csv` file and save it into a common dataframe.

    - `Outputs`:
        - `../data/6_character_metadata/all_people_with_duplicates.csv`: The script generates a file which has all the cast from every movie in one file.
        - `../data/6_character_metadata/all_people.csv`: This file is similar, but duplicates based on each person's unique imdb name ID have been removed to get a list of all unique people in our dataset.

- `get_valid_movies.ipynb`:
    - `Inputs`:
        - `../data/4_parsed_xrays/{dir}_sub_movies_with_xrays.csv`: We use the metadata of all the movies with valid xrays. We combine the metadata of all batches together and fill in any missing values. For example, `title` was missing for some entries. Therefore, we used the metadata file `../data/2_metadata/{dir}/clean_meta_en_prime.csv` to fill such cases.

    - `Outputs`:
        - `../data/6_character_metadata/movies_with_cast_manual.csv`: This is the dataset with the metadata of all movies with valid xrays in our dataset.
        