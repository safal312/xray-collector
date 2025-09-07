**Order of Execution**

- `merge_xray_sub.ipynb`: This notebook merges all metadata with information on whether it also has subtitles or not.

- `8_finalize_data/filter_final_crew.ipynb`: This notebook filters the cast and support crew files to keep data for only the movies in our dataset.

- `8_finalize_data/add_tmdb.ipynb`: This notebook adds tmdb ids to each movie in our dataset.

**Files**:

- `merge_xray_sub.ipynb`:
    - `Inputs`:
        - `../data/6_character_metadata/all_metadata_finalized.csv`: Final metadata of movies after filling missing values, cleaning, and validation of X-Ray and Playback Resources files.
        - `../data/5_subtitles/subtitles_collected.csv`: Metadata of movies and info whether they have subtitles. More info available [here](../5_get_subtitles/README.md).
    
    - `Outputs`:
        - `../data/finalized_data/metadata_with_subtitles.csv`: This is the metadata of our whole dataset that merges information on whether each of the movies has a subtitle.


- `8_finalize_data/filter_final_crew.ipynb`: This notebook copies some of the essential metadata files into the `../data/finalized_data` and filters the cast and support crew files to keep data for only the movies in our dataset.
    - `Inputs`:
        - `../data/6_character_metadata/all_people_with_duplicates.csv`: Dataset file of all the cast in each movie.
        - `../data/6_character_metadata/movies_support_crew_with_manual.csv`: Dataset file of all crew for each movie.
    
    - `Outputs`:
        - `../data/finalized_data/final_all_cast_with_duplicates.csv`: Filtered dataset of casts in the final list of movies.
        - `../data/finalized_data/final_movies_support_crew.csv`: Filtered dataset of crew in the final list of movies.

- `8_finalize_data/add_tmdb.ipynb`:
    - `Inputs:`
        - `../data/finalized_data/metadata_with_subtitles.csv`
    - `Outputs`:
        - `../data/finalized_data/metadata_with_subtitles_tmdb.csv`
