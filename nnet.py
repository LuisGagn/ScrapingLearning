from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import csv

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# abre la pagina en el navegador



def scrapear(url): 
    driver.get(url) 
    categoria = url.split('/')[3]
    # Toma la altura maxima del documento
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # Devuelve altura actualizada
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    items = driver.find_elements(By.CSS_SELECTOR, '[itemprop="name"]')
    unidades = driver.find_elements(By.CLASS_NAME, 'pmoneda')
    precios = driver.find_elements(By.CSS_SELECTOR, '[itemprop="price"]')

    for item, unidad, precio in zip(items, unidades, precios):
        csv_writer.writerow([categoria, item.text, unidad.text, precio.text])


with open('items.csv', "w", newline="", encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Categoria', 'Item', 'Moneda', 'Precio'])

    try:

        with open('urls.txt', 'r') as file:
            for line in file:
                url = line.strip()
                if url: 
                    scrapear(url)
    
    finally:
        driver.quit()
