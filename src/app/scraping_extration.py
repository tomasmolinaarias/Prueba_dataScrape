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
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Función para realizar scraping de la página de afiliación usando Selenium (sin mostrar el navegador)
def scrape_afp_data_selenium(rut):
    # Configurar el navegador Chrome con un User-Agent aleatorio y en modo headless
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        # Abrir la página de consulta de afiliación
        url = "https://www.spensiones.cl/apps/certificados/formConsultaAfiliacion.php"
        driver.get(url)
        print(f"Navegador abierto en: {url}")

        # Ingresar el RUT en el campo correspondiente
        rut_input = driver.find_element(By.ID, "rut")
        rut_input.clear()
        rut_input.send_keys(rut)
        print(f"RUT ingresado: {rut}")

        # Hacer clic en el botón de búsqueda
        search_button = driver.find_element(By.ID, "btn_buscar")
        search_button.click()
        print(f"Botón de búsqueda presionado para RUT: {rut}")

        # Esperar hasta que la información de resultados esté disponible
        wait = WebDriverWait(driver, 8)  # Esperar hasta 8 segundos
        afp_info_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#main > div > div:nth-child(2) > div > div.panel.panel-body > div:nth-child(1) > p:nth-child(1)")))
        afp_info = afp_info_element.text
        print(f"Datos obtenidos para RUT {rut}: {afp_info}")

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

# Cargar los usuarios desde el archivo JSON generado anteriormente
input_dir = "C:/Users/Administrador/Desktop/diagram AFP/SCRAPINGafp/src/app/archive/json/date_pdf"
input_files = [f for f in os.listdir(input_dir) if f.startswith('resultado_extraccion_') and f.endswith('.json')]
input_files.sort(key=lambda x: int(re.search(r'\d+', x).group()), reverse=True)
input_json_path = os.path.join(input_dir, input_files[0])

with open(input_json_path, 'r') as file:
    users = json.load(file)

# Ruta para guardar el registro de consultas
consulta_log_path = "C:/Users/Administrador/Desktop/diagram AFP/SCRAPINGafp/src/app/archive/json/Historial_consulta/consulta_log.json"

# Cargar o inicializar el registro de consultas
if os.path.exists(consulta_log_path):
    with open(consulta_log_path, 'r') as log_file:
        consulta_log = json.load(log_file)
else:
    consulta_log = []

# Filtrar consultas realizadas en las últimas 24 horas
consulta_log = [entry for entry in consulta_log if datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S") > datetime.now() - timedelta(hours=24)]

# Verificar si se extrajeron datos
if users:
    # Crear la carpeta de salida si no existe
    output_dir = "C:/Users/Administrador/Desktop/diagram AFP/SCRAPINGafp/src/app/archive/json/date_scraping"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Contar el número de archivos existentes en la carpeta para numerar el nuevo archivo
    existing_files = len([name for name in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, name))])
    output_file_path = os.path.join(output_dir, f"resultado_extraccion_SCRAPING.{existing_files + 1}.json")

    # Imprimir los resultados
    print("Datos extraídos:")
    consultas_realizadas = len(consulta_log)
    for idx, user in enumerate(users):
        if consultas_realizadas >= 100:
            print("Se alcanzó el límite de 100 consultas en 24 horas. Esperando hasta que se pueda continuar...")
            # Calcular el tiempo restante hasta que se cumplan las 24 horas
            tiempo_restante = (datetime.strptime(consulta_log[0]['timestamp'], "%Y-%m-%d %H:%M:%S") + timedelta(hours=24)) - datetime.now()
            time.sleep(tiempo_restante.total_seconds())
            consultas_realizadas = 0
            consulta_log = []
        print(f"RUT: {user['rut']}, Nombre: {user['name']}")
        # Realizar scraping para obtener la información de la AFP usando Selenium
        afp, fecha = scrape_afp_data_selenium(user['rut'])
        if afp is not None and fecha is not None:
            consultas_realizadas += 1
            consulta_log.append({"rut": user['rut'], "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        user["afiliacion"] = afp
        user["fecha"] = fecha
        # Agregar un pequeño retraso aleatorio para evitar sobrecargar el servidor y simular comportamiento humano
        time.sleep(random.uniform(1, 3))

    # Guardar los resultados en un archivo JSON
    with open(output_file_path, 'w') as file:
        json.dump(users, file, indent=4)

    # Guardar el registro de consultas actualizado
    with open(consulta_log_path, 'w') as log_file:
        json.dump(consulta_log, log_file, indent=4)

    print(f"Extracción de datos completada y guardada en '{output_file_path}'.")
else:
    print("No se encontraron RUTs en el archivo JSON.")