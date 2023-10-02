import time
import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utilities import random_sleep, start, error

print('Lancement de Chrome')

# lance le navigateur à la page dédiée

data = []

driver = start()
driver.get("https://www.paruvendu.fr/immobilier/location/appartement/")
random_sleep(3, 4)
link_element = driver.find_element(By.XPATH, "//a[@onclick='cmp_pv.ui.showVendors()']")
link_element.click()
random_sleep(1, 2)
button = driver.find_element(By.XPATH, "//button[@onclick='cmp_pv.ui.switchAllPurposes(false);']")
button.click()
random_sleep(2, 3)

posts = driver.find_elements(By.CSS_SELECTOR, ".border-1.border-grey-75.shadow-xl.hover\\:shadow-2xl.bg-white.relative.p-4.sm\\:p-2.my-6")

print('Récupération des données en cours...')

for post in posts: 
    random_sleep(2, 4)
    # Supposons que `parent_element` est l'élément parent que vous avez déjà localisé
    prix_div = post.find_element(By.CSS_SELECTOR, "div.flex.justify-center.items-center > div")
    prix = prix_div.text.split()[0]  # Cela devrait vous donner "750 €"
    print(prix)

    # url = post.get_attribute('href')
    random_sleep(0.5, 1)
    # driver.get(url)

    # try:  
    #     # Localiser l'élément contenant l'e-mail
    #     email_element = driver.find_element(By.XPATH, "//div[@class='col'][.//i[@class='fa fa-envelope']]")

    #     # Extraire le texte de l'élément
    #     email_text = email_element.text

    #     # Séparer le texte pour obtenir l'adresse e-mail
    #     email = email_text.split(': ')[1]

    #     print(email)  # Cela devrait afficher "reservations@hotel-omnubo.com"

    # except NoSuchElementException: 
    #     email = None  

    # try:  
    #     # Localiser l'élément contenant l'e-mail
    #     adress_element = driver.find_element(By.XPATH, "//div[@class='col'][.//i[@class='fa fa-map-marked']]")

    #     # Extraire le texte de l'élément
    #     adress = adress_element.text

    #     print(adress)  # Cela devrait afficher "reservations@hotel-omnubo.com"

    # except NoSuchElementException: 
    #     adress = None  

    data.append({
        "prix": prix,
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