
import time
import os
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Function to introduce a random sleep to mimic human behavior
def random_sleep(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Setup Chrome options for stealth
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--disable-images")

# Start the Chrome driver with the modified options
driver = webdriver.Chrome(options=chrome_options)
print('Lancement de Chrome')

driver.get('https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=clown&ou=Bretignolles+sur+Mer+%2885470%29&univers=pagesjaunes&idOu=L08503500')
random_sleep(2, 4)

# Function to check if CAPTCHA is present on the page
def is_captcha_present():
    try:
        driver.find_element(By.ID, "challenge-running")
        return True
    except NoSuchElementException:
        return False

# Check for CAPTCHA and wait for user to solve it manually
while is_captcha_present():
    print("CAPTCHA detected. Please solve it manually.")
    random_sleep(15, 20)

print("CAPTCHA solved or not present.")
driver.find_element(By.CLASS_NAME, "didomi-continue-without-agreeing").click()
random_sleep(2, 4)

data = []
print('Récupération des données en cours...')
posts = driver.find_elements(By.CSS_SELECTOR, ".bi-generic")

for post in posts:
    nom = post.find_element(By.CSS_SELECTOR, ".bi-content h3").text
    adresse = post.find_element(By.CLASS_NAME, "bi-address").text
    secteur = post.find_element(By.CLASS_NAME, "bi-activity-unit").text

    lien_page_dediee = post.find_element(By.CLASS_NAME, "bi-denomination").get_attribute("href")
    post.find_element(By.CLASS_NAME, "bi-denomination").click()
    random_sleep(3, 5)

    try:
        lien_site = driver.find_element(By.CSS_SELECTOR, ".lvs-container a").get_attribute("href")
    except NoSuchElementException:
        lien_site = None

    data.append({
        "Secteur": secteur,
        "Nom": nom,
        "Adresse": adresse,
        "Lien Page dédiée": lien_page_dediee,
        "Site Web": lien_site
    })

    driver.back()
    random_sleep(1, 2)

if os.path.exists("donnees_professionnels.xlsx"):
    old_data = pd.read_excel("donnees_professionnels.xlsx", engine='openpyxl')
    new_data = pd.DataFrame(data)
    df = pd.concat([old_data, new_data], ignore_index=True)
    print("Données ajoutées au fichier Xml...")
else:
    print("Création d'un fichier XMLX en cours...")
    df = pd.DataFrame(data)

df.to_excel("donnees_professionnels.xlsx", index=False, engine='openpyxl')

driver.quit()
print('Processus terminée.')
