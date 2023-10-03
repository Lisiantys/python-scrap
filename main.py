import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utilities import random_sleep, start, smooth_scroll, close_popup, one_scroll_on_page

print('Lancement de Chrome')

# lance le navigateur à la page dédiée

data = []

driver = start()
driver.get("https://www.paruvendu.fr/immobilier/annonceimmofo/liste/listeAnnonces?tt=5&tbApp=1&tbDup=1&tbChb=1&tbLof=1&tbAtl=1&tbPla=1&at=1&pa=FR&lol=15&ddlFiltres=nofilter&codeINSEE=,33126,")
random_sleep(2, 3)
link_element = driver.find_element(By.XPATH, "//a[@onclick='cmp_pv.ui.showVendors()']")
link_element.click()
random_sleep(1, 2)
button = driver.find_element(By.XPATH, "//button[@onclick='cmp_pv.ui.switchAllPurposes(false);']")
button.click()
random_sleep(2, 3)

posts = driver.find_elements(By.CSS_SELECTOR, ".border-1.border-grey-75.shadow-xl.hover\\:shadow-2xl.bg-white.relative.p-4.sm\\:p-2")

print('Récupération des données en cours...')

initial_step = 150
step_increment = 150

for post in posts: 

    url = post.find_element(By.CSS_SELECTOR, ".flex.sm\\:block.gap-4 a").get_attribute('href')
    random_sleep(0.5, 1)
    driver.get(url)
    random_sleep(1, 2)
    close_popup(driver)
    random_sleep(1, 2)
    one_scroll_on_page(driver)
   
    try:  
        prix_element = driver.find_element(By.CSS_SELECTOR, "#autoprix")
        prix = prix_element.text.split("\n")[0]
    except NoSuchElementException: 
        prix = None  

    try:  
        titre = driver.find_element(By.CSS_SELECTOR, "#detail_h1").text
    except NoSuchElementException: 
        titre = None  
    
    try:  
        lieu = driver.find_element(By.CSS_SELECTOR, "#detail_loc").text
    except NoSuchElementException: 
        lieu = None  
    
    try:  
        sous_titre = driver.find_element(By.CSS_SELECTOR, ".autodetail-titre.sepdetail14-ssbordure").text
    except NoSuchElementException: 
        sous_titre = None  

    try:  
        description = driver.find_element(By.CSS_SELECTOR, "#txtAnnonceTrunc").text
    except NoSuchElementException: 
        description = None  

    random_sleep(1, 2)

    driver.back()
    random_sleep(2, 3)
    smooth_scroll(driver, step=initial_step)

    # Incrémentez le step pour la prochaine itération de la boucle principale
    initial_step += step_increment

    data.append({
        "url": url,
        "prix": prix,
        "titre": titre,
        "sous-titre": sous_titre,
        "lieu": lieu,
        "description": description
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