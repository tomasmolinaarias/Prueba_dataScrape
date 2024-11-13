import re
from PyPDF2 import PdfReader
import unicodedata
import os
import json
from datetime import datetime
import shutil

class PdfDataExtractor:
    def __init__(self):
        pass

    # Función para normalizar el texto eliminando acentos y caracteres especiales
    def normalize_text(self, text):
        normalized_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        return normalized_text

    # Función para extraer nombres y RUTs desde el PDF
    def extract_users_from_pdf(self, pdf_path):
        users = []
        reader = PdfReader(pdf_path)
        # Ajustar el patrón para coincidir con los RUTs del PDF
        rut_pattern = re.compile(r'(\d{1,2}\.\d{3}\.\d{3})\s*-\s*([0-9Kk])')

        # Recorrer cada página del PDF
        for page_number, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
               #  print(f"Texto extraído de la página {page_number + 1}:\n{text}\n")  # Mostrar el texto extraído para depurar
                lines = text.split('\n')
                for line in lines:
                    match = rut_pattern.search(line)
                    if match:
                        __rut = match.group(0).replace('.', '').replace(' ', '')
                        __name = line.replace(match.group(0), '').strip()
                        __name = self.normalize_text(__name)  # Normalizar el nombre eliminando acentos
                        users.append({"__rut": __rut, "__name": __name})

        return users

    # Función para guardar los usuarios extraídos en un archivo JSON
    def save_users_to_json(self, users, output_dir, pdf_name):
        if users:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Crear el nombre del archivo JSON basado en el nombre del PDF
            json_file_name = pdf_name.replace('.pdf', '.json')
            output_file_path = os.path.join(output_dir, json_file_name)

            # Guardar los resultados en un archivo JSON
            with open(output_file_path, 'w') as file:
                json.dump(users, file, indent=4)

            print(f"Extracción de datos completada y guardada en '{output_file_path}'.")
        else:
            print("No se encontraron RUTs en el PDF.")

    # Función para renombrar y guardar el PDF con el formato adecuado
    def rename_and_save_pdf(self, pdf_path):
        output_dir = "./src/app/archive/pdf"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        today = datetime.now().strftime("%d_%m_%Y")
        # Obtener el número progresivo del documento
        existing_files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
        document_number = len(existing_files) + 1
        new_pdf_name = f"{today}.{document_number}.pdf"
        new_pdf_path = os.path.join(output_dir, new_pdf_name)

        # Copiar el archivo PDF en lugar de renombrarlo
        shutil.copy2(pdf_path, new_pdf_path)
        print(f"PDF copiado y guardado en: {new_pdf_path}")

        return new_pdf_path
