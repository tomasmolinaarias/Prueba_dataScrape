import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
import re
import pandas as pd
from src.app.data_extraction import PdfDataExtractor
from src.app.scraping_extration import Scraper

class PdfScrapingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Subir PDF para Extracción y Análisis de Datos")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        self.extractor = PdfDataExtractor()
        self.scraper = Scraper()
        self.create_widgets()

    def create_widgets(self):
        # Encabezado
        header_label = tk.Label(self.root, text="Extracción y Análisis de Datos desde PDF",
                                font=("Helvetica", 18, "bold"), pady=15, bg="#f0f0f0", fg="#333")
        header_label.pack()

        # Marco para el botón de carga de PDF
        upload_frame = tk.Frame(self.root, bg="#ffffff", relief="groove", bd=2)
        upload_frame.pack(pady=15, padx=10, fill="x")

        # Botón para subir el PDF
        self.upload_button = tk.Button(upload_frame, text="Subir PDF", command=self.upload_pdf,
                                       font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
        self.upload_button.pack(pady=10)

        # Caja de texto para mostrar información general
        self.text_box = tk.Text(self.root, height=10, width=110, font=("Courier", 10), bg="#f9f9f9", wrap="word")
        self.text_box.pack(pady=15, padx=10)

        # Etiqueta y campo de búsqueda
        search_frame = tk.Frame(self.root, bg="#ffffff", relief="groove", bd=2)
        search_frame.pack(pady=10, padx=10, fill="x")

        search_label = tk.Label(search_frame, text="Buscar por afiliación (ej. Modelo, Capital):", font=("Helvetica", 12), bg="#ffffff")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.search_entry = ttk.Entry(search_frame, font=("Helvetica", 12), width=30)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)
        self.search_entry.bind('<KeyRelease>', self.search_by_afp)  # Buscar en tiempo real

        # Botón para exportar los datos a Excel
        self.export_button = tk.Button(search_frame, text="Exportar a Excel", command=self.export_to_excel,
                                       font=("Helvetica", 12), bg="#2196F3", fg="white", padx=20, pady=5)
        self.export_button.grid(row=0, column=2, padx=10, pady=10)

        # Tabla para mostrar resultados
        table_frame = tk.Frame(self.root, bg="#ffffff", relief="groove", bd=2)
        table_frame.pack(pady=15, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("RUT", "Nombre", "Afiliación", "Fecha"), show="headings")
        self.tree.heading("RUT", text="RUT")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Afiliación", text="Afiliación")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.column("RUT", width=150)
        self.tree.column("Nombre", width=250)
        self.tree.column("Afiliación", width=150)
        self.tree.column("Fecha", width=150)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Estilo para la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)

    def upload_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            # Renombrar el archivo PDF y moverlo al directorio adecuado
            renamed_pdf_path = self.extractor.rename_and_save_pdf(self.pdf_path)
            self.text_box.insert(tk.END, f"PDF cargado y renombrado: {renamed_pdf_path}\n")
            self.extract_data(renamed_pdf_path)  # Extraer datos automáticamente después de cargar el PDF

    def extract_data(self, pdf_path):
        # Extraer usuarios desde el PDF subido
        users = self.extractor.extract_users_from_pdf(pdf_path)

        if users:
            # Crear la carpeta de salida si no existe
            output_dir = "./src/app/archive/json/date_pdf"
            self.extractor.save_users_to_json(users, output_dir, os.path.basename(pdf_path))
            self.text_box.insert(tk.END, f"Extracción de datos completada y guardada en '{output_dir}'.\n")

            # Ejecutar el scraping con el archivo JSON generado
            self.scraper.process_users()
            self.text_box.insert(tk.END, "Scraping completado y datos obtenidos guardados.\n")
            self.display_users()  # Mostrar los datos extraídos en la tabla
        else:
            self.text_box.insert(tk.END, "No se encontraron RUTs en el PDF.\n")

    def display_users(self):
        # Limpiar la tabla antes de mostrar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Cargar el último archivo JSON generado por el scraping
        scraping_dir = "./src/app/archive/json/date_scraping"
        scraping_files = [f for f in os.listdir(scraping_dir) if f.startswith('resultado_extraccion_SCRAPING') and f.endswith('.json')]
        scraping_files.sort(key=lambda x: int(re.search(r'\d+', x).group()), reverse=True)
        if scraping_files:
            latest_scraping_file = scraping_files[0]
            scraping_json_path = os.path.join(scraping_dir, latest_scraping_file)
            with open(scraping_json_path, 'r') as file:
                users = json.load(file)

            # Mostrar los datos en la tabla
            for user in users:
                self.tree.insert("", "end", values=(user['__rut'], user['__name'], user['afiliacion'], user['fecha']))

    def search_by_afp(self, event):
        afp_to_search = self.search_entry.get().strip().lower()
        if not afp_to_search:
            # Si el cuadro de búsqueda está vacío, mostrar todos los usuarios
            self.display_users()
            return

        # Limpiar la tabla antes de mostrar resultados de búsqueda
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Cargar el último archivo JSON generado por el scraping
        scraping_dir = "./src/app/archive/json/date_scraping"
        scraping_files = [f for f in os.listdir(scraping_dir) if f.startswith('resultado_extraccion_SCRAPING') and f.endswith('.json')]
        scraping_files.sort(key=lambda x: int(re.search(r'\d+', x).group()), reverse=True)
        if scraping_files:
            latest_scraping_file = scraping_files[0]
            scraping_json_path = os.path.join(scraping_dir, latest_scraping_file)
            with open(scraping_json_path, 'r') as file:
                users = json.load(file)

            # Filtrar los usuarios por afiliación que contenga el término de búsqueda
            filtered_users = [user for user in users if afp_to_search in user['afiliacion'].lower()]

            # Mostrar los resultados filtrados en la tabla
            for user in filtered_users:
                self.tree.insert("", "end", values=(user['__rut'], user['__name'], user['afiliacion'], user['fecha']))

    def export_to_excel(self):
        # Cargar el último archivo JSON generado por el scraping
        scraping_dir = "./src/app/archive/json/date_scraping"
        scraping_files = [f for f in os.listdir(scraping_dir) if f.startswith('resultado_extraccion_SCRAPING') and f.endswith('.json')]
        scraping_files.sort(key=lambda x: int(re.search(r'\d+', x).group()), reverse=True)
        if scraping_files:
            latest_scraping_file = scraping_files[0]
            scraping_json_path = os.path.join(scraping_dir, latest_scraping_file)
            with open(scraping_json_path, 'r') as file:
                users = json.load(file)

            # Crear un DataFrame con los datos
            df = pd.DataFrame(users)

            # Seleccionar el archivo de salida
            export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])
            if export_file_path:
                # Guardar los datos en un archivo Excel
                df.to_excel(export_file_path, index=False)
                messagebox.showinfo("Exportación Exitosa", f"Los datos se han exportado exitosamente a '{export_file_path}'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PdfScrapingApp(root)
    root.mainloop()
