# XML Processor GUI

## Descripción 🔊
Es una interfaz gráfica de usuario (GUI) desarrollada en Python utilizando la biblioteca Tkinter. Esta interfaz permite procesar archivos XML, realizar diversas operaciones con ellos, y manipular archivos CSV.

## Requisitos 🧷
- Python 3.x instalado en el sistema.
- Bibliotecas necesarias: tkinter.

## Instrucciones de Uso 🏁
1. Ejecute el script `interfaz.py` para iniciar la aplicación.
2. Una vez que la aplicación esté abierta, puede realizar las siguientes acciones:

    - **Seleccionar Archivo XML**: Haga clic en este botón para seleccionar un archivo XML para procesar.
    - **Actualizar**: Actualiza la lista de archivos mostrados.
    - **Eliminar**: Elimina el archivo seleccionado de la lista.
    - **Encontrar QR**: Encuentra el código QR en el archivo XML seleccionado.
    - **Encontrar Items**: Encuentra los elementos en el archivo XML seleccionado y crea un archivo CSV.
    - **Encontrar Información**: Permite seleccionar el tipo de partido (Supplier o Customer) y crea un archivo CSV con la información correspondiente.

## Estructura de Carpetas 📁
- **copies**: Esta carpeta contiene copias de los archivos XML procesados.
- **csv**: Esta carpeta contiene archivos CSV generados.

## Funcionalidades Adicionales 🎨
- **Seleccionar Carpeta para CSV**: Permite al usuario seleccionar una carpeta donde se guardarán los archivos CSV generados.

## Notas 🗒
- La aplicación también proporciona una funcionalidad para crear automáticamente las carpetas necesarias si no existen.
- Los botones "Encontrar QR", "Encontrar Items" y "Encontrar Información" están deshabilitados hasta que se seleccione un archivo XML.
- Para obtener más detalles sobre el código y las funciones, consulte los comentarios en el script `interfaz.py`.

# Documentación de Constantes 🎉

- <h3 style = "color: green">UBL_NAMESPACE</h3>

**Descripción**: Representa el espacio de nombres utilizado en el estándar Universal Business Language (UBL) para los Componentes Básicos Comunes (Common Basic Components).

**Valores de ejemplo:**

 	urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2

 	urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2

**Uso**: Utilizado para identificar y procesar elementos agregados en archivos XML que siguen el estándar UBL.

------------

- <h3 style = "color: green">DIAN_NAMESPAC</h3>

**Descripción**: Representa el espacio de nombres utilizado por la Dirección de Impuestos y Aduanas Nacionales (DIAN) de Colombia para la factura electrónica en la versión 2.1 de la estructura.

**Valor:**

 	dian:gov:co:facturaelectronica:Structures-2-1

**Uso**: Utilizado para identificar y procesar elementos específicos relacionados con la estructura de la factura electrónica de la DIAN en archivos XML.

### Uso General en el Código

Estas constantes desempeñan un papel fundamental en el procesamiento de archivos XML que siguen los estándares UBL y la estructura de factura electrónica de la DIAN en Colombia. Al emplear estas constantes, el código puede identificar de manera precisa los elementos y componentes necesarios para extraer información relevante de los archivos XML. Las descripciones proporcionadas ayudan a comprender la función y relevancia de cada constante en el contexto del código.

------------
