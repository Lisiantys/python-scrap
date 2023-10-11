import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



import time
from utilities import random_sleep, start

print('Lancement de Chrome')

# lance le navigateur à la page dédiée

def handle_modal(driver):
    try:
        # Attendre que le modal apparaisse
        modal_button = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.ID, "tarteaucitronAllDenied2"))
        )
        modal_button.click()
    except:
        # Si le modal n'apparaît pas dans les 4 secondes, passez
        pass



data = []
urls = [
    "https://chambre-notaires-vendee.notaires.fr/annuaire-notaires?langs%5B0%5D=18&departments%5B0%5D=6&displayList=1&page=1", 
    "https://chambre-notaires-vendee.notaires.fr/annuaire-notaires?langs%5B0%5D=18&departments%5B0%5D=6&displayList=1&page=2", 
    "https://chambre-notaires-vendee.notaires.fr/annuaire-notaires?langs%5B0%5D=18&departments%5B0%5D=6&displayList=1&page=3", 
    "https://chambre-notaires-vendee.notaires.fr/annuaire-notaires?langs%5B0%5D=18&departments%5B0%5D=6&displayList=1&page=4", 
    "https://chambre-notaires-vendee.notaires.fr/annuaire-notaires?langs%5B0%5D=18&departments%5B0%5D=6&displayList=1&page=5", 
    "https://chambre-notaires-vendee.notaires.fr/annuaire-notaires?langs%5B0%5D=18&departments%5B0%5D=6&displayList=1&page=6", 
    "https://chambre-notaires-vendee.notaires.fr/annuaire-notaires?langs%5B0%5D=18&departments%5B0%5D=6&displayList=1&page=7"
]

driver = start()

print('Récupération des données en cours...')


# for url in urls: 

driver.get("https://www.udaf85.fr/les-associations-de-udaf/annuaire-des-associations/")
random_sleep(1, 2)

def scroll_incrementally(driver, increment=650, delay=0.5, times=8):
    for _ in range(times):
        driver.execute_script(f"window.scrollBy(0, {increment});")
        time.sleep(delay)

    # Appel à la méthode pour effectuer le défilement
scroll_incrementally(driver)

# Maintenant, récupérez tous les éléments
posts = driver.find_elements(By.CSS_SELECTOR, "div.card--association-large")
print('Nombre de posts trouvés:', len(posts))
print('Récupération des données en cours...')

for post in posts: 
    try:
        title = post.find_element(By.CSS_SELECTOR, ".card__title a").text
    except NoSuchElementException:
        title = None
        
    try:
        adresse = post.find_element(By.CSS_SELECTOR, ".list-btn-contact__address span span").text
    except NoSuchElementException:
        adresse = None

    try:
        email_button = post.find_element(By.CSS_SELECTOR, "a.btn-show-content.btn-email")
        actions = ActionChains(driver)
        actions.move_to_element(email_button).perform()  # This will scroll the view to the email button
        email_button.click()
        random_sleep(0.5, 0.8)
        email = post.find_element(By.CSS_SELECTOR, "a[href^='mailto:']").get_attribute('href').replace('mailto:', '')
        print(email)
    except NoSuchElementException:
        email = None

    data.append({
        "Nom": title,
        "Adresse": adresse,
        "email": email,
    })

    random_sleep(0.5, 1) 


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