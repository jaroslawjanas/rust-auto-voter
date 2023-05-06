from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.debug import slow
from src. logs import debug_log, log


def action_sequence(driver, url):

    # Timeout
    wait = WebDriverWait(driver, 10)

    # Load page
    try:
        driver.get(url)
    except:
        debug_log(
            driver, "Failed to load page!\nCheck if the URL is correct: {url}")
        return False

    # Wait for document to load
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        slow()
    except TimeoutException:
        debug_log(driver, "Timed out waiting for page to load")
        return False
    
    return None