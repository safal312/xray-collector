import os
import sys
sys.path.append('../')  #relative import of AmazonPrimeScraper

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from AmazonPrimeScraper import Scraper, Logger
from consts import GET_LINK, ALL_LINKS_DIR, CLEAN_SCRAPE_DIR, BEFORE_2010_DIR, IN_2010S, AFTER_2020

scr = Scraper(headless=True)
lgr = Logger("log.txt")

driver = scr.get_driver()
# Since I didn't login first, the Watch Now buttons didn't appear

def dir_check():
    if not os.path.exists(ALL_LINKS_DIR): os.mkdir(ALL_LINKS_DIR)
    if not os.path.exists(os.path.join(ALL_LINKS_DIR, CLEAN_SCRAPE_DIR)): os.mkdir(os.path.join(ALL_LINKS_DIR, CLEAN_SCRAPE_DIR))
    if not os.path.exists(os.path.join(ALL_LINKS_DIR, BEFORE_2010_DIR)): os.mkdir(os.path.join(ALL_LINKS_DIR, BEFORE_2010_DIR))
    if not os.path.exists(os.path.join(ALL_LINKS_DIR, IN_2010S)): os.mkdir(os.path.join(ALL_LINKS_DIR, IN_2010S))
    if not os.path.exists(os.path.join(ALL_LINKS_DIR, AFTER_2020)): os.mkdir(os.path.join(ALL_LINKS_DIR, AFTER_2020))

# Change the target dir to set which subset you want to scrape
TARGET_DIR = AFTER_2020

# GET PAGES NO BY navigating to first page
driver.get(GET_LINK(1, type=TARGET_DIR))
PAGES = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "s-pagination-disabled"))
)[-1]
PAGES = int(PAGES.get_attribute("innerText"))

for pagen in range(1, PAGES + 1):
    try:
        dir_check()
        link = GET_LINK(pagen, type=TARGET_DIR)
        driver.get(link)

        content = driver.page_source

        print(f"Scraping {pagen}/{PAGES}...")

        with open(os.path.join(ALL_LINKS_DIR, TARGET_DIR, f"page_{pagen}.html"), "w", encoding='utf-8') as f:
            f.write(content)
    except:
        msg = "ERROR with page " + str(pagen)
        print(msg)
        lgr.save_log(msg)

driver.close()