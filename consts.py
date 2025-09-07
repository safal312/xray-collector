"""
We collect the data from Amazon in batches. Each of the following directories contains the data for a specific batch.
- CLEAN_BASE_DIR: Contains the data for the batch of movies without filtering for a specific decade.
- BEFORE_2010_DIR: Contains the data for the batch of movies released before 2010.
- IN_2010S: Contains the data for the batch of movies released in the 2010s.
- AFTER_2020: Contains the data for the batch of movies released after 2020.

The GET_LINK function allows one to get the URL with the decade specification based on these macros.
"""

ALL_LINKS_DIR="../data/1_all_pages"
CLEAN_BASE_DIR="com"
BEFORE_2010_DIR="before2010"
IN_2010S="in2010s"
AFTER_2020="after2020"

def GET_LINK(page, type=CLEAN_BASE_DIR):
    if type == CLEAN_BASE_DIR:
        return f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_entity_type%3A14069184011&dc&page={page}&rnid=14069183011&ref=sr_pg_2"

    if type == BEFORE_2010_DIR:
        return f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_entity_type%3A14069184011%2Cp_n_feature_three_browse-bin%3A2651256011%7C2651257011%7C2651258011%7C2651259011%7C2651260011%7C2651261011&dc&page={page}&rnid=2651254011&ref=sr_pg_2"

    if type == IN_2010S:
        return f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_entity_type%3A14069184011%2Cp_n_feature_three_browse-bin%3A2651255011&dc&page={page}&rnid=2651254011&ref=sr_pg_2"
    
    if type == AFTER_2020:
        return f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_feature_three_browse-bin%3A52030197011%2Cp_n_entity_type%3A14069184011&dc&page={page}&rnid=14069183011&ref=sr_pg_2"
    
    raise Exception("Other links not implemented")