import time
import os
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from utilities import random_sleep, start, error

print('Lancement de Chrome')

# lance le navigateur à la page dédiée
driver = start()
driver.get('https://www.annuairehotels.fr/hotel/?c=&departement=vendee')
error(driver)
time.sleep(3)

print('Récupération des données en cours...')
data = []

random_sleep(0.5, 1) 

posts = driver.find_elements(By.CSS_SELECTOR, ".entreprises-card")

for post in posts: 
    nom = post.find_element(By.CSS_SELECTOR, ".entreprises-card-title").text
    url = post.get_attribute('href')
    random_sleep(0.5, 1)
    driver.get(url)

    try:  
        # Localiser l'élément contenant l'e-mail
        email_element = driver.find_element(By.XPATH, "//div[@class='col'][.//i[@class='fa fa-envelope']]")

        # Extraire le texte de l'élément
        email_text = email_element.text

        # Séparer le texte pour obtenir l'adresse e-mail
        email = email_text.split(': ')[1]

        print(email)  # Cela devrait afficher "reservations@hotel-omnubo.com"

    except NoSuchElementException: 
        email = None  

    try:  
        # Localiser l'élément contenant l'e-mail
        adress_element = driver.find_element(By.XPATH, "//div[@class='col'][.//i[@class='fa fa-map-marked']]")

        # Extraire le texte de l'élément
        adress = adress_element.text

        print(adress)  # Cela devrait afficher "reservations@hotel-omnubo.com"

    except NoSuchElementException: 
        adress = None  

    data.append({
        "Nom": nom,
        "Adress": adress,
        "email" : email,
        "url": url
    })
    
    random_sleep(0.5, 1) 
    print(f"Processed: {nom}")

    driver.back()

   
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