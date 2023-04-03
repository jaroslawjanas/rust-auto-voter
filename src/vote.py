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
from src.logs import debug_log


def vote_on_server(url, cookies):

    # Get driver
    driver = get_driver()

    # Load page
    try:
        driver.get(url)
    except:
        debug_log(driver, "Failed to load page!\nCheck if the URL is correct: {url}")
        driver.quit()
        return False

    # Wait for document to load
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    except TimeoutException:
        debug_log(driver, "Timed out waiting for page to load")
        driver.quit()
        return False

    # Wait for cookies prompt to load and accapt
    try:
        wait = WebDriverWait(driver, 10)
        cookies_accept = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[(@id='cookiescript_accept')]")))
        cookies_accept.click()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for cookies prompt to load")
        driver.quit()
        return False

    # Wait for the button to be clickable and click
    try:
        wait = WebDriverWait(driver, 10)
        vote_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[(@title='Vote')]")))
        vote_button.click()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for button to be clickable")
        driver.quit()
        return False

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
        debug_log(driver, "Timed out waiting for/filling in Steam form")
        driver.quit()
        return False

    # Wait for steam to load
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    except TimeoutException:
        debug_log(driver, "Timed out waiting for Steam to load")
        driver.quit()
        return False

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
        debug_log(driver, "Timed out waiting for steam login form to load")
        driver.quit()
        return False

    # Selenium look for h1 with text "Vote Confirmation"
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(), 'Vote Confirmation')]")))
        debug_log(driver, "Vote successful!")
        driver.quit()
        return True
    except TimeoutException:
        debug_log(driver, "Timed out waiting for vote confirmation")
        driver.quit()
        return False