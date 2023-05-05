# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Locators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Other
import platform
import os
from src.args import args
from src.logs import log, debug_log
from src.debug import slow


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

def steam_login(driver):
    wait = WebDriverWait(driver, 10)

    # Load steam login page
    try:
        driver.get("https://store.steampowered.com/login/")
    except Exception as e:
        debug_log(
            driver, "Failed to load page!\nCheck if the URL is correct: {url}")
        log(f"Error msg: \n {str(e)}")
        return False
    
    # Wait for document to load
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        slow()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for page to load")
        driver.quit()
        return False

    # Detect login div
    try:
        # Find all div elements with class containing "newlogindialog"
        login_div = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'newlogindialog')]")))
    except TimeoutException as e:
        debug_log(driver, "Timed out waiting for steam login form")
        return False
    
    # Get username and password from the user
    username = input("Enter your username: ")
    password = input("Enter your password (not stored): ")

    # Fill in username
    try:
        login_input = login_div.find_element(
            By.XPATH, ".//input[@type='text']")
        login_input.send_keys(username)
    except NoSuchElementException:
        debug_log(driver, "Failed to find username input")
        return False
    
    # Fill in password
    try:
        login_password = login_div.find_element(
            By.XPATH, ".//input[@type='password']")
        login_password.send_keys(password)
    except NoSuchElementException:
        debug_log(driver, "Failed to find username input")
        return False
    
    #  Find submit button
    try:
        submit_button = login_div.find_element(
            By.XPATH, ".//button[@type='submit']")
        submit_button.click()
    except NoSuchElementException:
        debug_log(driver, "Failed to find submit button")
        return False

    # Check if 2FA is enabled
    two_factor = input("Do you have 2FA enabled? (y/n): ")
    # If 2FA is enabled, ask and input the code
    if two_factor.lower() == "y":

        # Some users get a confirm sign in dialog, others an input box
        try:
            wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[(@class='newlogindialog_AwaitingMobileConfText_7LmnT')]")))
            input("Press enter after you have confirmed the login on your phone")
        except TimeoutException:
            two_factor_code = input("Enter your 2FA code: ")
            if len(two_factor_code) != 5:
                log(driver, "2FA code must be 5 digits long")
                return False
            
            # split input into an array of characters
            two_factor_code_list = list(two_factor_code)
            try:
                two_factor_inputs = login_div.find_elements(
                    By.XPATH, ".//input[@type='text']")
                
                for char, input_element in zip(two_factor_code_list, two_factor_inputs):
                    input_element.send_keys(char)
                
            except NoSuchElementException:
                debug_log(driver, "Failed to find 2FA input")
                return False


    # Check if login was successful
    try:
        wait.until(lambda driver: "steamLoginSecure" in [cookie["name"] for cookie in driver.get_cookies()])
    except TimeoutException:
        return False

    return True


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
        if args.incognito:
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
        print("Driver test successful")
    except:
        print("Failed to test the driver!\nCheck if the browser and driver paths are correct")
        driver.quit()
        exit()

    # Login to steam
    if not steam_login(driver):
        print("Failed to login to steam!")
        driver.quit()
        exit()
    else:
        print("Login successful")

    # Return driver
    return driver