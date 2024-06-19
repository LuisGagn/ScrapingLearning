# Scrape Tienda Inglesa usando Selenium y BeautifulSoup.
# Utilizaremos BS para scrapear una lista con todas las URL de la pagina web.
# Luego evaluaremos como funciona la pagina web para analizar como realizar un scrape de cada item mediante pagination.
# Una vez terminado probaremos realizar el scrape usando Playwright ya que segun investigue, es mas rapido.

# Objetivos: 
# Scrapear 1 categoria entera ✅
# Scrapear Ofertas ✅


# Test 1: Pagina -> Limpieza, Items Totales: 740, Items totales Scrapeados 740 
# Test 2: Scrapeo de ofertas general; 3412 Items scrapeados, total items existentes: 3412
# Data is legit.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import csv


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Ver y realizar todo automatico
def GetUrls(url):
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    links =[]
    categorias = []
    definitivo = []
    catDivs = driver.find_elements(By.CLASS_NAME, 'id_category_button')

    for cat in catDivs:
        links.append(cat.get_attribute('href'))
        categorias.append(cat.get_attribute('aria-label'))
    
    with open('urls.csv', "w", newline="", encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Categoria', 'LVL 1', 'LVL 2'])

        for link, categoria in zip(links,categorias):
            driver.get(link)
            items = driver.find_elements(By.CSS_SELECTOR, '[data-gx-evt-control="THIRDLEVELTABLE"]')
            
            
            for i in range(len(items)):
                    items = driver.find_elements(By.CSS_SELECTOR, '[data-gx-evt-control="THIRDLEVELTABLE"]')
                    item = items[i]

                    subcategoria = item.find_element(By.XPATH, ".//*[contains(@id, 'TXTTHIRDCATEGORYDESCRIPTION')]").text
                    urlActual = driver.current_url
                    next = wait.until(EC.element_to_be_clickable(item))
                    next.click()
                    time.sleep(1)

                    definitivo.append([categoria, subcategoria, urlActual])
                    
                    driver.back()       
            for lv3 in definitivo:
                csv_writer.writerow(lv3)
                
            definitivo = []




GetUrls('https://www.tiendainglesa.com.uy/')



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
                        precioOferta = '0'  
                        itemPrice = div.find_element(By.CLASS_NAME, 'ProductPrice')

                        try:
                            itemPrice = div.find_element(By.CLASS_NAME, 'wTxtProductPriceBefore')
                            precioOferta = div.find_element(By.CLASS_NAME, 'ProductPrice').text
                        except:
                            pass

                            

                        items.append([itemName.text, itemPrice.text, precioOferta, href])

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

    


#Escribe los items.
with open('items.csv', 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Item', 'Precio', 'Precio Oferta', 'URL'])
    try:
       ScrapeItems('https://www.tiendainglesa.com.uy/supermercado/listas/ofertas/3716')
    finally:
       driver.quit()

    

