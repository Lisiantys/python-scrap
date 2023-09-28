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
def random_sleep(min_seconds=1, max_seconds=20):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Setup Chrome options for stealth
chrome_options = Options()
chrome_options.add_argument("user-agent=Chrome/117.0.5938.92")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--start-maximized")  # Start browser maximized to look more like a real user
chrome_options.add_argument("--disable-infobars") # Disable infobars
chrome_options.add_argument("--incognito")  # Launch browser in incognito mode

# Start the Chrome driver with the modified options
driver = webdriver.Chrome(options=chrome_options)
print('Lancement de Chrome')

driver.get('https://www.artisans-du-batiment.com/')
random_sleep(2, 5) # Let the user actually see something!

# Function to check if CAPTCHA is present on the page
def is_captcha_present():
    try:
        # This is just an example, you'd need to find the actual CAPTCHA element's selector
        driver.find_element(By.ID, "challenge-running")
        return True
    except NoSuchElementException:
        return False

# Check for CAPTCHA and wait for user to solve it manually
while is_captcha_present():
    print("CAPTCHA detected. Please solve it manually.")
    random_sleep(15, 20)  # Check every 5 seconds

print("CAPTCHA solved or not present.")

# Remplir le champ "Métier" (job)
job_input = driver.find_element(By.NAME, "job")
job_input.send_keys("maçon")  # Remplacez par le métier souhaité
random_sleep(1, 4)

# Remplir le champ "Lieu" (place)
place_input = driver.find_element(By.NAME, "place")
place_input.send_keys("85340")  # Remplacez par la ville souhaitée
random_sleep(2, 5)
# Appuyer sur la touche "Entrée" pour lancer la recherche
place_input.send_keys(Keys.ENTER)
random_sleep(3, 5)

data = []
print('Récupération des données en cours...')

posts = driver.find_elements(By.CSS_SELECTOR, ".a-artisanTease")

for post in posts:
    nom = post.find_element(By.CSS_SELECTOR, ".a-artisanTease__name span").text
    adresse = post.find_element(By.CSS_SELECTOR, ".a-artisanTease__address span").text
    secteur = job_input
    email = post.find_element(By.CSS_SELECTOR, ".a-artisanTease__address a").get_attribute("href")

    random_sleep(2, 4)

    # try:  # IF there is a web site link / facebook link
    #     lien_site = driver.find_element(By.CSS_SELECTOR, ".lvs-container a .value").text
    #     if lien_site and not lien_site.startswith("www."):
    #         lien_site = "www." + lien_site
    # except NoSuchElementException:  # If no link was found
    #     lien_site = None  # Default value = None = No text in xml file

    # Store the data
    data.append({
        "Secteur": secteur,
        "Nom": nom,
        "Adresse": adresse,
        "email" : email
    })

    random_sleep(1, 4)

# Check if the Excel file already exists
if os.path.exists("donnees_professionnels.xlsx"):
    # Load existing data
    old_data = pd.read_excel("donnees_professionnels.xlsx", engine='openpyxl')
    # Create a DataFrame from the new scraped data
    new_data = pd.DataFrame(data)
    # Append new data to the old data
    df = pd.concat([old_data, new_data], ignore_index=True)
    print("Données ajoutées au fichier Xml...")
else:
    print("Création d'un fichier XMLX en cours...")
    # If the file does not exist, just create a DataFrame from the new scraped data
    df = pd.DataFrame(data)
    

# Save the DataFrame to an Excel file
df.to_excel("donnees_professionnels.xlsx", index=False, engine='openpyxl')

driver.quit()
print('Processus terminée.')