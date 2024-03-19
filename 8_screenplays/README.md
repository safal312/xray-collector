**Order of Execution**

- `Movie Script Database`, Aveek Saha, [GitHub Repository](https://github.com/Aveek-Saha/Movie-Script-Database), Published: July 2021
We used this repository to collect screenplays from various sources at once and parse it. You can find additional details from the Github Repository. After this tool finishes execution, we will get a `scripts` folder. Among the files, `scripts/filtered` has all of the raw screenplays with duplicates removed which in this case has been renamed as `./raw_screenplays`. Another directory `scripts/metadata` has the metadata related to all the files. It has been renamed as `./parsed_screenplays/metadata`. Similary, the `scripts/parsed` directory has been renamed to `./parsed_screenplays/parsed`.

- `1_validation/validation_data.ipynb`: This notebook restructures the metadata into a csv file.

- `1_validation/validate.py`: This script helps validate the imdb ids collected by the tool manually.

- `1_validation/cleanup.ipynb`: This notebook cleans up and transforms validated metadata and also remove duplicates strategically.

- `2_metadata/1_get_movie_meta.ipynb`: This notebook collects IMDb metadata for all the movies.

- `2_metadata/2_get_cast.ipynb`: Get cast of all movies.

- `2_metadata/3_get_support_crew.ipynb`: This notebook gets all the support crew.

- `3_character_matching/character_matching.ipynb`: This notebook helps to match the characters in screenplay to imdb. It generates some stats on the matching as well.

- `merge_xray_sc.ipynb`: This notebook merges all metadata with information on whether it also has screenplays and subtitles or not.

**Files**:

- `Movie Script Database`:
    - `Outputs`: The description is pasted from the Github repo more information is available there.
        - `../data/8_screenplays/parsed_screenplays/charinfo/{movie_name}_charinfo.txt`: Contains a list of each character in the script and the number of lines they have, in this format, `C: Number of lines`.
        - `../data/8_screenplays/parsed_screenplays/dialogue/{movie_name}_dialogue.txt`: Contains scripts where each line has the character name, followed by a dialogue, in this format, `C=>D`.
        - `../data/8_screenplays/parsed_screenplays/tagged/{movie_name}_tagged.txt`: Contains scripts where each line has been tagged. The tags are:
            - `S` = Scene
            - `N` = Scene description
            - `C` = Character
            - `D` = Dialogue
            - `E` = Dialogue metadata
            - `T` = Transition
            - `M` = Metadata

- `1_validation/validation_data.ipynb`:
    - `Inputs`:
        - `../../data/8_screenplays/parsed_screenplays/metadata/clean_parsed_meta.json`: Metadata of all files in json format,
    
    - `Outputs`:
        - `../../data/8_screenplays/1_validation/validation.csv`: Reformatted metadata file.

- `1_validation/validate.py`:
    - `Inputs`:
        - `../../data/8_screenplays/1_validation/validation.csv`
    
    - `Outputs`:
        - `../../data/8_screenplays/1_validation/validated_file.csv`: File generated after validating IMDb ids.

- `1_validation/cleanup.ipynb`:
    - `Inputs`:
        - `../../data/8_screenplays/1_validation/validation.csv`
        - `../../data/8_screenplays/1_validation/validated_file.csv`

    - `Outputs`:
        - `../../data/8_screenplays/1_validation/clean_validated.csv`: This file has the clean metadata of all files. Among the other columns, `id_merged` has the finalized imdb id for all movies.

- `2_metadata/1_get_movie_meta.ipynb`:
    - `Inputs`:
        - `../../data/8_screenplays/1_validation/clean_validated.csv`
    
    - `Outputs`:
        - `../../data/8_screenplays/2_metadata/validated_meta.json`: IMDb metadata of all the movies in json format.
        - `../../data/8_screenplays/2_metadata/validated_movies.csv`: IMDb metadata in csv format. The columns are the different data entries available for any movie.

- `2_metadata/2_get_cast.ipynb`:
    - `Inputs`:
        - `../../data/8_screenplays/2_metadata/validated_movies.csv`
    
    - `Outputs`:
        - `../../data/8_screenplays/2_metadata/all_cast.csv`: This file has all the cast for each movie along with their name ID from IMDb.

- `2_metadata/3_get_support_crew.ipynb`:
    - `Inputs`:
        - `../../data/8_screenplays/2_metadata/validated_movies.csv`

    - `Outputs`:
        - `../../data/8_screenplays/2_metadata/all_support_cast.csv`: This file has all the support crew for each movie.
        - `../../data/8_screenplays/2_metadata/clean_all_support_cast.csv`: This file has the support crew data after removing duplicates and null person IDs.

- `3_character_matching/character_matching.ipynb`:
    - `Inputs`:
        - `../../data/8_screenplays/1_validation/clean_validated.csv`
        `../../data/8_screenplays/2_metadata/validated_movies.csv`: We merge this with clean_validated to get a file with the required columns.
        - `../../data/8_screenplays/parsed_screenplays/parsed/charinfo/*.txt`: Get the charinfo file for all movies which has a list of each character in the script and the number of lines they have.

    - `Outputs`:
        - `../../data/8_screenplays/3_character_matching/all_characters.csv`: This file has all the characters in all the movies of our dataset with the columns `imdb`: IMDb id of a movie, `char`: name of character, `utterances`: total dialogues in movie of character.
        - `../../data/8_screenplays/3_character_matching/total_utterances.csv`: File has total utterances in a movie by all characters.
        - `../../data/8_screenplays/3_character_matching/match_stats.csv`: This file has stats on the matching of characters for each movie. There are three measures that we use:
            - `high_matches`: (number of cast with match score > 80) / total_cast
            - `avg_score`: average matching score of all cast
            - `coverage`: total utterances of all remaining characters (some characters were removed if they had no utterance or were erroneous characters) / total utterances calculated for all characters. (We need this metric to check how much information we discarded from a movie)
        - `../../data/8_screenplays/3_character_matching/all_chars_matched_imdb.csv`: Metadata of all movies with match stats added as new columns.
        
        - `../../data/8_screenplays/3_character_matching/movies_with_high_coverage_and_matching/`: We remove entries with low scores on our metric (movies with low `high_matches` and low `coverage`).
            - `imdb_and_stats.csv`: Filtered `match_stats.csv` file with high matching.
            - `matches_with_stats.csv`: Filtered metadata of movies with stats.

- `merge_xray_sc.ipynb`:
    - `Inputs`:
        - `../data/6_character_metadata/all_metadata_finalized.csv`: Final metadata of movies after filling missing values, cleaning, and validation of X-Ray and Playback Resources files.
        - `../data/5_subtitles/subtitles_collected.csv`: Metadata of movies and info whether they have subtitles. More info available [here](../5_get_subtitles/README.md).
    
    - `Outputs`:
        - `../data/8_screenplays/metadata_with_screenplay_subtitles.csv`: This is the metadata of our whole dataset that merges information on whether each of the movies has a screenplay/subtitle.

- `../data/8_screenplays/clean_validated.csv`: The tool tries to find the appropriate IMDb id for each screenplay, but it's not very accurate. Thus, we manually validate all the ids. The finalized ids are under the column `id_merged`.

