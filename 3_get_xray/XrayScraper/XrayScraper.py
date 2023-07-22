from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
import time
import pickle
import sys
import math
import threading
import shutil

import pandas as pd
import numpy as np
sys.path.append('../../')

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
from seleniumwire.utils import decode

from AmazonPrimeScraper import Scraper

class XrayScraper(Scraper):
    def __init__(self, headless=True, workers=1):
        super().__init__(headless)
        self.wire_options = {
            'disable_encoding': True  # Ask the server not to compress the response
        }
        self.WORKERS = workers
        self.waittime = 10000

    def get_driver(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options, seleniumwire_options=self.wire_options)
        self.driver = driver
        return driver

    def get_element_with_id(self, id):
        return WebDriverWait(self.driver, self.waittime).until(
            EC.presence_of_element_located((By.ID, id))
        )

    def sign_in(self, address, driver):
        if os.path.exists(os.path.join(os.getcwd(), "cookies.pkl")):
            print("Found old session...")
            self.load_session(driver)
            return

        load_dotenv()

        driver.get(address)

        uname_el = self.get_element_with_id("ap_email")
        uname_el.send_keys(os.getenv("USER"))
        
        self.get_element_with_id("continue").click()

        password_el = self.get_element_with_id("ap_password")
        password_el.send_keys(os.getenv("PASS"))
        remember_me = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        remember_me.click()

        self.get_element_with_id("signInSubmit").click()

        otp = self.get_element_with_id("auth-mfa-otpcode")
        otp_value  = input("Enter OTP: ")
        otp.send_keys(otp_value)

        self.get_element_with_id("auth-signin-button").click()

        time.sleep(5)

        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    
    def load_session(self, driver):
        driver.get("https://www.amazon.com/404")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    
    def check_captcha(self, driver):
        try:
            driver.find_element(By.XPATH, '//button[text()="Continue shopping"]')
            input("Captcha detected. Fill in and press enter...")
        except:
            pass

    def scrape_metadata(self, df, driver):
        self.sign_in("https://www.amazon.com/gp/sign-in.html", driver)
        
        for index, row in df.iterrows():
            link = "https://www.amazon.com" + row['link']
            title = row['fname']
            driver.get(link)

            self.check_captcha(driver)

            content = driver.page_source

            try:
                with open(f"metadata/com/{title}.html", "w", encoding='utf-8') as f:
                    f.write(content)
                    print("Writing " + title)
            except:
                print("There was an error in downloading " + title)
        
        print("Scraping done for this chunk")
    
    def extract_xray_and_playbackresources(self, df, driver):
        self.sign_in("https://www.amazon.com/gp/sign-in.html", driver)

        for index, row in df.iterrows():
            link = "https://www.amazon.com" + row['link']
            title = row['fname']
            driver.get(link)

            self.check_captcha(driver)

            dir_name = "xrays/com/" + row['fname']

            try:
                # if the directory already exists, remove it
                if os.path.exists(dir_name):
                    shutil.rmtree(dir_name)
                os.mkdir(dir_name)
            except:
                print("Error in handling the directory")

            try:
                # gathering the playback resources
                req = driver.wait_for_request("https://atv-ps.amazon.com/cdp/catalog/GetPlaybackResources", timeout=self.waittime * 2)
                with open(os.path.join(dir_name, "PlaybackResources.json"), 'wb') as f:
                    f.write(((req.response.body)))
            except:
                print("Error in getting the playback resources")
            
            try:
                # get the xray data
                req = driver.wait_for_request("https://atv-ps.amazon.com/swift/page/xrayVOD", timeout=self.waittime * 2)
                with open(os.path.join(dir_name, "Xray.json"), 'wb') as f:
                    f.write(((req.response.body)))
            except:
                print("Error in getting the xray data")
            
        print("Scraping done for this chunk")

    # https://medium.com/geekculture/introduction-to-selenium-and-python-multi-threading-module-aa5b1c4386cb
    def run_workers(self, main_df, FOR):
        files = np.array_split(main_df, self.WORKERS)

        drivers = [self.get_driver() for _ in range(self.WORKERS)]

        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            handler = ""
            if FOR == "metadata":
                handler = self.scrape_metadata
            elif FOR == "xrays":
                handler = self.extract_xray_and_playbackresources
            
            executor.map(handler, files, drivers)
        
        [driver.quit() for driver in drivers]
