# README - Instalación de Dependencias para la Aplicación

Esta guía te ayudará a instalar todas las dependencias necesarias para que la aplicación funcione correctamente. Sigue los pasos a continuación para configurar tu entorno de desarrollo.

## Requisitos Previos

- **Python 3.9 o superior**: La aplicación está escrita en Python, por lo que necesitas tener Python instalado.
- **Pip**: El gestor de paquetes de Python, normalmente incluido con la instalación de Python.
- **Entorno Virtual (opcional)**: Se recomienda utilizar un entorno virtual para evitar conflictos de versiones de dependencias.

## Instalación de Dependencias

Para instalar todas las bibliotecas necesarias, sigue los siguientes pasos:

1. **Clonar el Repositorio**
   
   Clona este repositorio en tu computadora local:
   ```sh
   git clone https://github.com/tomasmolinaarias/Prueba_dataScrape
   cd Prueba_dataScrape
   ```

2. **Crear y Activar un Entorno Virtual** (opcional pero recomendado)
   
   Crear un entorno virtual para instalar las dependencias:
   ```sh
   python -m venv .venv
   ```

   Activar el entorno virtual:
   - En Windows:
     ```sh
     .\.venv\Scripts\activate
     ```
   - En MacOS/Linux:
     ```sh
     source .venv/bin/activate
     ```

3. **Instalar las Dependencias**

   Ejecuta el siguiente comando para instalar todas las bibliotecas requeridas para la aplicación:
   ```sh
   pip install -r requirements.txt
   ```

   Si el archivo `requirements.txt` no está disponible, puedes instalar manualmente las siguientes dependencias:
   
   - **Tkinter**: Viene preinstalado con la mayoría de las distribuciones de Python.
   - **PyPDF2**: Para la extracción de datos de los archivos PDF.
     ```sh
     pip install PyPDF2
     ```
   - **Pandas**: Para la exportación de los datos en formato Excel.
     ```sh
     pip install pandas
     ```
   - **Selenium**: Para realizar scraping automático con el navegador.
     ```sh
     pip install selenium
     ```
   - **Webdriver-Manager**: Para gestionar la instalación del driver de Chrome.
     ```sh
     pip install webdriver-manager
     ```
   - **Openpyxl**: Necesario para trabajar con archivos Excel (.xlsx).
     ```sh
     pip install openpyxl
     ```
   - **Pyperclip**: Para copiar el RUT al portapapeles (si es necesario).
     ```sh
     pip install pyperclip
     ```

## Configuración Adicional

1. **WebDriver de Chrome**: Selenium necesita el WebDriver de Chrome para automatizar las tareas en el navegador.
   WebDriver-Manager se encarga de descargarlo automáticamente.

2. **Archivos PDF y JSON**: Asegúrate de tener una estructura de carpetas como se especifica en el código:
   - `src/app/archive/pdf/` para los archivos PDF subidos.
   - `src/app/archive/json/date_pdf/` para los JSON generados desde los PDF.
   - `src/app/archive/json/date_scraping/` para los resultados del scraping.

## Ejecución de la Aplicación

Después de instalar las dependencias, puedes ejecutar la aplicación usando el siguiente comando:
```sh
python app.py
```

## Botón de Copiar RUT

En la interfaz gráfica, al lado de cada RUT se encuentra un botón que permite copiar el RUT al portapapeles. Esto facilita la gestión de los datos extraídos del PDF.

## Notas
- **Google Chrome**: Necesitas tener Google Chrome instalado para que Selenium funcione correctamente.
- **Errores con dependencias**: Si encuentras problemas de módulos no encontrados, asegúrate de estar en el entorno virtual correcto y haber instalado todas las dependencias mencionadas.



