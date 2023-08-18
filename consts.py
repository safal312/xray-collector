ALL_LINKS_DIR="all_pages"
CLEAN_SCRAPE_DIR="com"
BEFORE_2010_DIR="before2010"
IN_2010S="in2010s"
AFTER_2020="after2020"

def GET_LINK(page, type=CLEAN_SCRAPE_DIR):
    if type == CLEAN_SCRAPE_DIR:
        return f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_entity_type%3A14069184011&dc&page={page}&rnid=14069183011&ref=sr_pg_2"

    if type == BEFORE_2010_DIR:
        return f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_entity_type%3A14069184011%2Cp_n_feature_three_browse-bin%3A2651256011%7C2651257011%7C2651258011%7C2651259011%7C2651260011%7C2651261011&dc&page={page}&rnid=2651254011&ref=sr_pg_2"

    if type == IN_2010S:
        return f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_entity_type%3A14069184011%2Cp_n_feature_three_browse-bin%3A2651255011&dc&page={page}&rnid=2651254011&ref=sr_pg_2"
    
    if type == AFTER_2020:
        return f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_feature_three_browse-bin%3A52030197011%2Cp_n_entity_type%3A14069184011&dc&page={page}&rnid=14069183011&ref=sr_pg_2"
    
    raise Exception("Other links not implemented")