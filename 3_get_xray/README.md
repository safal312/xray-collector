**Order of Execution:**
- `.env.example`: Please copy the contents of the `.env.example` file into a new `.env` file and fill in your own username and password for Amazon Prime Video to start running the scripts.

- `get_video_data.py`: This script is used to get the main page of a movie listing on the Prime Video platform. We mainly need this step to see if a movie has x-ray data available. If a movie does, it will have a 'X-RAY' tag on it. This will help us filter out movies without x-ray data available and also collect some metadata in the process.

- `parse_video_data.py`: This script is used to parse the contents of the html files of each movie's main page in Prime Video. It generates a metadata file with the unique filename, link to the actual movie (link of the play button), synopsis, and other related movie data.

- `check_reduction.ipynb`: This notebook is used to check the number of movies after filtering out those without X-Ray data.

- `clean_parsed.ipynb`: This notebook removes all the movies without x-ray data and creates a new file.

- `get_xrays.py`: This script opens up the link to the prime video on multiple windows (based on number of workers set) and intercepts the x-ray and playback resources files.

- `inspect_missings.py`: This script checks the directory with all xrays and extracts the ones that have no files or only the playback resource file downloaded for inspection. Usually, the movies with no files are the ones that are "paid" and can't be accessed with the prime membership. The ones with only the playback resource are the ones which might have the x-rays but weren't downloaded because of the network or other issues. This script can be used to get the list of movies to retry downloading using the `get_xrays.py` script.

**Files**:
- `get_video_data.py`:
    - Inputs:
        - `../data/2_metadata/{target_dir}/sub_clean_meta_en_prime.csv`: This file includes all the metadata of the movie listings in their corresponding batch directories. `target_dir` represents the directory/batch to be processed.
    - Outputs: 
        - `../data/3_metadata_movie_pages/`: Directory where all the html webpages from Amazon website in different directories respective to their batches are stored.

- `parse_video_data.py`:
    - Inputs:
        - `../data/3_metadata_movie_pages`: Metadata output files from previous script.
    - Outputs:
        - `../data/3_metadata_movie_pages_parsed/{target_dir}/meta_en_prime.csv`: Metadata of all movies in their respective batch.

- `utils/PrimeVideoPageHandler.py`: Utility script used to parse video data in `parse_video_data.py`.

- `utils/general.py`: `extract_remaining` gets the remaining movies to download prime video main page for. `get_remaining_xrays` returns the original dataframe minus the movies for which xrays have been collected.

- `check_reduction.ipynb`:
    - Inputs: Metadata output files from `parse_video_data.py`

- `clean_parsed.ipynb`:
    - Inputs:
        - `../data/3_metadata_movie_pages_parsed/{target_dir}/meta_en_prime.csv`: Metadata output files from `parse_video_data.py`.
    - Outputs:
        - `../data/3_metadata_with_xray/{target_dir}/meta_en_prime.csv`: Metadata of all movies that have x-rays in their respective batch.

- `get_xrays.py`:
    - Inputs:
        - `../data/3_metadata_with_xray/{target_dir}/meta_en_prime.csv`: Metadata of all movies with xrays; output of `clean_parsed.ipynb`.
    - Outputs:
        - `../data/3_xrays/{target_dir}/{movie_dir}/PlaybackResources.json`: Playback Resources file of a movie which has movie metadata like title, synopsis, link to subtitles (if available) , runtime, and other additional details unique to prime video.
        - `../data/3_xrays/{target_dir}/{movie_dir}/Xray.json`: Xray file of a movie which has the list of scenes and the cast in each of the scenes. It also has duration of the scenes and the imdb name ID of each cast member.

- `XrayCollector/XrayCollector.py`: This file contains the main helper class which allows you to collect both the metadata (movie main page) and the playback with xray files.

- `cookies.pkl`: The scripts `get_video_data.py` and `get_xrays` need to login to your Amazon account before starting collecting. The `cookies.pkl` file is generated if it is missing in the directory when you run the script. On first run, the scripts will navigate you to the login page. After successful login, the cookie will be saved for easier use in the future.