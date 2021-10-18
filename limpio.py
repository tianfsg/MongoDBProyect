__author__ = 'Hao_Long_y_Sebastian_Gutierrez'

import pymongo
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
    geolocator = Nominatim(user_agent='Nosotros')
    location = geolocator.geocode(address)
    return 'Latitud = {}, Longitud = {}'.format(location.latitude, location.longitude)
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
            return self.model_class(**self.command_cursor.next())

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        try:
            self.command_cursor.next()
            return True
        except:
            return False

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

        id_aux = None
        if '_id' in kwargs:
            id_aux = kwargs['_id']
            kwargs.pop('_id')

        cont = 0
        for x in self.required_vars:
            for i in kwargs:
                if x == i:
                    cont +=1

        if cont == len(self.required_vars):
            all_vars = self.required_vars + self.admissible_vars
            for x in kwargs:
                for i in all_vars:
                    var_flag = False
                    if x == i :
                        var_flag = True
                        break
            if var_flag == False:
                raise Exception ('La key: ',x,' NO ES VALIDA.')

        if id_aux != None:
            self._id = id_aux
        self.__dict__.update(kwargs)


    def save(self):
        try:
            if hasattr(self, '_id'): #Significa que existe en la BD
                values = {'$set': self.mod}
                self.db.persona.update_one({'_id': self._id.inserted_id}, values) #DEBERIA SER EL NIF.
                print("\nSe ha actualizado correctamente.")
            else: #No existe en la BD
                self._id = self.db.persona.insert_one(self.__dict__)
                print('Se ha registrado correctamente.')
        except:
            print('\n\nERR: Algo ha fallado en Persona.save()')

    def set(self, **kwargs):

        id_aux = None
        if hasattr(self, '_id'):
            id_aux = self.__dict__['_id']
            self.__dict__.pop('_id')

        curr = list(self.__dict__.keys())
        mod = list(kwargs.keys())

        #all_vars = self.required_vars + self.admissible_vars
        var_flag = False
        for x in curr:
            for i in mod:
                if x == i:
                    var_flag = True
                    break
        if var_flag == False:
            raise Exception ('La key: ', i, ' NO ES VALIDA.')

        for x in curr:
            for i in mod:
                if x == i:
                    self.__dict__[x] = kwargs[i]
                    self.mod = {x: kwargs[i]}
                    
        if id_aux != None:
            self._id = id_aux
 
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
        Persona.db.persona.create_index('nif', unique = True)
        Persona.db.persona.create_index([("localizacion", pymongo.GEOSPHERE)])

class Centro:
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

        id_aux = None
        if '_id' in kwargs:
            id_aux = kwargs['_id']
            kwargs.pop('_id')

        cont = 0
        for x in self.required_vars:
            for i in kwargs:
                if x == i:
                    cont +=1

        if cont == len(self.required_vars):
            all_vars = self.required_vars + self.admissible_vars
            for x in kwargs:
                for i in all_vars:
                    var_flag = False
                    if x == i :
                        var_flag = True
                        break
            if var_flag == False:
                raise Exception ('La key: ',x,' NO ES VALIDA.')

        if id_aux != None:
            self._id = id_aux
        self.__dict__.update(kwargs)


    def save(self):
        try:
            if hasattr(self, '_id'): #Significa que existe en la BD
                values = {'$set': self.mod}
                self.db.centro.update_one({'_id': self._id.inserted_id}, values) #DEBERIA SER EL NIF.
                print("\nSe ha actualizado correctamente.")
            else: #No existe en la BD
                self._id = self.db.centro.insert_one(self.__dict__)
                print('Se ha registrado correctamente.')
        except:
            print('\n\nERR: Algo ha fallado en Persona.save()')

    def set(self, **kwargs):

        id_aux = None
        if hasattr(self, '_id'):
            id_aux = self.__dict__['_id']
            self.__dict__.pop('_id')

        curr = list(self.__dict__.keys())
        mod = list(kwargs.keys())

        #all_vars = self.required_vars + self.admissible_vars
        var_flag = False
        for x in curr:
            for i in mod:
                if x == i:
                    var_flag = True
                    break
        if var_flag == False:
            raise Exception ('La key: ', i, ' NO ES VALIDA.')

        for x in curr:
            for i in mod:
                if x == i:
                    self.__dict__[x] = kwargs[i]
                    self.mod = {x: kwargs[i]}
                    
        if id_aux != None:
            self._id = id_aux
 
    @classmethod
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        return ModelCursor(Centro, Centro.db.centro.find(filter))

    @classmethod
    def init_class(cls, db, vars_path="centro_vars.txt"):
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
            required_vars = nothing.split(',')
            file.close()
        except:
            print('el fichero de vars no existe')

        Centro.required_vars = required_vars
        Centro.db = db
        Centro.db.centro.create_index('', unique = True)


class Empresa:
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

        id_aux = None
        if '_id' in kwargs:
            id_aux = kwargs['_id']
            kwargs.pop('_id')

        cont = 0
        for x in self.required_vars:
            for i in kwargs:
                if x == i:
                    cont +=1

        if cont == len(self.required_vars):
            all_vars = self.required_vars + self.admissible_vars
            for x in kwargs:
                for i in all_vars:
                    var_flag = False
                    if x == i :
                        var_flag = True
                        break
            if var_flag == False:
                raise Exception ('La key: ',x,' NO ES VALIDA.')

        if id_aux != None:
            self._id = id_aux
        self.__dict__.update(kwargs)


    def save(self):
        try:
            if hasattr(self, '_id'): #Significa que existe en la BD
                values = {'$set': self.mod}
                self.db.empresa.update_one({'_id': self._id.inserted_id}, values) #DEBERIA SER EL NIF.
                print("\nSe ha actualizado correctamente.")
            else: #No existe en la BD
                self._id = self.db.empresa.insert_one(self.__dict__)
                print('Se ha registrado correctamente.')
        except:
            print('\n\nERR: Algo ha fallado en Persona.save()')

    def set(self, **kwargs):

        id_aux = None
        if hasattr(self, '_id'):
            id_aux = self.__dict__['_id']
            self.__dict__.pop('_id')

        curr = list(self.__dict__.keys())
        mod = list(kwargs.keys())

        #all_vars = self.required_vars + self.admissible_vars
        var_flag = False
        for x in curr:
            for i in mod:
                if x == i:
                    var_flag = True
                    break
        if var_flag == False:
            raise Exception ('La key: ', i, ' NO ES VALIDA.')

        for x in curr:
            for i in mod:
                if x == i:
                    self.__dict__[x] = kwargs[i]
                    self.mod = {x: kwargs[i]}
                    
        if id_aux != None:
            self._id = id_aux
 
    @classmethod
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        return ModelCursor(Empresa, Empresa.db.empresa.find(filter))

    @classmethod
    def init_class(cls, db, vars_path="empresa_vars.txt"):
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
            required_vars = nothing.split(',')
            file.close()
        except:
            print('el fichero de vars no existe')

        Empresa.required_vars = required_vars
        Empresa.db = db
        Empresa.db.empresa.create_index('', unique = True)

# Q1: Listado de todas las compras de un cliente
nombre = "Definir"
Q1 = []

# Q2: etc...

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    Persona.init_class(client['mongoproyect'])

    #TODO FALTA CREAR EL POINT y MANDAR UNIQUE KEY DE 2dSPHERE, TERMINAR Q4, Q5, Q7
    # Y ANIDAR LAS LATITUDES Y LONGITUDES.

    """
        Pruebas de funcionamieto de Modelo() 

            save() - Condicion (_id) ? update_one() : insert_one()
            set(filter) - Modifies the actual object.
            cursor - Gets the actual document.
    """

    persona = {'nombre': 'Sebas', 'apellido': 'Guti', 'telefono': '655408703','nif': 'y7502011t'}
    centro = {'nombre': 'Sebas', 'apellido': 'Guti', 'telefono': '655408703','nif': 'y7502011t'}
    empresa = {'nombre': 'Sebas', 'apellido': 'Guti', 'telefono': '655408703','nif': 'y7502011t'}

    p1 = Persona(**persona)
    p1.save()
    p1.set(**{'telefono':'5000000'})
    p1.save()
    cursor = Persona.find({'nombre': 'Sebas'})
    print(cursor.next())

    """
        Pruebas de GeoJSON
    """
    
    ubi = getCityGeoJSON('Madrid')
    print(ubi)
