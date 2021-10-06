__author__ = 'Nombres_y_Apellidos'

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

    def __init__(self, model_class, command_cursor):        #TODO ¿ES NECESARIO TENER EL PARAMETRO MODEL_CLASS SI FIND PIDE DE VUELTA UN CURSOR Y NEXT DEVUELVE UN MODELO??
        """ Inicializa ModelCursor
        Argumentos:
            model_class (class) -- Clase para crear los modelos del 
            documento que se itera.
            command_cursor (CommandCursor) -- Cursor de pymongo
        """
        self.modelClass = model_class
        self.command_cursor = command_cursor
        pass #No olvidar eliminar esta linea una vez implementado
    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        if ModelCursor.alive():
            self.command_cursor = self.command_cursor.next()
            return self.model_class(self.command_cursor)                 #TODO ¿COMO DIFERENCIAMOS LOS MODELOS?

        pass #No olvidar eliminar esta linea una vez implementado

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        return self.command_cursor.hasNext()
        pass #No olvidar eliminar esta linea una vez implementado

class Persona:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
    required_vars = [] #primer nivel {nombre, apellidos} SOLO PRIMER NIVEL.
    admissible_vars = []
    db = None

    def __init__(self, **kwargs):
        #TODO MEMORIA PRINCIPAL
        self.__dict__.update(**kwargs)
        pass #No olvidar eliminar esta linea una vez implementado


    def save(self):
        #TODO
        #Comprueba si existe con _id
            #Comprobar requierd vars
            #si se da:
                #Si existe: llamar al set con updateOne
                #Si no existe: Crearlo con el insert desde save
            #si no se da
                #nada
        pass #No olvidar eliminar esta linea una vez implementado

    def set(self, **kwargs):
        #TODO  EL UPDATE/CHANGE  - MEMORIA PRINCIPAL
        
        pass #No olvidar eliminar esta linea una vez implementado
    
    @classmethod
    def find(cls, filter): #FILTER ES LA QUERIE
        """ Devuelve un cursor de modelos        
        """ 
        #TODO EL QUERY.
        #comprobar cuando se ha modificado la informacion. 
        # cls es el puntero a la clase
        cursorPersona = ModelCursor(Persona, self.db.personas.find())#Se da por hecho que personas es una coleccio
        return #model cursor

    @classmethod
    def init_class(cls, db, vars_path="model_name.vars"):                   #TODO ¿QUE FORMATO DEBE DE TENER El TXT Y COMO SE LEE?
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        self.db = db['MongoDbProyect']
        # cls es el puntero a la clase
        pass #No olvidar eliminar esta linea una vez implementado


# Q1: Listado de todas las compras de un cliente
nombre = "Definir"
Q1 = []

# Q2: etc...

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    Persona.init_class(client['MongDBProyect']['personas'], "personas.txt")
    pass #No olvidar eliminar esta linea una vez implementado

