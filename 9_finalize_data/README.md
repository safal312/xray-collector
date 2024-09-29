**Order of Execution**

- `9_finalize_data/filter_final_crew.ipynb`: This notebook filters the cast and support crew files to keep data for only the movies in our dataset.

- `9_finalize_data/add_tmdb.ipynb`: This notebook adds tmdb ids to each movie in our dataset.

**Files**:

- `9_finalize_data/filter_final_crew.ipynb`: This notebook copies some of the essential metadata files (`../data/6_character_metadata/all_metadata_finalized.csv`,`../data/8_screenplays/metadata_with_screenplay_subtitles.csv`) into the `../data/finalized_data` and filters the cast and support crew files to keep data for only the movies in our dataset.
    - `Inputs`:
        - `../data/6_character_metadata/all_people_with_duplicates.csv`: Dataset file of all the cast in each movie.
        - `../data/6_character_metadata/movies_support_crew_with_manual.csv`: Dataset file of all crew for each movie.
    
    - `Outputs`:
        - `../data/finalized_data/final_all_cast_with_duplicates.csv`: Filtered dataset of casts in the final list of movies.
        - `../data/finalized_data/final_movies_support_crew.csv`: Filtered dataset of crew in the final list of movies.

- `9_finalize_data/add_tmdb.ipynb`:
    - `Inputs:`
        - `../data/finalized_data/metadata_with_screenplay_subtitles.csv`
    - `Outputs`:
        - `../data/finalized_data/metadata_with_screenplay_subtitles_tmdb.csv`
