"""

The main file was the type of logic I used to create the GUI, it's a pretty simple concept -
but I got the design right, somehow, before thinking about an interface. :)

This main file will not be used in future code. haha...
"""


# Importing variables from variables.py
import variables
# Importing classes from classes.py
from classes import XMLProcessor, XMLFileCreator
    
if __name__ == '__main__':
        
    # Creating a new XMLProcessor object
    xml_file_original = XMLProcessor(variables.XML1["file"])
    xml_file_original.parse_xml()

# Finding the description of the XML file
description = xml_file_original.find_root_description()

# If the description is found, create a new XML file with the description
if description:
    # Intance of XMLFileCreator with the description of the XML file
    new_xml_file_creator = XMLFileCreator(description, variables.XML1["name"])
    new_xml_file_creator.create_file()

    # Creating a new XMLProcessor object
    new_xml_file = XMLProcessor("source\\copies\\copia-ad080.xml")
    new_xml_file.parse_xml()

    # print the QR code (example of how to use the method find_qr_code())
    # print(new_xml_file.find_qr_code())

    # extract the items, supplier and customer from the XML file
    items = new_xml_file.find_invoice_items()
    supplier = new_xml_file.find_party_info_items("supplier")
    customer = new_xml_file.find_party_info_items("customer")
    
    # print the type of the variables
    print(type(items))
    print(type(supplier))
    print(type(customer))
    
    # create a new CSV file with the items
    create_csv = XMLFileCreator(supplier, variables.XML1["name"])
    create_csv.create_csv_file()
    
    # TODO: create the way to use graphing libraries to create a graph with the items

else:
    print("the tag description was not found in the XML file.")
    