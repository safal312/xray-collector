from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.window import WindowHandles
from selenium.webdriver.chrome.options import Options

from utils.FileHandler import FileHandler
from utils.UserInput import UserInput

INPUT_FILE = "../../data/8_screenplays/1_validation/validation.csv"
OUTPUT_FILE = "../../data/8_screenplays/1_validation/validated_file.csv"

ui = UserInput(OUTPUT_FILE)
fh = FileHandler(ui.get_current_position(), INPUT_FILE)

# Create a new instance of Firefox driver
driver = webdriver.Firefox()

driver.get("https://example.com")
# Set the window size and position for both windows
window_width = driver.execute_script("return window.screen.availWidth;")
window_height = driver.execute_script("return window.screen.availHeight;")

driver.set_window_size(window_width // 2, window_height)
driver.set_window_position(0, 0)

# Open a new window and switch to it
driver.switch_to.new_window('window')
driver.get("https://example.com")

driver.set_window_size(window_width // 2, window_height)
driver.set_window_position(window_width // 2, 0)

def get(driver, url):
    res = driver.get(url)
    print(res)

while True:
    links, info = fh.get_link_next()
    if links == None: break

    imdb, script = links
    
    driver.switch_to.window(driver.window_handles[0])

    # Open the first link in the first window
    get(driver, imdb)

    driver.switch_to.window(driver.window_handles[1])

    get(driver, script)

    res = ui.ask_assessment(info)

driver.quit()