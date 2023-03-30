# Start
from selenium.webdriver.chrome.options import Options
from src.driver_setup import get_driver

# Locators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Exceptions
from selenium.common.exceptions import TimeoutException

# Other
from src.args import args

def vote_on_server(url, cookies):

    options = Options()
    if not args.debug:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=960,960")
    options.add_argument("--incognito")
    options.add_argument("--disable-cloud-management")

    # Get driver
    driver = get_driver(options)

    # Load page
    try:
        driver.get(url)
    except:
        print(f"Failed to load page!\nCheck if the URL is correct: {url}")
        driver.quit()
        return

    # Wait for document to load
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

    # Wait for cookies prompt to load and accapt
    try:
        wait = WebDriverWait(driver, 10)
        cookies_accept = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[(@id='cookiescript_accept')]")))
        cookies_accept.click()
    except TimeoutException:
        print("Timed out waiting for cookies prompt to load")
        driver.quit()

    # Wait for the button to be clickable and click
    try:
        wait = WebDriverWait(driver, 10)
        vote_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[(@title='Vote')]")))
        vote_button.click()
    except TimeoutException:
        print("Timed out waiting for button to be clickable")
        driver.quit()

    # Steam Form
    try:
        wait = WebDriverWait(driver, 10)
        steam_form = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//form[(@name='steam_form')]")))
        form_checkbox = steam_form.find_element(
            By.XPATH, ".//input[(@class='form-check-input')]")
        form_checkbox.click()
        steam_form.submit()
    except TimeoutException:
        print("Timed out waiting for/filling in Steam form")
        driver.quit()

    # Wait for steam to load
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    except TimeoutException:
        print("Timed out waiting for Steam to load")
        driver.quit()

    # Add cookies
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Reload page
    driver.refresh()

    # Wait for steam login form to load
    try:
        wait = WebDriverWait(driver, 10)
        login_form = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//form[(@name='loginForm')]")))
        login_form.submit()
    except TimeoutException:
        print("Timed out waiting for steam login form to load")
        driver.quit()

    # Selenium look for h1 with text "Vote Confirmation"
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(), 'Vote Confirmation')]")))
        driver.quit()
        return True
    except TimeoutException:
        print("Timed out waiting for vote confirmation")
        driver.quit()
        return False