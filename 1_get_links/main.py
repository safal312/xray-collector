
import sys
sys.path.append('../')  #relative import of AmazonPrimeScraper

from AmazonPrimeScraper import Scraper, Logger

scr = Scraper(headless=True)
lgr = Logger("log.txt")

driver = scr.get_driver()

PAGES = 2

# Since I didn't login first, the Watch Now buttons didn't appear

for pagen in range(1, PAGES + 1):
    try:
        driver.get(f"https://www.amazon.com/s?i=instant-video&rh=n%3A19325307011%2Cp_n_ways_to_watch%3A12007865011%2Cp_n_entity_type%3A14069184011&dc&page={pagen}&rnid=14069183011&ref=sr_pg_2")

        content = driver.page_source

        print(f"Scraping {pagen}/PAGES...")

        with open(f"all_pages/com/page_{pagen}.html", "w", encoding='utf-8') as f:
            f.write(content)
    except:
        msg = "ERROR with page " + str(pagen)
        print(msg)
        lgr.save_log(msg)

driver.close()