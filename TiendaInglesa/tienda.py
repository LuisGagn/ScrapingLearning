# Scrape Tienda Inglesa usando Selenium y BeautifulSoup.
# Utilizaremos BS para scrapear una lista con todas las URL de la pagina web.
# Luego evaluaremos como funciona la pagina web para analizar como realizar un scrape de cada item mediante pagination.
# Una vez terminado probaremos realizar el scrape usando Playwright ya que segun investigue, es mas rapido.

# Test 1: Pagina -> Limpieza, Items Totales: 740, Items totales Scrapeados 740 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import csv


service = Service(executable_path="chromedriver.exe")
options = webdriver.ChromeOptions() # Optimiza la velocidad de carga
options.add_argument('--headless')
driver = webdriver.Chrome(service=service)

# Ver y realizar todo automatico
def GetUrls(url):
    driver.get(url)
    links =[]
    urls = driver.find_elements(By.CLASS_NAME, 'id_category_button')

    for url in urls:
        links.append(url.get_attribute('href'))



    with open('urls.csv', "w", newline="", encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
    
        for link in links:
            csv_writer.writerow([link])


# GetUrls('https://www.tiendainglesa.com.uy/')



def ScrapeItems(url):
    driver.get(url)
    
    wait = WebDriverWait(driver, 10)

    while True:
            try:
                # Como las URL, Nombres y precios estan en un mismo DIV por item los agrupamos todos
                itemDivs = driver.find_elements(By.CLASS_NAME, 'card-product-name-and-price')
                items = [] # Para realizar el csv_writer de manera mas eficaz

                for div in itemDivs:
                    try: # En caso de un error que continue
                        link = div.find_element(By.TAG_NAME, 'a')
                        href = link.get_attribute('href')
                        itemName = div.find_element(By.CLASS_NAME, 'card-product-name')
                        itemPrice = div.find_element(By.CLASS_NAME, 'ProductPrice')
                        items.append([itemName.text, itemPrice.text, href])
                    except Exception as e:
                        print(e)
                        continue
                csv_writer.writerows(items)
                # Si llegamos a la ultima pagina que cierre y no scrapee mas
                if len(driver.find_elements(By.CSS_SELECTOR, 'span.wPageSelectorDisable#W0074TEXTBLOCK12')) > 0:
                    print("No hay mas paginas")
                    break
            
                # Toma el indicador final, espera que cargue y lo clickea.
                next = wait.until(EC.element_to_be_clickable((By.ID, 'W0074TEXTBLOCK12')))
                next.click()

                time.sleep(1)
            except Exception as e:
                print(e)
                break

    


# Escribe los items.
with open('items.csv', 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Item', 'Precio', 'URL'])
    try:
        ScrapeItems('https://www.tiendainglesa.com.uy/supermercado/categoria/limpieza/1895')
    finally:
        driver.quit()

    

