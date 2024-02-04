import os
import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
from classes import XMLProcessor, XMLFileCreator

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XML Processor GUI")
        self.xml_processor = None
        self.destination_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source', 'copies')
        self.selected_file = None


        # ! Botones ! #
        
        # Botón para seleccionar un archivo XML
        self.btn_browse = tk.Button(self, text="Seleccionar Archivo XML", command=self.load_and_process_xml)
        self.btn_browse.pack(pady=10)
        
        # ! Secciones ! #
        
        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.file_listbox.pack(pady=10)
        # Asignar la función "doble click"
        self.file_listbox.bind("<Double-1>", self.on_file_selected)
        
         # Botones de ejemplo
        self.btn_example_1 = tk.Button(self, text="Botón 1", command=lambda: self.on_button_click(1))
        self.btn_example_1.pack(pady=5)
        self.btn_example_1["state"] = "disabled"  # Inicialmente deshabilitado

        self.btn_example_2 = tk.Button(self, text="Botón 2", command=lambda: self.on_button_click(2))
        self.btn_example_2.pack(pady=5)
        self.btn_example_2["state"] = "disabled"  # Inicialmente deshabilitado

        self.btn_example_3 = tk.Button(self, text="Botón 3", command=lambda: self.on_button_click(3))
        self.btn_example_3.pack(pady=5)
        self.btn_example_3["state"] = "disabled"  # Inicialmente deshabilitado
        
        self.update_file_list()
         

    def load_and_process_xml(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
        if file_path:
            self.xml_processor = XMLProcessor(file_path)
            self.xml_processor.parse_xml()
            self.xml_processor.find_root_description()
            
            if self.xml_processor.description:
                # Crea una copia del archivo utilizando XMLFileCreator
                creator = XMLFileCreator(self.xml_processor)
                copied_file_path = creator.create_file(self.destination_folder)
                self.update_file_list()
    
    def update_file_list(self):
        # Borra elementos antiguos de la lista
        self.file_listbox.delete(0, tk.END)

        # Obtiene la lista de archivos en source/copies
        file_names = os.listdir(self.destination_folder)

        # Agrega los nombres de los archivos a la lista
        for file_name in file_names:
            self.file_listbox.insert(tk.END, file_name)
            
        if file_names:
            self.btn_example_1["state"] = "normal"
            self.btn_example_2["state"] = "normal"
            self.btn_example_3["state"] = "normal"
        else:
            # Si no hay archivos, deshabilita los botones
            self.btn_example_1["state"] = "disabled"
            self.btn_example_2["state"] = "disabled"
            self.btn_example_3["state"] = "disabled"
    
    def on_file_selected(self, event):
        # Obtiene el índice del elemento seleccionado
        selected_index = self.file_listbox.curselection()
        if selected_index:
            self.selected_file = self.file_listbox.get(selected_index)
            print(f"Archivo seleccionado: {self.selected_file}")

    def on_button_click(self, button_number):
        print(f"Botón {button_number} clickeado para el archivo {self.selected_file}")
            
    
if __name__ == "__main__":
    app = GUI()
    app.mainloop()