# import requests

# # page range is from 1 to 100
# page = 1

# for p in range(1, 2):
#     url = f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_entity_type%3A14069184011&dc&page={p}&rnid=14069183011&ref=sr_pg_2"
    
#     page = requests.get(url)

#     with open(f"all_pages/page_{p}.html", "wb") as f:
#         f.write(page.content)

from AmazonPrimeScraper import Scraper, Logger

scr = Scraper()
lgr = Logger("log.txt")

driver = scr.get_driver()

PAGES = 400

for pagen in range(1, PAGES + 1):
    try:
        driver.get(f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_entity_type%3A14069184011&dc&page={pagen}&rnid=14069183011&ref=sr_pg_2")

        content = driver.page_source

        print(f"Scraping {pagen}/PAGES...")

        with open(f"all_pages/page_{pagen}.html", "w", encoding='utf-8') as f:
            f.write(content)
    except:
        msg = "ERROR with page " + str(pagen)
        print(msg)
        lgr.save_log(msg)

driver.close()