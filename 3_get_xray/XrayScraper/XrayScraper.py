from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
import time
import pickle
import sys
import math
import threading
import shutil
import asyncio
import concurrent.futures
from multiprocessing import Process
from threading import Thread

import pandas as pd
import numpy as np
sys.path.append('../../')

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
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
        self.waittime = 60

    def get_driver(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options, seleniumwire_options=self.wire_options)
        driver.scopes = [
            "https://atv-ps.amazon.com/cdp/catalog/GetPlaybackResources",
            "https://atv-ps.amazon.com/swift/page/xrayVOD"
        ]
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
            time.sleep(5)

            pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
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

    def check_for_ad(self, driver):
        # //*[@id="dv-web-player"]/div/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[5]/div[2]/div[2]/div/div[2]/div[2]
        # //*[@id="dv-web-player"]/div/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[5]/div[2]/div[2]/div/div[2]/div
        print("Checking if there's an ad...")

        try:
            skipbtn = WebDriverWait(driver, self.waittime * 2).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Skip']"))
            )
            print("Found skip button, clicking...")
            print(skipbtn)
            print(skipbtn.get_attribute('innerText'))
            
            actions = ActionChains(driver)
            print("Moving to button...")
            actions.move_to_element(skipbtn)
            print("Clicking...")
            actions.click(skipbtn).perform()
            # skipbtn.click()
            print("Button clicked")
        except:
            print("Didn't find skipbtn")
        
    def capture_resources(self, driver, dir_name):
        counter = 0
        while True:
            print(f"Capture Resources {counter}...")
            # self.check_for_ad(driver)
            print("Look for the resources")
            try:
                # gathering the playback resources
                req_pb = driver.wait_for_request("https://atv-ps.amazon.com/cdp/catalog/GetPlaybackResources", timeout=self.waittime * 2)
                with open(os.path.join(dir_name, "PlaybackResources.json"), 'wb') as f:
                    f.write(((req_pb.response.body)))
            except:
                print("Error in getting the playback resources")
            
            # print("Look for skip btn")
            t = Thread(target=self.check_for_ad, args=(driver,), daemon=True)
            t.start()
            # self.check_for_ad(driver)

            try:
                print("Looking for xray...")
                # get the xray data
                req_xray = driver.wait_for_request("https://atv-ps.amazon.com/swift/page/xrayVOD", timeout=self.waittime * 2)
                with open(os.path.join(dir_name, "Xray.json"), 'wb') as f:
                    f.write(((req_xray.response.body)))
                print("Got all resources")
                print("Finishing up search for skip...")
                t.join()
                break
            except:
                counter += 1
                if counter >= 3: break 
                driver.refresh()
                print("Error in getting the xray data")
                print("Finishing up search for skip...")
                t.join()


    def extract_xray_and_playbackresources(self, df, driver):
        self.sign_in("https://www.amazon.com/gp/sign-in.html", driver)

        for index, row in df.iterrows():
            link = "https://www.amazon.com" + row['link']
            title = row['fname']
            driver.get(link)

            self.check_captcha(driver)
            # self.check_for_ad(driver)
            # if return_val == 0: continue

            dir_name = "xrays/com/" + row['fname']

            # play btn
            # document.querySelector('.dv-dp-node-playback')

            try:
                # if the directory already exists, remove it
                if os.path.exists(dir_name):
                    shutil.rmtree(dir_name)
                os.mkdir(dir_name)
            except:
                print("Error in handling the directory")
            
            # first check if movie playable
            # document.querySelector('#tvod-btn-ab-movie-hd-tvod_rental')
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'dv-dp-node-playback'))
                )
                print("Content is playable...\n")
            except:
                print("Play button not found, skip...", dir_name)
                continue

            self.capture_resources(driver, dir_name)

            # missing this line ruins lives
            del driver.requests
            
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
