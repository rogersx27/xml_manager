# Explicaciones

#### ¿Dos o más clases que puedan manejar el mismo archivo instaciado?

Sí, he estado siguiendo el principio de diseño conocido como Separación de Responsabilidades y utilizando el patrón Singleton de forma implícita, aunque esta última no se aplica de manera estricta (que normalmente implica una única instancia de una clase).

- La clase *XMLProcessor* se encarga específicamente de procesar y extraer información de un archivo XML. Su responsabilidad es __analizar la estructura__  XML y proporcionar métodos para __acceder a datos específicos__.

- La clase *XMLFileCreator* se encarga de crear una copia del contenido del archivo XML procesado. Su responsabilidad está centrada en la __manipulación y creación de archivos__.

# Documentación de Constantes 🎉

- <h3 style = "color: green">UBL_NAMESPACE</h3>

**Descripción**: Representa el espacio de nombres utilizado en el estándar Universal Business Language (UBL) para los Componentes Básicos Comunes (Common Basic Components).

**Valor**

 	urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2

**Uso**: Esta constante se utiliza al buscar elementos específicos en archivos XML que siguen el estándar UBL.

------------

- <h3 style = "color: green">UBL_AGGREGATE_NAMESPACE</h3>

**Descripción**: Representa el espacio de nombres utilizado en el estándar Universal Business Language (UBL) para los Componentes Agregados Comunes (Common Aggregate Components).

**Valor**

 	urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2

**Uso**: Utilizado para identificar y procesar elementos agregados en archivos XML que siguen el estándar UBL.

------------

- <h3 style = "color: green">DIAN_NAMESPAC</h3>

**Descripción**: Representa el espacio de nombres utilizado por la Dirección de Impuestos y Aduanas Nacionales (DIAN) de Colombia para la factura electrónica en la versión 2.1 de la estructura.

**Valor**

 	dian:gov:co:facturaelectronica:Structures-2-1

**Uso**: Utilizado para identificar y procesar elementos específicos relacionados con la estructura de la factura electrónica de la DIAN en archivos XML.

### Uso General en el Código

Estas constantes desempeñan un papel fundamental en el procesamiento de archivos XML que siguen los estándares UBL y la estructura de factura electrónica de la DIAN en Colombia. Al emplear estas constantes, el código puede identificar de manera precisa los elementos y componentes necesarios para extraer información relevante de los archivos XML. Las descripciones proporcionadas ayudan a comprender la función y relevancia de cada constante en el contexto del código.

------------
