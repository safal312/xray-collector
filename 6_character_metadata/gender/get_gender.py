import sys
sys.path.append('../../')  #relative import of AmazonPrimeScraper

from AmazonPrimeScraper import Scraper
from utils.ImdbGender import ImdbGender


scr = Scraper(headless=False, fast_load=True)
# driver = scr.get_driver()
ig = ImdbGender(scraper=scr)

ig.scrape_concurrent()