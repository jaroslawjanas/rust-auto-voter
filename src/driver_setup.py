# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Other
import platform
import time
import os
from src.args import args
from src.logs import log


deafult_paths = {
    "Windows": ("./browser/chrome-win/chrome.exe", "./browser/chromedriver_win32/chromedriver.exe"),
    "Linux": ("./browser/chrome-linux/chrome", "./browser/chromedriver_linux64/chromedriver")
}

def get_paths():

    # Set paths
    if args.browser_path and args.driver_path:
        browser_path = args.browser_path
        driver_path = args.driver_path

    elif args.browser_path or args.driver_path:
        print(
            "You must specify both browser (--browser_path) and driver (--driver_path) path")
        exit()

    else:
        if platform.system() == "Windows":
            browser_path, driver_path = deafult_paths["Windows"]
        else:
            browser_path, driver_path = deafult_paths["Linux"]

    # Check paths
    if not os.path.isfile(browser_path):
        print("Chromium browser not found.")
        print("Please download it from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html")
        exit()
    if not os.path.isfile(driver_path):
        print("Chromium driver not found.")
        print("Please download it from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html")
        exit()

    return (browser_path, driver_path)


def get_driver(options=None):

    browser_path, driver_path = get_paths()

    # Check OS and set paths
    if args.browser_path and args.driver_path:
        browser_path = args.browser_path
        driver_path = args.driver_path
    elif args.browser_path or args.driver_path:
        print(
            "You must specify both browser (--browser_path) and driver (--driver_path) path")
        exit()
    else:
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
    # if options is not None then
    if not options:
        options = Options()
        if args.headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={args.width},{args.height}")
        options.add_argument("--incognito")
        options.add_argument("--disable-cloud-management")
        if args.debug:
            options.add_argument("--log-level=0")
        else:
            options.add_argument("--log-level=3")
            options.add_argument("--silent")

    options.binary_location = browser_path

    service = ChromiumService(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Test driver
    try:
        driver.get("https://www.google.com/")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.title_is("Google"))
        log("Driver test successful")
    except:
        print("Failed to test the driver!\nCheck if the browser and driver paths are correct")
        driver.quit()
        exit()

    # Return driver
    return driver