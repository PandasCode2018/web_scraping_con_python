import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Constantes  

class WebScraping:
    
    def __init__(self, url):
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=1920,1200")
        self.service = Service(executable_path=Constantes.DRIVER_PATH)
        self.url = url
        self.driver = True
    
    def start(self):
        try:
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            self.driver.get(self.url)
            print(f"Navegando a {self.url}")
        except Exception as e:
            print(f"Ocurrió un error al iniciar el WebDriver: {e}")
    
    def stop(self):
        if self.driver:
            self.driver.quit()
            print("WebDriver cerrado.")
    
    def save_to_file(self, product_name, product_price):
        os.makedirs('resultados', exist_ok=True)
        file_path = os.path.join('resultados', 'producto.txt')

        try:
            with open(file_path, 'a', encoding='utf-8') as file:  # Cambiado a 'a' para agregar
                file.write(f"Nombre del producto: {product_name}\n")
                file.write(f"Precio del producto: {product_price}\n")
                file.write("\n")  # Añadir una línea en blanco entre entradas
                print(f"Datos guardados en {file_path}.")
        except Exception as e:
            print(f"Ocurrió un error al guardar los datos: {e}")

    def scrape_products(self):
        while True:
            try:
                products = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-layout__item"))
                )
                
                for product in products:
                    try:
                        name_element = product.find_element(By.CSS_SELECTOR, ".poly-component__title a")
                        name = name_element.text
                        
                        price_element = product.find_element(By.CSS_SELECTOR, ".andes-money-amount--cents-superscript")
                        price = price_element.text
                        
                        # Llamar al método para guardar los datos
                        self.save_to_file(name, price)

                    except Exception as inner_e:
                        print(f"Ocurrió un error al extraer datos del producto: {inner_e}")

                # Busca el botón "Siguiente" y navega a la siguiente página
                try:
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "andes-pagination__button--next"))
                    )
                    if "andes-pagination__button--next" in next_button.get_attribute("class"):
                        link = next_button.find_element(By.TAG_NAME, "a")
                        if not link.is_enabled():  # Verifica si el enlace está habilitado
                            print("No hay más páginas para navegar.")
                            break
                        
                        link.click()
                        print("Navegando a la siguiente página...")
                        products = WebDriverWait(self.driver, 10).until( EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ui-search-layout__item"))
                )
                       
                except Exception as e:
                    print("No se pudo encontrar el botón 'Siguiente':", e)
                    break  # Sale del bucle si no se puede hacer clic en "Siguiente"

            except Exception as e:
                print(f"Ocurrió un error al extraer datos: {e}")
                break

if __name__ == "__main__":
    web_driver = WebScraping(Constantes.URL)
    web_driver.start()
    web_driver.scrape_products()
    web_driver.stop()
