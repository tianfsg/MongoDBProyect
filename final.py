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
        self.model_class = model_class
        self.command_cursor = command_cursor

    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        if ModelCursor.alive:
            self.command_cursor = self.command_cursor.next()
            return self.model_class(list(self.command_cursor)[0])
        
        #TODO Que pasa si el ModelCursor no es Alive , y falta comprobar si funciona

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
        lista = list(kwargs.keys())
        cont = 0

        for i in range(0, len(self.required_vars), 1): #Comprobador de las variables requeridas
            for x in range(0, len(kwargs), 1):
                if self.required_vars[i] == lista[x]:
                    cont += 1
                    break
        if cont == len(self.required_vars): #Entrar solo si coincidn las required vars
            #Comprobar todas las variables
            all_vars = self.required_vars + self.admissible_vars
            for i in range(0, len(kwargs), 1):
                var_flag = False
                for x in range(0, len(all_vars), 1):
                    if all_vars[x] == lista[i]:
                        var_flag = True         #Si esta dentro de las variables true
                        break
                if var_flag == False:           #Si no esta dentro de las variables se borra
                    raise Exception("La key: *" + lista[i] + "* NO ES VALIDA")
        else:
            raise Exception("Alguna variable requerida no es valida")

        self.__dict__.update(kwargs)
        self.modified_vars = {}

    def save(self):
        try:
            #comprobar si existe en la bd.
            if hasattr(self,'_id'): #Significa que existe
                print(self._id.inserted_id)
                values = {"$set": self.modified_vars}
                self.db.persona.update_one({"_id": self._id.inserted_id}, values)
                print('Se ha actualizado correctamente.')
            else: #Significa que no existe
                modified_vars_bckp = self.modified_vars #Se guardan variables cambiadas en una variable de funcion
                del self.modified_vars #Se borra del diccionario del modelo las variables cambiadas

                self._id = self.db.persona.insert_one(self.__dict__)
                print(self._id)
                self.modified_vars = modified_vars_bckp #Se vuelve a guardar el diccionario de variables cambiadas en el Modelo
                print('Registrado exitosamente.')
        except:
            print('Algo fallo en Persona.save()')
    

    def set(self, **kwargs):
        cur = list(self.__dict__.keys())
        mod = list(kwargs.keys())

        modified_vars_bckp = self.modified_vars #Se guardan variables cambiadas en una variable de funcion
        del self.modified_vars #Se borra del diccionario del modelo las variables cambiadas

        #comprobar todas las variables admisibles y requeridas
        lista = list(kwargs.keys())
        all_vars = self.required_vars + self.admissible_vars
        for i in range(0, len(kwargs), 1):
            var_flag = False
            for x in range(0, len(all_vars), 1):
                if all_vars[x] == lista[i]:
                    var_flag = True         #Si esta dentro de las variables true
                    break
            if var_flag == False:           #Si no esta dentro de las variables se borra
                raise Exception("La key: *" + lista[i] + "* NO ES VALIDA")
        
        for i in range(0, len(mod), 1): #Bucle para cambiar el Atributo
            for x in range(0, len(cur), 1):
                if cur[x] == mod[i]:
                    self.__dict__[cur[x]] = kwargs[mod[i]]
                    modified_vars_bckp.update({mod[i]:kwargs[mod[i]]})   #Se añaden los elementos cambiados a variables cambiadas
        
        self.modified_vars = modified_vars_bckp #Se vuelve a guardar el diccionario de variables cambiadas en el Modelo
    
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

    #X, E dentro de mongo
    x = {'nombre': 'Sebas', 'apellido': 'Guti', 'telefono': 6553984293, 'nif': 'y7502011t'}
    e = {'nombre': 'Hao', 'apellido': 'Long', 'telefono': 84473466374, 'nif': 'x3610444l'}
    i = {'nombre': 'Javier', 'apellido': 'Algarra', 'telefono': 3453245353, 'nif': 'e47583920'}
    w = {'nombre': 'Pablo', 'apellido': 'Ramos', 'telefono': 6558347834, 'nif': 'xxxxxxxxx'}

    # cursor = client['mongoproyect'].persona.count_documents({'_id': x['_id']})
    # cursor = client['mongoproyect'].persona.find()
    # print(cursor[0])

    p1 = Persona(**w)
    #print(p1.find({'_id': p1.__dict__['_id']}).command_cursor)
    p1.save()
    p1.set(**{'telefono': 000000000})
    p1.save()

    # a = 0
    # while a == 0:
    #     print('Bienvenido al Menu')
    #     print('Que desea introducir: ')
    #     print('1. Persona')
    #     print('2. Centro')
    #     print('3. Empresa')
    #     print()
    #     print('4. Salir')

    #     opc = input()

    #     if opc == '1':
    #         pass
    #     elif opc == '2':
    #         pass
    #     elif opc == '3':
    #         pass
    #     elif opc == '4':
    #         exit
    #     else:
    #         print()
    #         print('introduzca un valor valido\n')
