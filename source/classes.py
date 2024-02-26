# -------------- #
# Import modules #
# -------------- #

import os
import csv
import xml.etree.ElementTree as ET

# -------------------------------------------------------------------- #
# Constants for Namespaces                                             #
# -------------------------------------------------------------------- #

"""
'cac': UBL_AGGREGATE_NAMESPACE,
'cbc': UBL_NAMESPACE

urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2
urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2
"""

UBL_AGGREGATE_NAMESPACE = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
UBL_NAMESPACE = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
DIAN_NAMESPACE = 'dian:gov:co:facturaelectronica:Structures-2-1'

# ---------------------------------------------------------------------------------------------------
# XMLProcessor class parse the XML file and find the root, then looking for a XML description element
# ---------------------------------------------------------------------------------------------------


class XMLProcessor:
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.tree = None
        self.root = None
        self.description = None

    def parse_xml(self):
        try:
            self.tree = ET.parse(self.xml_file)
            self.root = self.tree.getroot()
        except Exception as e:
            self.handle_exception('parse xml', e)

    def find_root_description(self):
        try:
            # TODO: Find the type of XML file (Invoice or CreditNote)
            # xml_invoice = self.root.find('.//Invoice')
            # xml_credit_note = self.root.find('.//CreditNote')
            
            # print(f'Es invoice:{xml_invoice}')
            # print(f'Es creditNote: {xml_credit_note}')
            
            finded_root = self.root.findall('.//cbc:Description', namespaces={'cbc': UBL_NAMESPACE})
            self.description = finded_root[0].text if finded_root else None
        except Exception as e:
            self.handle_exception('find_root_description', e)
            self.description = "XML sin etiquetas <cbc:Description>"

    def find_qr_code(self):
        try:
            qrcode_element = self.root.find('.//sts:QRCode', namespaces={'sts': DIAN_NAMESPACE})
            return qrcode_element.text if qrcode_element is not None else "QRCode no encontrado en el XML"
        except Exception as e:
            self.handle_exception('find_qr_code', e)

    def find_invoice_items(self):
        try:
            # Extract taf InvoiceLine from the XML file
            invoice_items = self.root.findall('.//cac:InvoiceLine', 
                                              namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE})
            
            # Extract the CreditNoteLine from the XML file
            credit_note_items = self.root.findall('.//cac:CreditNoteLine', 
                                               namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE})

            # If InvoiceLine is found, extract the information
            if invoice_items:
                # Extract the information from each InvoiceLine and return a list of dictionaries
                items = [ self.extract_invoice_line_info(invoice_item) for invoice_item in invoice_items ]
                return items # <-- that's a list of dictionaries :D
            
            # If CreditNoteLine is found, extract the information
            if credit_note_items:
                # If InvoiceLine is not found, return a list with the other items
                data = [self.other_items(credit_item) for credit_item in credit_note_items]
                return data # <-- that's a list with a dictionary x2

            
        except Exception as e:
            self.handle_exception('find_invoice_items', e)

    def other_items(self, xml_item: str) -> dict:
        credit_note_item_info = {} # <-- that dictionary
        
        
        try:
            # Extract ID 
            credit_note_item_info['ID'] = xml_item.find('.//cbc:ID', namespaces={'cbc': UBL_NAMESPACE}).text
        except Exception as e :
            self.handle_exception('ID Credit Note', e)
            
        try:
            # Extract CreditedQuantity
            credit_note_item_info['CreditedQuantity'] = xml_item.find('.//cbc:CreditedQuantity', namespaces={'cbc': UBL_NAMESPACE}).text
        except Exception as e :
            self.handle_exception('CreditedQuantity Credit Note', e)
            
        try:
            # Extract LineExtensionAmount
            credit_note_item_info['LineExtensionAmount'] = xml_item.find('.//cbc:LineExtensionAmount', namespaces={'cbc': UBL_NAMESPACE}).text
        except Exception as e :
            self.handle_exception('LineExtensionAmount Credit Note', e)
            
        try:
            # Extract Item
            item = xml_item.find('.//cac:Item', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE})
            if item is not None:
                credit_note_item_info['Item'] = {
                    'Description': item.find('.//cbc:Description', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    
                    # NO FUNCIONA
                    # 'Description': item.find('.//cac:Item/cbc:Description', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text, <- NO FUNCIONA
                    
                    'StandardItemIdentification': {
                        'ID': item.find('.//cac:StandardItemIdentification/cbc:ID', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    }
                }
        except Exception as e :
            self.handle_exception('Item Credit Note', e)
            
        try:
            # Extract Price
            price = xml_item.find('.//cac:Price', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE})
            if price is not None:
                credit_note_item_info['Price'] = {
                    'PriceAmount': price.find('.//cbc:PriceAmount', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    'BaseQuantity': price.find('.//cbc:BaseQuantity', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text
                }
        except Exception as e :
            self.handle_exception('Price Credit Note', e)

        return credit_note_item_info # <-- that's a dictionary we are returning up there

    def find_party_info_items(self, party_type: str):
        party_type = party_type.lower()
        try:
            # Extract Party from the XML file
            party_info_items = self.root.findall('.//cac:Party', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE
            })

            # If Party is found, extract the information
            if party_info_items:
                # Extract the information from each Party and return a list of dictionaries
                if party_type == "supplier":
                    supplier = [self.extract_party_info(party_info_items[0])]
                    return supplier # <-- that's a list with a dictionary
                elif party_type == "customer":
                    customer = [self.extract_party_info(party_info_items[1])]
                    return customer
            else:
                print("No se encontró la etiqueta <sts:Party> en el archivo XML")
        except Exception as e:
            self.handle_exception('find_party_info_items', e)
            
    def extract_invoice_line_info(self, xml_item: str) -> dict:
        invoice_line_info = {} # <-- that dictionary

        try:
            # Extract ID and InvoicedQuantity
            invoice_line_info['ID'] = xml_item.find('.//cbc:ID', namespaces={
                'cbc': UBL_NAMESPACE
            }).text
        except Exception as e:
            self.handle_exception('ID', e)

        try:
            # Extract LineExtensionAmount
            invoice_line_info['LineExtensionAmount'] = xml_item.find('.//cbc:LineExtensionAmount', namespaces={
                'cbc': UBL_NAMESPACE
            }).text
        except Exception as e:
            self.handle_exception('LineExtensionAmount', e)

        try:
            # Extract FreeOfChargeIndicator
            free_of_charge_indicator = xml_item.find('.//cbc:FreeOfChargeIndicator', namespaces={
                'cbc': UBL_NAMESPACE
            }).text
            if free_of_charge_indicator is not None:
                invoice_line_info['FreeOfChargeIndicator'] = free_of_charge_indicator
        except Exception as e:
            self.handle_exception('FreeOfChargeIndicator', e)

        try:
            # ? Extract TaxTotal
            tax_total = xml_item.find('.//cac:TaxTotal', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if tax_total is not None:
                invoice_line_info['TaxTotal'] = {
                    'TaxAmount': tax_total.find('.//cbc:TaxAmount', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    'TaxSubtotal': {
                        'TaxableAmount': tax_total.find('.//cbc:TaxableAmount', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                        'TaxAmount': tax_total.find('.//cbc:TaxAmount', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                        'TaxCategory': {
                            'Percent': tax_total.find('.//cbc:Percent', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                            'TaxScheme': {
                                'Name': tax_total.find('.//cac:TaxScheme/cbc:Name', namespaces={'cac': UBL_AGGREGATE_NAMESPACE,
                                                                                                'cbc': UBL_NAMESPACE}).text
                            }
                        }
                    }
                }
        except Exception as e:
            self.handle_exception('TaxTotal', e)

        try:
            # ? Extract Item
            product = xml_item.find('.//cac:Item', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE,
            })
            if product is not None:
                invoice_line_info['Item'] = {
                    'Description': product.find('.//cbc:Description', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    # 'SellersItemIdentification': {
                    #     'ID': product.find('.//cac:SellersItemIdentification/cbc:ID', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text
                    # },
                    'StandardItemIdentification': {
                        'ID': product.find('.//cac:StandardItemIdentification/cbc:ID', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    },
                    # 'AdditionalItemProperty': {
                    #     'Name': product.find('.//cac:AdditionalItemProperty/cbc:Name', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    #     'Value': product.find('.//cac:AdditionalItemProperty/cbc:Value', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text
                    # }
                }
            else:
                raise ValueError("La etiqueta <cac:Item> no se encontró en la factura electrónica.")
        except Exception as e:
            self.handle_exception('Item', e)
            
        try:
            # Extract AdditionalItemProperty
            additional_item_property = xml_item.find('.//cac:Item/cac:AdditionalItemProperty', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if additional_item_property is not None:
                invoice_line_info['AdditionalItemProperty'] = {
                    'Name': additional_item_property.find('.//cbc:Name', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    'Value': additional_item_property.find('.//cbc:Value', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text
                }
        except Exception as e:
            self.handle_exception('Item AdditionalItemProperty', e)
            
        try:
            # Extract Price
            price = xml_item.find('.//cac:Price', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if price is not None:
                invoice_line_info['Price'] = {
                    'PriceAmount': {
                        'value': price.find('.//cbc:PriceAmount', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                        'CurrencyID': price.find('.//cbc:PriceAmount', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).get('CurrencyID')
                    },
                    'BaseQuantity': {
                        'value': price.find('.//cbc:BaseQuantity', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    }
                }
        except Exception as e:
            self.handle_exception('Price', e)

        return invoice_line_info # <-- that's a dictionary we are returning up there

    def extract_party_info(self, xml_item: str) -> dict:
        party_info = {} # <-- that dictionary

        try:
            # Extract PartyName
            party_name = xml_item.find('.//cac:PartyName/cbc:Name', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if party_name is not None:
                party_info['PartyName'] = party_name.text
        except Exception as e:
            self.handle_exception('PartyName', e)

        try:
            # Extract physical_location
            physical_location = xml_item.find('.//cac:PhysicalLocation/cac:Address', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if physical_location is not None:
                party_info['CityName'] = physical_location.find('.//cbc:CityName', namespaces={
                                                                'cbc': UBL_NAMESPACE}).text
                party_info['PostalZone'] = physical_location.find('.//cbc:PostalZone', namespaces={
                                                                'cbc': UBL_NAMESPACE}).text
                party_info['Country'] = physical_location.find('.//cac:Country/cbc:Name[@languageID="es"]', namespaces={
                                                                'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text
                party_info['AddressLine'] = physical_location.find('.//cac:AddressLine/cbc:Line', namespaces={
                                                                'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text
        except Exception as e:
            self.handle_exception('PhysicalLocation', e)

        try:
            # Extract tax_scheme
            tax_scheme = xml_item.find('.//cac:PartyTaxScheme/cac:TaxScheme', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if tax_scheme is not None:
                party_info['TaxSchemeID'] = tax_scheme.find(
                    './/cbc:ID', namespaces={'cbc': UBL_NAMESPACE}).text
                party_info['TaxSchemeName'] = tax_scheme.find(
                    './/cbc:Name', namespaces={'cbc': UBL_NAMESPACE}).text
        except Exception as e:
            self.handle_exception('PartyTaxScheme', e)

        try:
            # Extract PartyLegalEntity
            legal_entity = xml_item.find('.//cac:PartyLegalEntity', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if legal_entity is not None:
                party_info['LegalEntityName'] = legal_entity.find('.//cbc:RegistrationName', namespaces={
                                                                'cbc': UBL_NAMESPACE}).text
                party_info['LegalEntityID'] = legal_entity.find('.//cbc:CompanyID', namespaces={
                                                                'cbc': UBL_NAMESPACE}).text
                party_info['RegistrationSchemeID'] = legal_entity.find('.//cac:CorporateRegistrationScheme/cbc:ID', namespaces={
                                                                'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text
        except Exception as e:
            self.handle_exception('PartyLegalEntity', e)

        try:
            # Extract Contact
            contact = xml_item.find('.//cac:Contact', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if contact is not None:
                party_info['Telephone'] = contact.find('.//cbc:Telephone', namespaces={
                                                        'cbc': UBL_NAMESPACE}).text
                party_info['Email'] = contact.find('.//cbc:ElectronicMail', namespaces={
                                                        'cbc': UBL_NAMESPACE}).text
        except Exception as e:
            self.handle_exception('Contact', e)

        return party_info # <-- that's a dictionary we are returning up there

    def handle_exception(self, section_name: str, exception: Exception):
        if section_name == 'Invoice':
            print(f"|Error al analizar el archivo XML: {str(exception)}")
            print("||-Asegúrese de que el archivo XML esté bien formado y no esté dañado.")
            print("||--Asegúrese de que el archivo XML no esté vacío.")
            print("||---Asegúrese de que el archivo XML sí sea una factura electrónica.")
        # Print the error message
        print(f"Error in the section {section_name}: {str(exception)}")

# ------------------------------------------------------------------------------------------- #
# XMLFileCreator class create a new XML file with the content in the XML description element  #
# ------------------------------------------------------------------------------------------- #


class XMLFileCreator:
    # Constructor
    # XMLFileCreator class receives the description of the XML file and the original file name
    def __init__(self, xml_processor: XMLProcessor):
        self.description = xml_processor.description
        # Extract the original file name without the extension
        self.original_file_name = os.path.splitext(os.path.basename(xml_processor.xml_file))[0] # <- that's the original file name

    # destination_folder is the folder where the new XML file will be created
    def create_file(self, destination_folder):
        # Create a new XML file with the description
        prefix = self.original_file_name
        path_copies_file = os.path.join(destination_folder, f"{prefix}.xml") # <- that's the path of the new file

        os.makedirs(os.path.dirname(path_copies_file), exist_ok=True) # <- that's the new folder

        with open(path_copies_file, 'w', encoding='utf-8') as new_file:
            # Write the description in the new XML file
            new_file.write(self.description)

        print(f"Contenido copiado y pegado en '{path_copies_file}'") # <- that's the message we are printing

        return path_copies_file # <- that's the path of the new file

    # Function to create a CSV file
    def create_csv_file(self, destination_folder: str, data: str, name: str):
        try:
            data_list = data

            # If the data is a list, create a CSV file
            if data_list:
                # Create a new CSV file with the data
                path_copies_file = os.path.join(destination_folder, f"csv-{name}.csv") # <- that's the path of the new file

                os.makedirs(os.path.dirname(path_copies_file), exist_ok=True) # <- that's the new folder

                # Open the new CSV file and write the data
                with open(path_copies_file, 'w', newline='', encoding='utf-8') as csvfile:
                    # Write the BOM character to ensure that the CSV file is opened correctly
                    csvfile.write('\ufeff')

                    # Ensures that each element in datalist is a dictionary
                    data_list = [item if isinstance(
                        item, dict) else dict(item) for item in data_list]

                    # Verify that the list is not empty
                    if data_list:
                        # Define the field names for the CSV file
                        fieldnames = data_list[0].keys()

                        # Create a CSV writer object
                        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                        # Write the field names in the CSV file
                        csv_writer.writeheader()

                        # Write the data in the CSV file
                        csv_writer.writerows(data_list)

                        print(f"Contenido copiado y pegado en '{path_copies_file}'")
                        
                        return path_copies_file # <- that's the path of the new file
            else:
                print("No se encontró la etiqueta <sts:Party> en el archivo XML")
                
        except Exception as e:
            print(f"Error al crear el archivo CSV: {str(e)}")


"""


"""