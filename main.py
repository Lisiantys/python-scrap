import time
import os
import random
import time
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

driver.get('https://www.artisans-du-batiment.com/trouver-un-artisan-qualifie/?job=architecte+int%C3%A9rieur&place=85470')
arrayLength = 24
random_sleep(1, 2) # Let the user actually see something!

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
    random_sleep(0.5, 2)  # Check every 5 seconds

print("CAPTCHA solved or not present.")
time.sleep(3)
print('Récupération des données en cours...')

data = []
last_num_posts = 0

while len(data) < arrayLength:  # Continue until we have 24 posts
    
    # Wait for new content to load
    random_sleep(0.5, 1)  # Wait for 2-3 seconds
    
    # Get the current posts
    posts = driver.find_elements(By.CSS_SELECTOR, ".a-artisanTease")
    
    for post in posts[last_num_posts:]:  # Only process new posts
        nom = post.find_element(By.CSS_SELECTOR, ".a-artisanTease__name span").text
        adresse = post.find_element(By.CSS_SELECTOR, ".a-artisanTease__address span").text

        try:  # IF there is a web site link / facebook link
            email = post.find_element(By.CSS_SELECTOR, ".a-artisanTease__mail a").text
        except NoSuchElementException:  # If no link was found
            email = None  # Default value = None = No text in xml file

        # Store the data
        data.append({
            "Nom": nom,
            "Adresse": adresse,
            "email" : email
        })

        # Scroll down a fixed amount
        driver.execute_script("window.scrollBy(0, 150);")  # Scroll by 500 pixels
        
        random_sleep(0.5, 1) 
        print(f"Processed: {nom}")
    
    # Update the last_num_posts
    last_num_posts = len(posts)


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