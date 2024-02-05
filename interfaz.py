import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from classes import XMLProcessor, XMLFileCreator

# Class to select the type of party (todo: move to a separate file)
class PartyTypeDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Seleccionar Tipo de Party")
        self.geometry("300x100")

        self.party_type = None  # <- variable to store the selected party type

        label = tk.Label(self, text="Seleccione el tipo de party:")
        label.pack(pady=10)

        # Supplier button
        btn_supplier = tk.Button(self, text="Supplier", command=lambda: self.set_party_type("supplier"))
        btn_supplier.pack(side="left", padx=10)

        # Customer button
        btn_customer = tk.Button(self, text="Customer", command=lambda: self.set_party_type("customer"))
        btn_customer.pack(side="right", padx=10)

    def set_party_type(self, party_type):
        self.party_type = party_type
        self.destroy() # <- close the dialog

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XML Processor GUI")
        self.xml_processor = None
        self.destination_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source', 'copies')
        self.destination_folder_2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source', 'csv')
        self.selected_file = None
        
        # Botón para seleccionar un archivo XML
        self.btn_browse = tk.Button(self, text="Seleccionar Archivo XML", command=self.load_and_process_xml)
        self.btn_browse.pack(pady=10)
        
        # ! Sections ! #
        
        # Refresh button
        self.btn_refresh = tk.Button(self, text="Actualiza", command=lambda: self.update_file_list())
        self.btn_refresh.pack(pady=5)
        
        # List box to show the files
        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.file_listbox.pack(pady=10)
        # Assign the event to the listbox (double click)
        self.file_listbox.bind("<Double-1>", self.on_file_selected)
        
        # funtion buttons
        self.btn_example_1 = tk.Button(self, text="Encontrar QR", command=lambda: self.on_button_click(1))  # <- button 1 (QR)
        self.btn_example_1.pack(pady=5)
        self.btn_example_1["state"] = "disabled"  

        self.btn_example_2 = tk.Button(self, text="Encontrar items", command=lambda: self.on_button_click(2)) # <- button 2 (items)
        self.btn_example_2.pack(pady=5)
        self.btn_example_2["state"] = "disabled"  

        self.btn_example_3 = tk.Button(self, text="Encontrar información", command=lambda: self.on_button_click(3)) # <- button 3 (party info)
        self.btn_example_3.pack(pady=5)
        self.btn_example_3["state"] = "disabled"  
        
        self.update_file_list() # <- update the file list when the app starts
         
    # Funtion for loading and processing the XML file
    def load_and_process_xml(self):
        # Open a file dialog to select the XML file
        file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
        if file_path:
            # Create a XMLProcessor object with the selected file
            self.xml_processor = self.file_parser(file_path) # <- call the file_parser function
            self.xml_processor.find_root_description() # <- call the find_root_description method
            
            if self.xml_processor.description:
                # Create a new XML file with the description
                creator = XMLFileCreator(self.xml_processor) # <- create a XMLFileCreator object
                copied_file_path = creator.create_file(self.destination_folder) # <- call the create_file method
                self.update_file_list() # <- update the file list
    
    # Function to parse the XML file
    def file_parser(self, file_path):
        processor = XMLProcessor(file_path)
        processor.parse_xml()
        return processor # <- return the processor object
        
    def update_file_list(self):
        # Clear the listbox
        self.file_listbox.delete(0, tk.END)

        # Get the names of the files in the destination folder
        file_names = os.listdir(self.destination_folder)

        # Add the file names to the listbox
        for file_name in file_names:
            self.file_listbox.insert(tk.END, file_name) # <- inserts
            
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
    
    # Function to handle the event when a file is selected
    def on_file_selected(self, event):
        # Get the index of the selected item
        selected_index = self.file_listbox.curselection()
        if selected_index:
            # Get the file name
            self.selected_file = self.file_listbox.get(selected_index)
            print(f"Archivo seleccionado: {self.selected_file}")

    # Function to handle the event when a button is clicked
    def on_button_click(self, button_number):
        # If a button is clicked, and a file is selected
        if button_number == 1 and self.selected_file:
            # Create a XMLProcessor object with the selected file
            self.xml_processor = self.file_parser(os.path.join(self.destination_folder, self.selected_file)) # <- call the file_parser function with the selected file
            # find the QR code
            qr_code = self.xml_processor.find_qr_code() # <- call the find_qr_code method
            print(f"Código QR: {qr_code}")
                
        elif button_number == 2 and self.selected_file:
            # Create a XMLProcessor object with the selected file
            self.xml_processor = self.file_parser(os.path.join(self.destination_folder, self.selected_file))
            # Find the items
            invoice_items = self.xml_processor.find_invoice_items() # <- call the find_invoice_items method
            
            # Create a new XMLFileCreator object
            creator = XMLFileCreator(self.xml_processor)
            creator.create_csv_file(self.destination_folder_2, invoice_items, "test")
            
        elif button_number == 3 and self.selected_file:
            # Show the dialog to select the party type
            party_dialog = PartyTypeDialog(self)
            self.wait_window(party_dialog) # <- wait for the dialog to close
            
            # If the party type is selected
            if party_dialog.party_type:
                # Get the party type
                party_type = party_dialog.party_type
                
                name = f"{party_type}_info"
                
                # Create a XMLProcessor object with the selected file
                self.xml_processor = self.file_parser(os.path.join(self.destination_folder, self.selected_file))
                party_info = self.xml_processor.find_party_info_items(party_type) # <- call the find_party_info_items method
                
                creator = XMLFileCreator(self.xml_processor)
                creator.create_csv_file(self.destination_folder_2, party_info, name)

        else:
            print(f"Selecciona un archivo y presiona el botón {button_number} para continuar.")
            
    
if __name__ == "__main__":
    app = GUI()
    app.mainloop()
