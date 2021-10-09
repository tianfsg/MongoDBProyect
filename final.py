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
        """ #TODO
        if ModelCursor.alive:
            self.command_cursor = self.command_cursor.next()
            return self.model_class(list(self.command_cursor)[0])

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
        #Comprobador de la posesion de las required_vars

        lista = list(self.__dict__.keys())
        valido = True
        cont = 0

        for i in range(0, len(self.required_vars), 1): 
            for x in range(0, len(self.__dict__), 1):
                if self.required_vars[i] == lista[x]:
                    cont += 1
                    break
    
        if cont == len(self.required_vars):
            #comprobar todas las variables porque no hemos separado las en el diccionario las RV de las AV
            all_vars = self.required_vars + self.admissible_vars
            for i in range(0, len(self.__dict__), 1):
                var_flag = False
                for x in range(0, len(all_vars), 1):
                    if all_vars[x] == lista[i]:
                        var_flag = True         #Si esta dentro de las variables true
                        break
                if var_flag == False:           #Si no esta dentro de las variables se borra
                    print("La key: *" + lista[i] + "* NO ES VALIDA")
                    valido = False
                    break

        try:
            if valido == True: #True: entonces contiene requeridas y admisibles.
                #comprobar si existe en la bd.

                if list(Persona.find({'_id': self.__dict__['_id']}).command_cursor): #Significa que existe
                    
                    self.set(self.__dict__)
                    print('Se ha actualizado correctamente.')
                else: #Significa que no existe
                    self.db.persona.insert_one(self.__dict__)
                    print('Registrado exitosamente.')
            else:
                print('invalido')
        except:
            print('Algo fallo en Persona.save()')
    

    def set(self, **kwargs):
        #TODO
        self.db.persona.update_one({'_id': self.__dict__['_id']}, {'$set': {kwargs}})
    
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

    x = {'_id': '1', 'nombre': 'Sebas', 'apellido': 'Guti', 'telefono': 6553984293, 'nif': 'x3610444l'}
    e = {'_id': '2', 'nombre': 'Hao', 'apellido': 'Long', 'telefono': 84473466374, 'nif': 'y7502011t'}
    i = {'_id': '3', 'nombre': 'Javier', 'apellido': 'Algarra', 'telefono': 3453245353, 'nif': 'e47583920'}

    # cursor = client['mongoproyect'].persona.count_documents({'_id': x['_id']})
    # cursor = client['mongoproyect'].persona.find()
    # print(cursor[0])

    p1 = Persona(**x)
    p2 = Persona(**e)
    #print(p1.find({'_id': p1.__dict__['_id']}).command_cursor)
    p1.save()
    p2.save()

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
