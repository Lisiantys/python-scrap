from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.artisans-du-batiment.com/trouver-un-artisan-qualifie/?job=Plombier&place=paris').text

soup = BeautifulSoup(html_text, 'lxml')
addresses = soup.find_all('div', class_='a-artisanTease__address')

for address_div in addresses:
    address_span = address_div.find('span')
    if address_span:
        print(address_span.text.strip())  # .strip() pour supprimer les espaces inutiles