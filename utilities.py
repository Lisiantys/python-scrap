import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.92 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.92 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.92 Safari/537.36 OPR/77.0.4054.203"
]

def random_sleep(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def start():
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    chrome_options.add_argument("--start-maximized")  # Start browser maximized to look more like a real user
    chrome_options.add_argument("--incognito")  # Launch browser in incognito mode
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def button_exists(driver):
    try:
        # Attendez jusqu'à 5 secondes pour voir si le bouton est présent
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "reload-button")))
        return True
    except TimeoutException:
        return False

def error(driver):
    while button_exists(driver):
        random_sleep(1, 2)
        button = driver.find_element(By.ID, "reload-button")
        button.click()
        random_sleep(1, 2)

    random_sleep(1, 2)

