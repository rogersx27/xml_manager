# Importing variables from variables.py
import variables
# Importing classes from classes.py
from classes import XMLProcessor, XMLFileCreator
    
if __name__ == '__main__':
        
    # Creating a new XMLProcessor object
    xml_file_original = XMLProcessor(variables.XML1["file"])
    xml_file_original.parse_xml()

description = xml_file_original.find_root_description()

if description:
    # Crear un nuevo XMLFileCreator con la descripción encontrada
    new_xml_file_creator = XMLFileCreator(description, variables.XML1["name"])
    new_xml_file_creator.create_file()

    # Crear una instancia de XMLProcessor con el archivo XML copiado
    new_xml_file = XMLProcessor("source\\copies\\copia-ad080.xml")
    new_xml_file.parse_xml()

    # Imprimir el código QR y otros detalles si es necesario
    # print(new_xml_file.find_qr_code())

    # Extraer información sobre ítems, proveedores y clientes
    items = new_xml_file.find_invoice_items()
    supplier = new_xml_file.find_party_info_items("supplier")
    customer = new_xml_file.find_party_info_items("customer")
    print(type(items))
    print(type(supplier))
    print(type(customer))
    
    create_csv = XMLFileCreator(supplier, variables.XML1["name"])
    create_csv.create_csv_file()

else:
    print("No se encontró la etiqueta <sts:QRCode> en el archivo XML")
    