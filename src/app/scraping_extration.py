import re
import os
import json
import time
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
from webdriver_manager.chrome import ChromeDriverManager

class Scraper:
    def __init__(self):
        self.input_dir = "./src/app/archive/json/date_pdf"
        self.output_dir = "./src/app/archive/json/date_scraping"
        self.consulta_log_path = "./src/app/archive/json/Historial_consulta/consulta_log.json"
        self.users = []
        self.consulta_log = []

    def scrape_afp_data_selenium(self, rut):
        # Configurar el navegador Chrome con un User-Agent aleatorio y en modo headless
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-proxy-server")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            # Abrir la página de consulta de afiliación
            url = "https://www.spensiones.cl/apps/certificados/formConsultaAfiliacion.php"
            driver.get(url)

            # Ingresar el RUT en el campo correspondiente
            rut_input = driver.find_element(By.ID, "rut")
            rut_input.clear()
            rut_input.send_keys(rut)

            # Hacer clic en el botón de búsqueda
            search_button = driver.find_element(By.ID, "btn_buscar")
            search_button.click()

            # Esperar hasta que la información de resultados esté disponible
            wait = WebDriverWait(driver, 15)  # Aumentar el tiempo de espera
            afp_info_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#main > div > div:nth-child(2) > div > div.panel.panel-body > div:nth-child(1) > p:nth-child(1)")))
            afp_info = afp_info_element.text

            # Extraer la afiliación y la fecha de ingreso del texto
            afp_match = re.search(r'incorporado\(a\) a (AFP \w+),', afp_info)
            fecha_match = re.search(r'con fecha (\d{1,2} de \w+ de \d{4})', afp_info)
            afp = afp_match.group(1) if afp_match else None
            fecha = fecha_match.group(1) if fecha_match else None

            return afp, fecha
        except Exception as e:
            print(f"Error al realizar la solicitud para el RUT {rut}: {e}")
            return None, None
        finally:
            # Cerrar el navegador
            driver.quit()

    def load_users_from_json(self):
        input_files = [f for f in os.listdir(self.input_dir) if f.endswith('.json')]
        input_files.sort(key=lambda x: int(re.search(r'\d+', x).group()), reverse=True)
        if input_files:
            latest_json_path = os.path.join(self.input_dir, input_files[0])
            with open(latest_json_path, 'r') as file:
                self.users = json.load(file)

    def load_consulta_log(self):
        if os.path.exists(self.consulta_log_path):
            with open(self.consulta_log_path, 'r') as log_file:
                self.consulta_log = json.load(log_file)
        else:
            self.consulta_log = []

        self.consulta_log = [entry for entry in self.consulta_log if datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S") > datetime.now() - timedelta(hours=24)]

    def save_results_to_json(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        existing_files = len([name for name in os.listdir(self.output_dir) if os.path.isfile(os.path.join(self.output_dir, name))])
        output_file_path = os.path.join(self.output_dir, f"resultado_extraccion_SCRAPING.{existing_files + 1}.json")

        with open(output_file_path, 'w') as file:
            json.dump(self.users, file, indent=4)

        with open(self.consulta_log_path, 'w') as log_file:
            json.dump(self.consulta_log, log_file, indent=4)

        print(f"Extracción de datos completada y guardada en '{output_file_path}'.")

    def process_users(self):
        self.load_users_from_json()
        self.load_consulta_log()

        if self.users:
            print("Datos extraídos:")
            consultas_realizadas = len(self.consulta_log)
            tasks = []

            start_time = time.time()  # Registrar el tiempo de inicio del scraping

            with ThreadPoolExecutor(max_workers=5) as executor:
                for idx, user in enumerate(self.users):
                    if consultas_realizadas >= 100:
                        print("Se alcanzó el límite de 100 consultas en 24 horas. Avisar al usuario.")
                        break
                    print(f"Procesando RUT: {user['__rut']}, Nombre: {user['__name']}")
                    tasks.append(executor.submit(self.scrape_afp_data_selenium, user['__rut']))

                for future, user in zip(as_completed(tasks), self.users):
                    afp, fecha = future.result()
                    if afp is not None and fecha is not None:
                        consultas_realizadas += 1
                        self.consulta_log.append({"rut": user['__rut'], "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    user["afiliacion"] = afp
                    user["fecha"] = fecha

            end_time = time.time()  # Registrar el tiempo de finalización del scraping
            total_time = end_time - start_time
            print(f"Tiempo total de scraping: {total_time:.2f} segundos.")

            self.save_results_to_json()
            print("JSON de scraping listo.")
        else:
            print("No se encontraron RUTs en el archivo JSON.")
