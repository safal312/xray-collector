from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# driver class extending webdriver element
class FirefoxDriver(webdriver.Firefox):
    def __init__(self):
        """
        Helper class to start two windows of Firefox browser.
        """
        super().__init__()

        self.def_addr = "https://example.com"
    
    def initiate_two_screens(self):
        self.get(self.def_addr)
        # Set the window size and position for both windows
        window_width = self.execute_script("return window.screen.availWidth;")
        window_height = self.execute_script("return window.screen.availHeight;")

        self.set_window_size(window_width // 2, window_height)
        self.set_window_position(0, 0)

        # Open a new window and switch to it
        self.switch_to.new_window('window')
        self.get(self.def_addr)

        self.set_window_size(window_width // 2, window_height)
        self.set_window_position(window_width // 2, 0)