## Amazon Prime Video X-Ray Data Collector Pipeline
This repository holds the code to collect data from the Amazon Prime Video platform. It has different modules with their own functions that come together to help gather, clean, and augment X-Ray data.



![](./images/logo.png)


### Modules
The following are the different modules in our xray collector pipeline. Each of the modules have their own README file for more detail.
- `1_get_links`: Collects the movie listing from Amazon US platform.
- `2_parse_links`: Parses the html files of movie listing to csv.
- `3_get_xray`: First gathers metadata on each movie and gets the "Playback Resources" and "X-Ray" file for movies with x-ray data.
- `4_parse_xrays`: Parses the playback resources and x-ray file to generate metadata about the movies and also extract list of people in different scenes.
- `5_get_subtitles`: Collects subtitles with appropriate formats for the movies.
- `6_character_metadata`: Organizes information on the cast. Matches each movie with an IMDb id and also provides a helper module to validate the movies. Collects the support crew for each movie after correct imdb ids are collected.
- `7_imdb_validation`: Helps manually validate the matching accuracy of imdb ids.
- `8_finalize_data`: It has a notebook that finalizes the end dataset and puts them in the `/data/finalized_data` folder.

### Data
The data is available under `/data`. Each directory is numbered with the module number it belongs to. For example, `1_get_links` produces the html pages of movie listings and saves it under `1_all_pages`. Suggestions on accessing the crucial data files are mentioned in the `data/README.md` file.