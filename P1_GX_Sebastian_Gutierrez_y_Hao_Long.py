__author__ = 'Sebastian_Gutierrez_&_Hao_Long'

from pymongo import MongoClient

def getCityGeoJSON(address):
    """ Devuelve las coordenadas de una direcciion a partir de un str de la direccion
    Cuidado, la API tiene un limite de peticiones.
    Argumentos:
        address (str) -- Direccion
    Return:
        (str) -- GeoJSON
    """
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    #TODO
    # Devolver GeoJSON de tipo punto con la latitud y longitud almacenadas
    # en las variables location.latitude y location.longitude

class ModelCursor:
    """ Cursor para iterar sobre los documentos del resultado de una
    consulta. Los documentos deben ser devueltos en forma de objetos
    modelo.
    """

    def __init__(self, model_class, command_cursor):
        """ Inicializa ModelCursor
        Argumentos:
            model_class (class) -- Clase para crear los modelos del 
            documento que se itera.
            command_cursor (CommandCursor) -- Cursor de pymongo
        """
        #TODO
        #2 lineas
        pass #No olvidar eliminar esta linea una vez implementado
    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        #TODO PARA PODER CONVERTIR LO QUE DEVUELVE A UN MODELO HAY QUE UTILIZAR DPS PERSONA(**dict);
        #model_class(**dict) DE MANERA GENERICA.
        #
        #TRY/CATCH
        pass #No olvidar eliminar esta linea una vez implementado

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado

class Persona:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja.

        SI ESTA EN MEMORIA PRINCIPAL NO TIENE _ID, SI LO TIENE ENTONCES YA ESTA EN LA BD.

        CON ESTA ID cambia EL NOMBRE x EJEMPLO.

        DESEMPACAR EL DICCIONARIO PARA PODER PASARLO POR EL **(EL DICCIONARIO) CURSOR


        CLS -> REFERENCE TO THE CLASS


        CONSIDERAR HACER LOS .aggregate() para filtrar la informacion
    """
    required_vars = [] #primer nivel {nombre, apellidos} SOLO PRIMER NIVEL. NECESARIAS SI O SI PARA CREAR USUARIO
    admissible_vars = [] #se permiten aun que no son necesarias para crear al perfil
    db = None

    def __init__(self, **kwargs):
        #TODO MEMORIA PRINCIPAL / CONSTRUCTOR.
        #No olvidar eliminar esta linea una vez implementado
        self.__dict__.update(kwargs)
    
    #MODEL              MONGO
    #SAVE()             FIND()
    #SET                NEXT()

    def save(self):
        #TODO MEMORIA PRINCIPAL -> DB

        pass #No olvidar eliminar esta linea una vez implementado

    def set(self, **kwargs):
        #TODO  EL UPDATE/CHANGE  - MEMORIA PRINCIPAL
        pass #No olvidar eliminar esta linea una vez implementado
    

    #MONGO para SERVER
    @classmethod
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        #TODO - EL QUERY.
        #pymongo.find() NO HAY PROYECCION. recibe el mismo argumento que db.x.find('<query>') **IMPORTANTE ENTRE COMILLAS LAS QUERY.
        #DEVUELVE UN CURSOR. 
        #comprobar cuando se ha modificado la informacion. 
        # cls es el puntero a la clase
        pass #No olvidar eliminar esta linea una vez implementado

    @classmethod
    def init_class(cls, db, vars_path="model_name.vars"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        file = open(vars_path, 'r')
        content_file = file.read()
        nothing = content_file.split('\n')
        required_vars = nothing[0].split(',')
        admissible_vars = nothing[1].split(',')
        file.close()

        Persona.required_vars = required_vars
        Persona.admissible_vars = admissible_vars
    

        pass #No olvidar eliminar esta linea una vez implementado


class Empresa:

    def __init__(self, **kwargs):
        pass
    

    def save(self):
        #TODO MEMORIA PRINCIPAL -> DB
        pass #No olvidar eliminar esta linea una vez implementado

    def set(self, **kwargs):
        #TODO  EL UPDATE/CHANGE  - MEMORIA PRINCIPAL
        pass #No olvidar eliminar esta linea una vez implementado
    
    @classmethod
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        #TODO - EL QUERY.
        #pymongo.find() NO HAY PROYECCION. recibe el mismo argumento que db.x.find('<query>') **IMPORTANTE ENTRE COMILLAS LAS QUERY.
        #DEVUELVE UN CURSOR. 
        #comprobar cuando se ha modificado la informacion. 
        # cls es el puntero a la clase
        pass #No olvidar eliminar esta linea una vez implementado

    @classmethod
    def init_class(cls, db, vars_path=""):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        #TODO
        # cls es el puntero a la clase
        pass #No olvidar eliminar esta linea una vez implementado


class Centro_educativo:

    def __init__(self, **kwargs):
        pass

    def save(self):
        #TODO MEMORIA PRINCIPAL -> DB
        pass #No olvidar eliminar esta linea una vez implementado

    def set(self, **kwargs):
        #TODO  EL UPDATE/CHANGE  - MEMORIA PRINCIPAL
        pass #No olvidar eliminar esta linea una vez implementado
    
    @classmethod
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        #TODO - EL QUERY.
        #pymongo.find() NO HAY PROYECCION. recibe el mismo argumento que db.x.find('<query>') **IMPORTANTE ENTRE COMILLAS LAS QUERY.
        #DEVUELVE UN CURSOR. 
        #comprobar cuando se ha modificado la informacion. 
        # cls es el puntero a la clase
        pass #No olvidar eliminar esta linea una vez implementado

    @classmethod
    def init_class(cls, db, vars_path="model_name.vars"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        
        # cls es el puntero a la clase
        

        #pass #No olvidar eliminar esta linea una vez implementado



# Q1: Listado de todas las compras de un cliente
nombre = "Definir"
Q1 = []

# Q2: etc...

if __name__ == '__main__':
    #TODO
    #MongoClient al host
    #MAIN COMPLETO DEL PROG
    #la bd completa o la collecion

    client = MongoClient(host="localhost", port=27017)
    db = client.practica
    user = db.usuario
    
    #keys nos permite ver las claves que tiene cada objeto
    for x in user.find():
       #print(x.keys())
       pass

    #print(db)
    #print(user)

    #print(user.find()[1])

    #print(user.find_one({'nombre.nombre': 'Hao'}))

    p1 = Persona(**{'nombre':'Elsa', 'apellido':'Munoz', 'edad':23})
    Persona.init_class(db,'/Users/willyfsg/Downloads/model_vars.vars.txt')
    print(p1.admissible_vars)
    print(p1.required_vars)

