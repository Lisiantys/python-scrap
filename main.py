import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import pandas as pd

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=comedien&ou=Bretignolles+sur+Mer+%2885470%29&univers=pagesjaunes&idOu=L08503500')
time.sleep(3) # Let the user actually see something!
driver.find_element(By.CLASS_NAME, "didomi-continue-without-agreeing").click()
time.sleep(5) # Let the user actually see something!
data = []

professionnels = driver.find_elements(By.CSS_SELECTOR, ".bi-generic")  # Remplacez par le bon sélecteur

for i in range(len(professionnels)):
    pro = driver.find_elements(By.CSS_SELECTOR, ".bi-generic")[i]
    nom = pro.find_element(By.CSS_SELECTOR, ".bi-content h3").text
    adresse = pro.find_element(By.CLASS_NAME, "bi-address").text
    secteur = pro.find_element(By.CLASS_NAME, "bi-activity-unit").text

    # Accéder à la page dédiée
    lien_page_dediee = pro.find_element(By.CLASS_NAME, "bi-denomination").get_attribute("href")
    pro.find_element(By.CLASS_NAME, "bi-denomination").click()
    time.sleep(3)

    # Supposons que sur la page dédiée, il y a un lien vers le site du carreleur avec le texte "Visitez notre site"
    try:
        lien_site = driver.find_element(By.CSS_SELECTOR, ".teaser-item .value").get_attribute("href")
    except NoSuchElementException:  # Si le lien n'est pas trouvé
        lien_site = None  # Vous pouvez définir lien_site à None ou à une autre valeur par défaut


    # Stocker les informations
    data.append({
        "Nom": nom,
        "Adresse": adresse,
        "Secteur": secteur,
        "Lien Page dédiée": lien_page_dediee,
        "Site Web": lien_site
    })

    # Retourner en arrière pour continuer le scraping
    driver.back()
    time.sleep(2)

    # Créer un DataFrame à partir des données collectées
    df = pd.DataFrame(data)

    # Enregistrer le DataFrame dans un fichier Excel
    df.to_excel("donnees_professionnels.xlsx", index=False, engine='openpyxl')


driver.quit()