# -------------- #
# Import modules #
# -------------- #

import os
import csv
import xml.etree.ElementTree as ET

# -------------------------------------------------------------------- #
# Constants for Namespaces                                             #
# -------------------------------------------------------------------- #

UBL_NAMESPACE = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
UBL_AGGREGATE_NAMESPACE = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
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
        self.tree = ET.parse(self.xml_file)
        self.root = self.tree.getroot()

    def find_root_description(self):
        try:
            finded_root = self.root.findall('.//cbc:Description', namespaces={'cbc': UBL_NAMESPACE})
            self.description = finded_root[0].text if finded_root else None
        except IndexError:
            return "XML sin etiquetas <cbc:Description>"

    def find_qr_code(self):
        try:
            qrcode_element = self.root.find('.//sts:QRCode', namespaces={'sts': DIAN_NAMESPACE})
            return qrcode_element.text if qrcode_element is not None else "QRCode no encontrado en el XML"
        except IndexError:
            return "XML sin etiquetas <sts:QRCode>"

    def find_invoice_items(self):
        try:
            invoice_items = self.root.findall('.//cac:InvoiceLine', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE})

            if invoice_items:
                items = [self.extract_invoice_line_info(
                    item) for item in invoice_items]
                return items
            else:
                data = [self.other_items()]
                return data

        except IndexError:
            self.handle_exception('InvoiceLine')

    def other_items(self) -> dict:
        credit_note_item_info = {}

        try:
            # Extract CreditNoteLine
            CreditNoteLine = self.root.find('.//cac:CreditNoteLine', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE
            })
            if CreditNoteLine is not None:
                credit_note_item_info = {
                    'Description': CreditNoteLine.find('.//cac:Item/cbc:Description', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    'StandardItemIdentification': {
                        'ID': CreditNoteLine.find('.//cac:Item/cac:StandardItemIdentification/cbc:ID', namespaces={'cac': UBL_AGGREGATE_NAMESPACE, 'cbc': UBL_NAMESPACE}).text,
                    }
                }
        except Exception as e:
            self.handle_exception('CreditNoteLine', e)

        return credit_note_item_info

    def find_party_info_items(self, party_type: str):
        party_type = party_type.lower()
        try:
            party_info_items = self.root.findall('.//cac:Party', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE
            })

            if party_info_items:
                if party_type == "supplier":
                    supplier = [self.extract_party_info(party_info_items[0])]
                    return supplier
                elif party_type == "customer":
                    customer = [self.extract_party_info(party_info_items[1])]
                    return customer
            else:
                print("No se encontró la etiqueta <sts:Party> en el archivo XML")
        except IndexError:
            return "XML sin etiquetas <sts:Party>"

    def extract_invoice_line_info(self, xml_item: str) -> dict:
        invoice_line_info = {}

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
            invoice_line_info['FreeOfChargeIndicator'] = xml_item.find('.//cbc:FreeOfChargeIndicator', namespaces={
                'cbc': UBL_NAMESPACE
            }).text
        except Exception as e:
            self.handle_exception('FreeOfChargeIndicator', e)

        try:
            # Extract TaxTotal
            tax_total = xml_item.find('.//cac:TaxTotal', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if tax_total is not None:
                invoice_line_info['TaxTotal'] = {
                    'TaxAmount': tax_total.find('.//cbc:TaxAmount', namespaces={'cbc': UBL_NAMESPACE}).text,
                    'TaxSubtotal': {
                        'TaxableAmount': tax_total.find('.//cbc:TaxableAmount', namespaces={'cbc': UBL_NAMESPACE}).text,
                        'TaxAmount': tax_total.find('.//cbc:TaxAmount', namespaces={'cbc': UBL_NAMESPACE}).text,
                        'TaxCategory': {
                            'Percent': tax_total.find('.//cbc:Percent', namespaces={'cbc': UBL_NAMESPACE}).text,
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
            # Extract Item
            item = xml_item.find('.//cac:Item', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if item is not None:
                invoice_line_info['Item'] = {
                    'Description': item.find('.//cbc:Description', namespaces={'cbc': UBL_NAMESPACE}).text,
                    'AdditionalItemProperty': {
                        'Name': item.find('.//cac:AdditionalItemProperty/cbc:Name', namespaces={'cac': UBL_AGGREGATE_NAMESPACE,
                                                                                                'cbc': UBL_NAMESPACE}).text,

                        'Value': item.find('.//cac:AdditionalItemProperty/cbc:Value', namespaces={'cac': UBL_AGGREGATE_NAMESPACE,
                                                                                                  'cbc': UBL_NAMESPACE}).text
                    },
                    'OriginAddress': {
                        'ID': item.find('.//cac:OriginAddress/cbc:ID', namespaces={'cac': UBL_AGGREGATE_NAMESPACE,
                                                                                   'cbc': UBL_NAMESPACE}).text
                    }
                }
        except Exception as e:
            self.handle_exception('Item', e)

        try:
            # Extract Price
            price = xml_item.find('.//cac:Price', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if price is not None:
                invoice_line_info['Price'] = {
                    'PriceAmount': {
                        'value': price.find('.//cbc:PriceAmount', namespaces={'cbc': UBL_NAMESPACE}).text,
                        'CurrencyID': price.find('.//cbc:PriceAmount', namespaces={'cbc': UBL_NAMESPACE}).get('CurrencyID')
                    },
                    'BaseQuantity': {
                        'value': price.find('.//cbc:BaseQuantity', namespaces={'cbc': UBL_NAMESPACE}).text,
                    }
                }
        except Exception as e:
            self.handle_exception('Price', e)

        return invoice_line_info

    def extract_party_info(self, xml_item: str) -> dict:
        party_info = {}

        try:
            # Extraemos información de PartyName
            party_name = xml_item.find('.//cac:PartyName/cbc:Name', namespaces={
                'cac': UBL_AGGREGATE_NAMESPACE,
                'cbc': UBL_NAMESPACE
            })
            if party_name is not None:
                party_info['PartyName'] = party_name.text
        except Exception as e:
            self.handle_exception('PartyName', e)

        try:
            # Extraemos información de PhysicalLocation
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
            # Extraemos información de PartyTaxScheme
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
            # Extraemos información de PartyLegalEntity
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
            # Extraemos información de Contact
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

        return party_info

    def handle_exception(self, section_name: str, exception: Exception):
        print(f"Error en la sección {section_name}: {str(exception)}")

# ------------------------------------------------------------------------------------------- #
# XMLFileCreator class create a new XML file with the content in the XML description element  #
# ------------------------------------------------------------------------------------------- #


class XMLFileCreator:
    def __init__(self, xml_processor: XMLProcessor):
        self.description = xml_processor.description
        self.original_file_name = os.path.splitext(os.path.basename(xml_processor.xml_file))[0]

    def create_file(self, destination_folder):
        prefix = self.original_file_name[:7]
        path_copies_file = os.path.join(destination_folder, f"copia-{prefix}.xml")

        os.makedirs(os.path.dirname(path_copies_file), exist_ok=True)

        with open(path_copies_file, 'w', encoding='utf-8') as new_file:
            new_file.write(self.description)

        print(f"Contenido copiado y pegado en '{path_copies_file}'")

        return path_copies_file

    def create_csv_file(self):
        try:
            data_list = self.text
            item = input("Ingrese el nombre del ítem: ")
            prefix = self.original_file_name[:7]

            # Cambia la extensión del archivo a .csv
            path_csv_file = os.path.join(
                'source', 'csv', f"csv-{prefix}-{item}.csv")

            os.makedirs(os.path.dirname(path_csv_file), exist_ok=True)

            # Abre el archivo CSV en modo de escritura
            with open(path_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                # Escribe el BOM (Byte Order Mark) para garantizar UTF-8 con BOM
                csvfile.write('\ufeff')

                # Asegura que cada elemento en data_list sea un diccionario
                data_list = [item if isinstance(
                    item, dict) else dict(item) for item in data_list]

                # Verifica si data_list no está vacío
                if data_list:
                    # Define los encabezados del CSV basados en las claves del primer diccionario en la lista
                    fieldnames = data_list[0].keys()

                    # Crea el objeto escritor CSV
                    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    # Escribe los encabezados en el archivo
                    csv_writer.writeheader()

                    # Escribe cada diccionario en la lista como una fila en el archivo
                    csv_writer.writerows(data_list)

                    print(f"Archivo CSV creado con éxito en: {path_csv_file}")

        except Exception as e:
            print(f"Error al crear el archivo CSV: {str(e)}")
