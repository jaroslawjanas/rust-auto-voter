# Start
from selenium.webdriver.chrome.options import Options
from src.driver_setup import get_driver

# Locators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Exceptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Other
from src.logs import debug_log
from src.debug import slow

def vote_on_server(url, cookies):

    # Get driver
    driver = get_driver()

    # Timeout
    wait = WebDriverWait(driver, 10)

    # Load page
    try:
        driver.get(url)
    except:
        debug_log(driver, "Failed to load page!\nCheck if the URL is correct: {url}")
        driver.quit()
        return False

    # Wait for document to load
    try:
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        slow()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for page to load")
        driver.quit()
        return False

    # Wait for cookies prompt to load and accapt
    try:
        cookies_accept = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[(@id='cookiescript_accept')]")))
        slow()
        cookies_accept.click()
        slow()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for cookies prompt to load")
        driver.quit()
        return False

    # Wait for the button to be clickable and click
    try:
        vote_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[(@title='Vote')]")))
        slow()
        vote_button.click()
        slow()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for button to be clickable")
        driver.quit()
        return False

    # Steam Form
    try:
        steam_form = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//form[(@name='steam_form')]")))
        form_checkbox = steam_form.find_element(
            By.XPATH, ".//input[(@class='form-check-input')]")
        slow()
        form_checkbox.click()
        slow()
        steam_form.submit()
        slow()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for/filling in Steam form")
        driver.quit()
        return False

    # Wait for steam to load
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        slow()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for Steam to load")
        driver.quit()
        return False

    # Add cookies
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Reload page
    driver.refresh()

    # Steam login
    try:
        # Wait for steam login form to load
        login_form = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//form[(@name='loginForm')]")))
        # Get the logged in user's name
        user_info = login_form.find_element(By.XPATH, ".//div[(@class='OpenID_loggedInAccount')]")
        debug_log(driver, f"Logged in as {user_info.text} ")
        slow()
        login_form.submit()
        slow()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for steam login form to load")
        driver.quit()
        return False
    except NoSuchElementException:
        debug_log(driver, "Failed to find logged in user's name, is the cookie correct?")
        driver.quit()

    # Selenium look for h1 with text "Vote Confirmation"
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(), 'Vote Confirmation')]")))
        debug_log(driver, "Vote successful!")
        slow()
        driver.quit()
        return True
    except TimeoutException:
        debug_log(driver, "Timed out waiting for vote confirmation")
        driver.quit()
        return False