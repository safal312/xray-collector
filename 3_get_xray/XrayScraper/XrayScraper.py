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

    async def check_for_ad(self, driver):
        # //*[@id="dv-web-player"]/div/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[5]/div[2]/div[2]/div/div[2]/div[2]
        print("Checking if there's an ad...")
        

        # # check if the sdk is loaded
        # WebDriverWait(driver, self.waittime).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'webPlayerSDKContainer'))
        # )
        # print("The video sdk is loaded")

        # ac = ActionChains(driver)

        # # text title
        # print("Title visible...")
        # title =  WebDriverWait(driver, 5 * 60).until(
        #     EC.visibility_of_element_located((By.CLASS_NAME, 'atvwebplayersdk-title-text'))
        # )

        # title_invisible =  WebDriverWait(driver, 5 * 60).until(
        #     EC.invisibility_of_element_located((By.CLASS_NAME, 'atvwebplayersdk-title-text'))
        # )
        # print("Title invisible...")

        # try:
        #     skipbtn = WebDriverWait(driver, 2 * 60).until(
        #         EC.presence_of_element_located((By.XPATH, '//div[text()="Skip"]'))
        #     )
        #     print("Skip btn present...")
        #     skipbtn.click()
        # except:
        #     print("Skip button not found")

        
        # try:
        #     seekbar_loaded = WebDriverWait(driver, 2 * 60).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, 'atvwebplayersdk-infobar-container'))
        #     )
        #     print(" Video loaded...")

        #     playbtn = WebDriverWait(driver, 60).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, "atvwebplayersdk-playpause-button"))
        #     )

        #     ac = ActionChains(driver)
        #     ac.move_to_element(playbtn).click().perform()

        #     print("Pressed playbtn")
        #     print(playbtn)
        # except:
        #     print("Skip button not found")
        # print("Title Loaded ...")

        # loading_done = WebDriverWait(driver, 5 * 60).until(
        #     EC.invisibility_of_element_located((By.CLASS_NAME, "atvwebplayersdk-loadingspinner-overlay"))
        # )
        # print("Loading complete...")

        # playbtn = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "atvwebplayersdk-playpause-button"))
        # )

        # print("Moving to play btn...")
        # ac.move_to_element(playbtn).perform()

        # time.sleep(2)
        # print("Play button visible")
        # playbtn.click()
        # print("Pushing btn...")

        # while True:
        #     try:
        #         # playbtn = WebDriverWait(driver, 120).until(
        #         #     EC.presence_of_element_located(By.CLASS_NAME, "atvwebplayersdk-playpause-button")
        #         # )
        #         # playbtn.click()
        #         # print("Looking for skip button...")
        #         skip_container = WebDriverWait(driver, 120).until(
        #             EC.presence_of_element_located((By.XPATH, '//div[text()="Skip"]'))
        #         )
        #         skip_container.click()
        #         return 1
        #     except:
        #         return 
        #         # counter += 1
        #         # driver.refresh()
        #         # if counter >= 2: return 0
        #         # print("Didn't find the skip button")
    
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

            try:
                # if the directory already exists, remove it
                if os.path.exists(dir_name):
                    shutil.rmtree(dir_name)
                os.mkdir(dir_name)
            except:
                print("Error in handling the directory")

            # run asynchronous search for skip button

            counter = 0
            while True:
                try:
                    # gathering the playback resources
                    req_pb = driver.wait_for_request("https://atv-ps.amazon.com/cdp/catalog/GetPlaybackResources", timeout=self.waittime * 2)
                    with open(os.path.join(dir_name, "PlaybackResources.json"), 'wb') as f:
                        f.write(((req_pb.response.body)))
                except:
                    print("Error in getting the playback resources")
                
                try:
                    # get the xray data
                    req_xray = driver.wait_for_request("https://atv-ps.amazon.com/swift/page/xrayVOD", timeout=self.waittime * 2)
                    with open(os.path.join(dir_name, "Xray.json"), 'wb') as f:
                        f.write(((req_xray.response.body)))
                    
                    break
                except:
                    counter += 1
                    if counter >= 3: break 
                    driver.refresh()
                    print("Error in getting the xray data")
                
            # missing this line ruins lives
            del driver.requests

            # try:
            #     for index, request in enumerate(driver.requests):
            #         if request.response:
            #             if "https://atv-ps.amazon.com/cdp/catalog/GetPlaybackResources" in request.url:
            #                 print(request.url)
            #                 del driver.requests[index]
            #                 print("deleted cached pb")

            #             if "https://atv-ps.amazon.com/swift/page/xrayVOD" in request.url:
            #                 print(request.url)
            #                 del driver.requests[index]
            #                 print("deleted cached xray")


            #         # if request.url.includes("https://atv-ps.amazon.com/cdp/catalog/GetPlaybackResources"):
            #         #     print(request)
                    
            #         # if request.url.includes("https://atv-ps.amazon.com/swift/page/xrayVOD"):
            #         #     print(request)
            # except:
            #     print("Can't delete")

                # print(driver.requests.index(req_pb))
                # print(driver.requests.index(req_xray))
                # del driver.requests
            
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
