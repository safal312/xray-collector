**Order of Execution:**
The following scripts need to run in the mentioned order. Detailed descriptions are available below under **Files**.
- `parse_metadata.py`: Parses movie listing webpages collected in `1_get_links` module.
- `clean_metadata.ipynb`: Parses and standardizes tags and titles of movies in the movie listing. Explores varieties of duplicated movie entries and de-duplication techniques. Generates unique file names associated with each movie.
- `check_duplicated_run.ipynb`: Redundant movies across different batches removed.

**Files:**

- `parse_metadata.py`:
    - Inputs:
        - `../data/1_all_links/{target_dir}`: Directory with all the html webpages from Amazon website. `target_dir` represents the directory/batch to be processed.
    - Outputs: 
        - `../data/2_metadata/{target_dir}`: Directory where parsed metadata will be stored.
            - `meta_en_prime.csv`: Metadata generated after parsing webpage.

- `clean_metadata.ipynb`:
    - Inputs:
        - `../data/2_metadata/{target_dir}/meta_en_prime.csv`: Output files of above script
    - Outputs:
        - `../data/2_metadata/{target_dir}/clean_meta_en_prime.csv`: Output file after first de-duplication. Includes: `title,link,tags,year,clean_title,file,short_url,clean_short_url`

- `check_duplicated_run.ipynb`:
    - Inputs:
        - `../data/2_metadata/{target_dir}/clean_meta_en_prime.csv`: Output files of above script
    - Outputs:
        - `../data/2_metadata/{target_dir}/sub_clean_meta_en_prime.csv`: Output file after removing duplicates across the multiple batches
