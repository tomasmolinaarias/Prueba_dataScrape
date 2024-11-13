import re
from PyPDF2 import PdfReader
import unicodedata
import os
import json

# Función para normalizar el texto eliminando acentos y caracteres especiales
def normalize_text(text):
    normalized_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return normalized_text

# Función para extraer nombres y RUTs desde el PDF
def extract_users_from_pdf(pdf_path):
    users = []
    reader = PdfReader(pdf_path)
    # Ajustar el patrón para coincidir con los RUTs del PDF
    rut_pattern = re.compile(r'(\d{1,2}\.\d{3}\.\d{3})\s*-\s*([0-9Kk])')

    # Recorrer cada página del PDF
    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            print(f"Texto extraído de la página {page_number + 1}:\n{text}\n")  # Mostrar el texto extraído para depurar
            lines = text.split('\n')
            for line in lines:
                match = rut_pattern.search(line)
                if match:
                    rut = match.group(0).replace('.', '').replace(' ', '')
                    name = line.replace(match.group(0), '').strip()
                    name = normalize_text(name)  # Normalizar el nombre eliminando acentos
                    users.append({"rut": rut, "name": name})

    return users

# Uso del código para extraer los datos del PDF
pdf_path = "C:/Users/Administrador/Desktop/diagram AFP/SCRAPINGafp/src/app/archive/pdf/personal_data.pdf"
users = extract_users_from_pdf(pdf_path)

# Verificar si se extrajeron datos
if users:
    # Crear la carpeta de salida si no existe
    output_dir = "C:/Users/Administrador/Desktop/diagram AFP/SCRAPINGafp/src/app/archive/json/date_pdf"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Contar el número de archivos existentes en la carpeta para numerar el nuevo archivo
    existing_files = len([name for name in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, name))])
    output_file_path = os.path.join(output_dir, f"resultado_extraccion__PDF.{existing_files + 1}.json")

    # Imprimir los resultados
    print("Datos extraídos:")
    for user in users:
        print(f"RUT: {user['rut']}, Nombre: {user['name']}")

    # Guardar los resultados en un archivo JSON
    with open(output_file_path, 'w') as file:
        json.dump(users, file, indent=4)

    print(f"Extracción de datos completada y guardada en '{output_file_path}'.")
else:
    print("No se encontraron RUTs en el PDF.")
