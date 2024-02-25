**Order of Execution**

- `Movie Script Database`, Aveek Saha, [GitHub Repository](https://github.com/Aveek-Saha/Movie-Script-Database), Published: July 2021
We used this repository to collect screenplays from various sources at once and parse it. You can find additional details from the Github Repository. Among other, running this repository will give you a `raw_screenplays` folder with the screenplays in their original format and another `parsed_screenplays` folder with the screenplays parsed and formatted in different files.

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

- `../data/8_screenplays/clean_validated.csv`: The tool tries to find the appropriate IMDb id for each screenplay, but it's not very accurate. Thus, we manually validate all the ids. The finalized ids are under the column `id_merged`.