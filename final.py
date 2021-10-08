__author__ = 'Sebastian-Gutierrez_Hao-Long'

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
        self.modelClass = model_class
        self.command_cursor = command_cursor
    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        if ModelCursor.alive():
            self.command_cursor = self.command_cursor.next()
            return self.model_class(self.command_cursor[0])

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        return self.command_cursor.hasNext()

class Persona:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
    required_vars = []
    admissible_vars = []
    db = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


    def save(self):

        #Comprueba si existe con _id
            #Comprobar requierd vars
            #si se da:
                #Si existe: llamar al set con updateOne
                #Si no existe: Crearlo con el insert desde save
            #si no se da
            #nada
        lista = list(self.__dict__.keys())
        cont = 0

        print(len(self.required_vars))
        print(len(self.__dict__))

        for i in range(0, len(self.required_vars), 1):

            print('i:',i,'-requerida: ', self.required_vars[i])
        
            for x in range(i, len(self.__dict__), 1):
            
                print('x:', x, '-dicc:   ', lista[x])
                if lista[x] != self.required_vars[i]:
                    print(self.required_vars[i],' ',lista[x],' ',lista[x] == self.required_vars[i])
                    i+=1
                else:
                    print(self.required_vars[i],' ',lista[x],' ',lista[x] == self.required_vars[i])
                    cont+=1
                    break
                    

        print('contador: ', cont)



    def set(self, **kwargs):
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado
    
    @classmethod
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        #TODO
        cursorPersona = ModelCursor(Persona, self.db.personas.find())#Se da por hecho que personas es una coleccio
        pass #No olvidar eliminar esta linea una vez implementado

    @classmethod
    def init_class(cls, db, vars_path="model_vars.txt"):
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
        Persona.db = db['MongoDbProyect']


# Q1: Listado de todas las compras de un cliente
nombre = "Definir"
Q1 = []

# Q2: etc...

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    Persona.init_class(client['MongDBProyect'])

    x = {'_id': '1', 'nombre': 'Sebas', 'apellido': 'Guti', 'telefono': 6553984293}
    
    p1 = Persona(**x)
    p1.save()
   

