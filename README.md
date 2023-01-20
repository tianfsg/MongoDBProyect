# MongoDBProyect
Este proyecto es un ejemplo de cómo utilizar MongoDB con Python. Se incluyen funciones para obtener las coordenadas de una dirección a través de la API de geolocalización Nominatim y una clase modelo para facilitar la creación de objetos a partir de los documentos de la base de datos.

Para utilizar este proyecto, es necesario tener una instancia de MongoDB corriendo en localhost en el puerto predeterminado (27017) y tener instalado el paquete pymongo.

La clase ModelCursor permite iterar sobre los documentos devueltos por una consulta y devolverlos como objetos modelo. La clase Persona es un ejemplo de un modelo que se utiliza para representar documentos de la colección "personas" en la base de datos. Esta clase tiene métodos para guardar y actualizar documentos en la base de datos.

La función getCityGeoJSON utiliza la API de geolocalización Nominatim para obtener las coordenadas de una dirección y devolverlas en formato GeoJSON. Tenga en cuenta que esta función tiene un límite de peticiones.

Este proyecto es solo un ejemplo y puede ser modificado y ampliado según las necesidades del usuario.

Dependecias:
centro_vars.txt
empresa_vars.txt
persona_vars.txt
redES.json
