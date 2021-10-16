__author__ = 'Hao_Long_y_Sebastian_Gutierrez'

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
        self.model_class = model_class
        self.command_cursor = command_cursor
    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        if ModelCursor.alive:
            return self.model_class(self.command_cursor.next())

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
        cont = 0
        for x in self.required_vars:
            for i in kwargs:
                if x == i:
                    cont +=1

        if cont == len(self.required_vars):
            all_vars = self.required_vars + self.admissible_vars
            print('all(', all_vars,')')
            for x in kwargs:
                for i in all_vars:
                    var_flag = False
                    if x == i :
                        var_flag = True
                        break
            if var_flag == False:
                raise Exception ('La key: ',x,' NO ES VALIDA.')

        self.__dict__.update(kwargs)


    def save(self):
        try:
            if hasattr(self, '_id'): #Significa que existe en la BD
                values = {'$set': self.modifed_vars}
                self.db.persona.update_one({'_id': self._id.inserted_id}) #DEBERIA SER EL NIF.
                print("\nSe ha actualizado correctamente.")
            else: #No existe en la BD
                modified_vars_aux = self.modified_vars
                del self.modified_vars
                self._id = self.db.persona.insert_one(self.__dict__)
                self.modified_vars = modified_vars_aux
                print('Se ha registrado correctamente.')
        except:
            print('\n\nERR: Algo ha fallado en Persona.save()')

    def set(self, **kwargs):

        curr = list(self.__dict__.keys())
        mod = list(kwargs.keys())

        modified_vars_aux = self.modified_vars
        all_vars = self.required_vars + self.admissible_vars

        del self.modified_vars

        for x in kwargs:
            var_flag = False
            print('DEBUG all(', all_vars[x],') && mod(', mod[x],')')
            if all_vars[x] == mod[x]:
                var_flag = True
                break
        if var_flag == False:
            raise Exception ('La key: ', mod[x], ' NO ES VALIDA.')

        for x in mod:
            if curr[x] == mod[x]:
                self.__dict__[curr[x]] = kwargs[mod[x]]
                modified_vars_aux.update({mod[x]: kwargs[mod[x]]})

        self.modified_vars = modified_vars_aux
    
    @classmethod
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        return ModelCursor(Persona, Persona.db.persona.find(filter))

    @classmethod
    def init_class(cls, db, vars_path="persona_vars.txt"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        try:
            file = open(vars_path, 'r')
            content_file = file.read()
            nothing = content_file.split('\n')
            required_vars = nothing[0].split(',')
            admissible_vars = nothing[1].split(',')
            file.close()
        except:
            print('el fichero de vars no existe')

        Persona.required_vars = required_vars
        Persona.admissible_vars = admissible_vars
        Persona.db = db


# Q1: Listado de todas las compras de un cliente
nombre = "Definir"
Q1 = []

# Q2: etc...

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    Persona.init_class(client['mongoproyect'])

    x = {'nombre': 'Sebas', 'apellido': 'Guti', 'telefono': 6553984293,'nif': 'y7502011t'}

    p1 = Persona(**x)
    p1.save()


    

