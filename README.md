# Requisitos para ejecutar el script de extracción de datos y scraping de AFP

Este documento proporciona una guía sobre las herramientas y bibliotecas que deben instalarse para ejecutar el script correctamente.

## Requisitos previos

1. **Python**: Asegúrate de tener Python 3.9.7 (u otra versión compatible) instalado en tu sistema. Puedes descargarlo desde [Python.org](https://www.python.org/downloads/).

2. **Gestor de Paquetes `pip`**: Python debería venir con `pip` incluido. Puedes verificarlo ejecutando:
   ```sh
   pip --version
   ```

3. **Google Chrome**: El script utiliza Google Chrome para automatizar el scraping de la web. Descarga la última versión de Chrome desde [aquí](https://www.google.com/chrome/).

## Instalación de bibliotecas

Para que el script funcione, necesitas instalar las siguientes bibliotecas de Python. Puedes instalarlas ejecutando los siguientes comandos en la terminal:

1. **Selenium**: Para automatizar la navegación web.
   ```sh
   pip install selenium
   ```

2. **Webdriver Manager**: Para gestionar automáticamente el controlador de Chrome.
   ```sh
   pip install webdriver-manager
   ```

3. **PyPDF2**: Para extraer datos de los archivos PDF.
   ```sh
   pip install PyPDF2
   ```

4. **Pillow**: Para manejar imágenes si es necesario (aunque no se usa directamente en este script).
   ```sh
   pip install Pillow
   ```

5. **Unicodedata**: Este módulo viene incluido en la instalación de Python, por lo que no necesitas instalarlo manualmente.

## Archivos requeridos

Asegúrate de tener los siguientes archivos en las ubicaciones correctas:

- **Archivo PDF** con los datos personales: Debe estar ubicado en `./src/app/archive/pdf/personal_data.pdf`.
- **Archivos JSON** para almacenar los resultados de extracción y scraping:
  - Carpeta de salida para extracción PDF: `./src/app/archive/json/date_pdf/`
  - Carpeta de salida para scraping: `./src/app/archive/json/date_scraping/`
  - Carpeta para el historial de consultas: `./src/app/archive/json/Historial_consulta/`

## Ejecución del script

1. Clona el repositorio o asegúrate de tener todos los archivos necesarios.
2. Navega hasta el directorio donde se encuentra el script `scraping_extration.py`.
3. Ejecuta el script usando Python:
   ```sh
   python scraping_extration.py
   ```

## Notas adicionales

- **Límite de consultas**: El script está diseñado para realizar un máximo de 100 consultas por cada 24 horas para evitar bloqueos del sitio web.
- **User-Agent**: El script utiliza un User-Agent aleatorio para simular un navegador real y evitar bloqueos automáticos por parte del servidor.

Si experimentas algún problema o error, asegúrate de que todas las dependencias estén instaladas y que los archivos estén en sus ubicaciones respectivas.

