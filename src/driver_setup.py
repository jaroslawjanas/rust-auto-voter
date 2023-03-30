# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService

# Other
import platform
import time
import os
from src.args import args


def get_driver(options):

    # Check OS and set paths
    if args.browser_path and args.driver_path:
        browser_path = args.browser_path
        driver_path = args.driver_path
    elif args.browser_path or args.driver_path:
        print("You must specify both browser (--browser_path) and driver (--driver_path) path")
        exit()

    if platform.system() == "Windows":
        browser_path = "./browser/chrome-win/chrome.exe"
        driver_path = "./browser/chromedriver_win32/chromedriver.exe"
    else:
        browser_path = "./browser/chrome-linux/chrome"
        driver_path = "./browser/chromedriver_linux64/chromedriver"

    if not os.path.isfile(browser_path):
        print("Chromium browser not found, please download it from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html")
        exit()
    if not os.path.isfile(driver_path):
        print("Chromium driver not found, please download it from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html")
        exit()

    # Set options and start driver
    options.binary_location = browser_path
    service = ChromiumService(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Return driver
    return driver

# This is for testing
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=960,960")
    options.add_argument("--incognito")
    options.add_argument("--disable-cloud-management")
    driver = get_driver(options)
    driver.get("https://www.google.com/")
    time.sleep(10)
    driver.quit()