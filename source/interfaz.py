import os

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk

from classes import XMLProcessor, XMLFileCreator

# TODO: Class to select the type of party (move to a separate file)
class PartyTypeDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Seleccionar Tipo de Party")
        self.geometry("300x100")

        self.party_type = None  # <- variable to store the selected party type
        
        # GUI configuration
        
        # Create a style object
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use the clam theme
        
        # Configure the style
        self.style.configure(".", background="#f0f0f0")  
        self.style.configure("TButton", padding=5, font=('Helvetica', 10), foreground="#333333")  
        self.style.map("TButton", background=[("active", "#dddddd")])

        label = ttk.Label(self, text="Seleccione el tipo de party:")
        label.pack(pady=10)

        # Supplier button
        btn_supplier = ttk.Button(
            self, text="Supplier", command=lambda: self.set_party_type("supplier"))
        btn_supplier.pack(side="left", padx=5)

        # Customer button
        btn_customer = ttk.Button(
            self, text="Customer", command=lambda: self.set_party_type("customer"))
        btn_customer.pack(side="right", padx=5)

    def set_party_type(self, party_type):
        self.party_type = party_type
        self.destroy()  # <- close the dialog


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XML Processor GUI")
        self.geometry("600x400")
        self.xml_processor = None
        
        # Llamar a los métodos para crear las carpetas necesarias
        self.create_copies_folder()
        self.create_csv_folder()

        self.destination_folder = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'copies')

        self.destination_folder_2 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'csv')

        self.selected_file = None
        self.selected_csv_file = None
        
        # GUI configuration
        
        # Create a style object
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use the clam theme
        
        # Configure the style
        self.style.configure(".", background="#f0f0f0")  
        self.style.configure("TButton", padding=5, font=('Helvetica', 10), foreground="#333333")  
        self.style.map("TButton", background=[("active", "#dddddd")])

        # ! Sections ! #

          # Button to select the XML file
        self.btn_browse = ttk.Button(self, text="Seleccionar Archivo XML", 
                                    command=self.load_and_process_xml)
        self.btn_browse.pack(pady=10, anchor="center")
        
        # Create a frame for the function buttons
        self.function_buttons_frame = tk.Frame(self)
        self.function_buttons_frame.pack(side="top", fill="x", anchor="center")
        
        # Refresh button
        self.btn_refresh = ttk.Button(self.function_buttons_frame, text="Actualiza", 
                                    command=lambda: self.update_file_list())
        self.btn_refresh.pack(side="left", padx=(100, 25), pady=5 ,ipadx=50, ipady=5)

        # Delete button
        self.btn_delete = ttk.Button(self.function_buttons_frame, text="Eliminar", 
                                    command=self.delete_file_list)
        self.btn_delete.pack(side="left", padx=(10, 50), ipadx=50, pady=5, ipady=5)

        # Separator
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x")

        # List box to show the XML files
        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.file_listbox.pack(side="left", padx=(25, 10), fill="none", expand=True,)
        self.file_listbox.bind("<Double-1>", self.on_file_selected)

        # List box to show the CSV files
        self.csv_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.csv_listbox.pack(side="left", padx=(0, 10), fill="none", expand=True)
        self.csv_listbox.bind("<Double-1>", self.on_csv_selected)

        # ! functions buttons ! #

        # Crear el frame para los botones
        self.function_buttons_frame = tk.Frame(self)
        self.function_buttons_frame.pack(side="right", padx=(0, 10), pady=50, anchor="ne")  # Alineado a la derecha

        # QR button
        self.btn_example_1 = ttk.Button(self.function_buttons_frame, text="Encontrar QR", 
                                        command=lambda: self.on_button_click(1), width=20) 
        self.btn_example_1.pack(pady=(0, 5), anchor="center")
        self.btn_example_1["state"] = "disabled"

        # Items button
        self.btn_example_2 = ttk.Button(self.function_buttons_frame, text="Encontrar items", 
                                        command=lambda: self.on_button_click(2), width=20) 
        self.btn_example_2.pack(pady=5, anchor="center")
        self.btn_example_2["state"] = "disabled"

        # Party info button
        self.btn_example_3 = ttk.Button(self.function_buttons_frame, text="Encontrar información",
                                        command=lambda: self.on_button_click(3), width=20) 
        self.btn_example_3.pack(pady=5, anchor="center")
        self.btn_example_3["state"] = "disabled"

        self.btn_select_csv_folder = ttk.Button(self.function_buttons_frame, text="Seleccionar Carpeta para CSV",
                                                command=self.select_csv_folder)
        self.btn_select_csv_folder.pack(pady=5)

        self.update_file_list()  # <- update the file list when the app starts
    
    # Funtion for loading and processing the XML file
    def load_and_process_xml(self):
        # Open a file dialog to select the XML file
        file_path = filedialog.askopenfilename(
            filetypes=[("XML Files", "*.xml")])
        
        if file_path:
            # Create a XMLProcessor object with the selected file
            self.xml_processor = self.file_parser(file_path)  # <- call the file_parser function
            self.xml_processor.find_root_description() # <- call the find_root_description method

            if self.xml_processor.description:
                # Create a new XML file with the description
                creator = XMLFileCreator(self.xml_processor) # <- create a XMLFileCreator object
                copied_file_path = creator.create_file(self.destination_folder)  # <- call the create_file method
                self.update_file_list()  # <- update the file list

    # Function to parse the XML file
    def file_parser(self, file_path):
        processor = XMLProcessor(file_path)
        processor.parse_xml()
        return processor  # <- return the processor object

    # Function to update the file list
    def update_file_list(self):
        # Clear the listbox
        self.file_listbox.delete(0, tk.END)
        self.csv_listbox.delete(0, tk.END)

        # Get the names of the files in the destination folder
        file_names = os.listdir(self.destination_folder)

        # Add the file names to the listbox
        for file_name in file_names:
            self.file_listbox.insert(tk.END, file_name)  # <- inserts
            
        csv_file_names = os.listdir(self.destination_folder_2)
        for csv_file_name in csv_file_names:
            self.csv_listbox.insert(tk.END, csv_file_name)

        # block or unblock the buttons
        if file_names:
            self.btn_example_1["state"] = "normal"
            self.btn_example_2["state"] = "normal"
            self.btn_example_3["state"] = "normal"
        else:
            # if there are no files, block the buttons
            self.btn_example_1["state"] = "disabled"
            self.btn_example_2["state"] = "disabled"
            self.btn_example_3["state"] = "disabled"

    # Function to delete the selected file
    def delete_file_list(self):
        select_index = self.file_listbox.curselection()
        select_csv_index = self.csv_listbox.curselection()
        
        if select_index:
            # Get the file name
            select_file = self.file_listbox.get(select_index)
            # Build the file path
            file_path = os.path.join(self.destination_folder, select_file)
            try:
                # Delete the file
                os.remove(file_path)
                print(f"Archivo eliminado: {select_file}")
                # Update the file list
                self.update_file_list()
            except OSError as e:
                print(f"Error al eliminar el archivo: {e}")
        
        if select_csv_index:
            select_csv_file = self.csv_listbox.get(select_csv_index)
            csv_file_path = os.path.join(self.destination_folder_2, select_csv_file)
            try:
                os.remove(csv_file_path)
                print(f"Archivo CSV eliminado: {select_csv_file}")
                self.update_file_list()
            except OSError as e:
                print(f"Error al eliminar el archivo CSV: {e}")
                
      # Function to remove the extension from the file name
    
    # Function to remove the extension from the file name
    def remove_extension_xml(self, select_index):
        # Get the file name
        select_file = self.file_listbox.get(select_index)
        new_name = select_file.replace('.xml', '') # <- remove the extension
        new_name = new_name.replace('copia', '') # <- remove the 'copia' phrase
        new_name = new_name.replace('-', '') # <- remove the '-' phrase
        return new_name
    
    # Function to handle the event when a file is selected
    def on_file_selected(self, event):
        # Get the index of the selected item
        selected_index = self.file_listbox.curselection()
        if selected_index:
            # Get the file name
            self.selected_file = self.file_listbox.get(selected_index)
            # Enable the delete button
            self.btn_delete["state"] = "normal"
            print(f"Archivo seleccionado: {self.selected_file}")
            return True
    
    # Function to handle the event when a CSV file is selected
    def on_csv_selected(self, event):
        selected_index = self.csv_listbox.curselection()
        if selected_index:
            self.selected_csv_file = self.csv_listbox.get(selected_index)
            print(f"Archivo CSV seleccionado: {self.selected_csv_file}")
            return True

    # Function to handle the event when a button is clicked
    def on_button_click(self, button_number):
        # If a button is clicked, and a file is selected
        if button_number == 1 and self.selected_file:
            # Create a XMLProcessor object with the selected file
            file_path = os.path.join(self.destination_folder, self.selected_file)
            self.xml_processor = self.file_parser(file_path) # <- Create the path to parser the file with the selected file and the destination folder
            
            # find the QR code
            qr_code = self.xml_processor.find_qr_code()  # <- call the find_qr_code method
            print(f"Código QR: {qr_code}")

        elif button_number == 2 and self.selected_file:
            # Get the index of the selected item
            select_index = self.file_listbox.curselection()
            new_name = self.remove_extension_xml(select_index)
            
            # Create a XMLProcessor object with the selected file
            file_path = os.path.join(self.destination_folder, self.selected_file)
            self.xml_processor = self.file_parser(file_path)
            
            # Find the items
            invoice_items = self.xml_processor.find_invoice_items() # <- call the find_invoice_items method

            # Create a new XMLFileCreator object
            creator = XMLFileCreator(self.xml_processor)
            creator.create_csv_file(
                self.destination_folder_2, invoice_items, new_name)
            
            self.update_file_list()

        elif button_number == 3 and self.selected_file:
            # Show the dialog to select the party type
            party_dialog = PartyTypeDialog(self)
            self.wait_window(party_dialog)  # <- wait for the dialog to close

            # If the party type is selected
            if party_dialog.party_type:
                # Get the index of the selected item
                select_index = self.file_listbox.curselection()
                # Get the party type
                party_type = party_dialog.party_type

                name = f"{party_type}-info-{self.remove_extension_xml(select_index)}"

                # Create a XMLProcessor object with the selected file
                file_path = os.path.join(self.destination_folder, self.selected_file)
                self.xml_processor = self.file_parser(file_path)
                
                party_info = self.xml_processor.find_party_info_items(party_type)  # <- call the find_party_info_items method

                creator = XMLFileCreator(self.xml_processor)
                creator.create_csv_file(self.destination_folder_2, party_info, name)
                
                self.update_file_list()
        else:
            messagebox.showinfo(message="Selecciona un archivo XML y presiona el botón para continuar.")
            
    # Functions to create the structure folders
    # For default, the copies folder will be created in the same directory as the program
    def create_copies_folder(self):
        actual_path = os.path.abspath(os.path.dirname(__file__))
        
        copies_folder = os.path.join(actual_path, 'copies')
        
        if not os.path.exists(copies_folder):
            os.makedirs(copies_folder)
            return os.path.join(actual_path, 'copies')
        else:
            print("La carpeta ya existe")        
    
    def create_csv_folder(self):
        actual_path = os.path.abspath(os.path.dirname(__file__))
        
        csv_folder = os.path.join(actual_path, 'csv')
        
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)
            return os.path.join(actual_path, 'csv')
        else:
            print("La carpeta ya existe #2")

    # Function to select the CSV folder
    # In this case, the user can select the folder where the CSV files will be saved
    def select_csv_folder(self):
            folder_selected = filedialog.askdirectory()
            if folder_selected:
                self.destination_folder_2 = folder_selected
                print(f"Directorio CSV seleccionado: {self.destination_folder_2}")
                messagebox.showinfo("Información", f"Directorio CSV seleccionado: {self.destination_folder_2}")
            else:
                print("No se seleccionó ninguna carpeta para los archivos CSV.")

    # !!!
    # TODO: Add a function to open the CSV file or any other file
    # !!!
    
if __name__ == "__main__":
    app = GUI()
    app.mainloop()
