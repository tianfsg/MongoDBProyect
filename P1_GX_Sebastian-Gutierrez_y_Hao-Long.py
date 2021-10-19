__author__ = 'Hao_Long_y_Sebastian_Gutierrez'

import pymongo
import json
import dateutil
from dateutil import parser
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
    location = geolocator.geocode(address).point
    return [location.latitude, location.longitude]
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
        loc_aux = None
        if '_id' in kwargs:
            id_aux = kwargs['_id']
            kwargs.pop('_id')
        if 'loc' in kwargs:
            loc_aux = kwargs['loc']
            kwargs.pop('loc')

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

        if loc_aux != None:
            self.loc = loc_aux

        kwargs['loc'] = getCityGeoJSON(kwargs['ciudad'])
        self.__dict__.update(kwargs)


    def save(self):
        try:
            if hasattr(self, '_id'): #Significa que existe en la BD
                values = {'$set': self.mod}
                self.db.persona.update_one({'_id': self._id.inserted_id}, values)
                print("\nSe ha actualizado correctamente.")
            else: #No existe en la BD
                self._id = self.db.persona.insert_one(self.__dict__)
                print('Se ha registrado correctamente.')
        except Exception:
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
        Persona.db.persona.create_index([("loc", pymongo.GEOSPHERE)])

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
        loc_aux = None
        if '_id' in kwargs:
            id_aux = kwargs['_id']
            kwargs.pop('_id')

        if 'loc' in kwargs:
            loc_aux = kwargs['loc']
            kwargs.pop('loc')

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

        if loc_aux != None:
            self.loc = loc_aux
        
        kwargs['loc'] = getCityGeoJSON(kwargs['localizacion'])
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
            print('\n\nERR: Algo ha fallado en Centro.save()')

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
            required_vars = nothing[0].split(',')
            admissible_vars = nothing[1].split(',')
            file.close()
        except:
            print('el fichero de vars no existe')

        Centro.required_vars = required_vars
        Centro.admissible_vars = admissible_vars
        Centro.db = db
        #Centro.db.centro.create_index('', unique = True)

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
        loc_aux = None
        if '_id' in kwargs:
            id_aux = kwargs['_id']
            kwargs.pop('_id')

        if 'loc' in kwargs:
            loc_aux = kwargs['loc']
            kwargs.pop('loc')

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

        if loc_aux != None:
            self.loc = loc_aux

        kwargs['loc'] = getCityGeoJSON(kwargs['localizacion'])
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
            print('\n\nERR: Algo ha fallado en Empresa.save()')

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
            required_vars = nothing[0].split(',')
            admissible_vars = nothing[1].split(',')
            file.close()
        except:
            print('el fichero de vars no existe')

        Empresa.required_vars = required_vars
        Empresa.admissible_vars = admissible_vars
        Empresa.db = db
        #Empresa.db.empresa.create_index('', unique = True)


nombre = 'Definir'

"""
    <QUERIES>
"""

Q1 = [{'$match': {'ciudad':'Huelva'}}]
Q2 = [{'$match': {'estudios.universidad': {'$in': ['UAM', 'UPM']}}}]
Q3 = [{'$group': {'_id':"$ciudad"}}]
Q4 = [{'$geoNear':{'near': {'type':'Point', 'coordinates': [ 40.4167047, -3.7035825 ]}, 'distanceField': 'dist.calculated', 'maxDistance': '700000', 'includeLocs':'dist.locstion', 'spherical': 'true'}}, {'$sort':{'dist.calculated': 1}}, {'$limit': 10}]
dateStr = "2017-01-01T00:00:00Z"
myDatetime = dateutil.parser.parse(dateStr)
Q5 = [{'$unwind':"$estudios"}, {'$match':{'$expr':{'$gte':[{'$dateFromString':{'dateString': "$estudios.final", 'format': "%d/%m/%Y"}}, myDatetime]}}},{'$group':{'_id': "$_id", 'nombre':{'$first': "$nombre.nombre"}, 'apellido':{'$first': "$nombre.apellido"}, 'fechaFinal':{'$first':"$estudios.final"}}},{'$out': {'db': "mongoproyect2", 'coll': "after2017"}}]
Q6 = [{'$match':{"trabajo.empresa":"UPM"}},{'$group':{'_id':"",'avg_estudios':{'$avg':{'$size': "$estudios"}}}}]
Q7 = [{'$unwind':"$estudios"}, {'$group':{'_id':"$estudios.universidad", 'count': {'$sum': 1}}}, {'$sort':{'count': -1}}, {'$limit': 3}]


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    Persona.init_class(client['mongoproyect'])
    Empresa.init_class(client['mongoproyect'])
    Centro.init_class(client['mongoproyect'])

    json_db = client['mongoproyect2']
    collection_persona = json_db['persona']
    with open('redES.json') as f:
        file_data = json.load(f)
    collection_persona.insert_many(file_data)



    """
        Pruebas de funcionamieto de Modelo() 

            save() - Condicion (_id) ? update_one() : insert_one()
            set(filter) - Modifies the actual object.
            cursor - Gets the actual document.
    """

    persona = {'nombre': 'Sebas', 'apellido': 'Guti', 'telefono': '655408703','nif': 'eiror3iri', 'ciudad':'A Coruña'}
    centro = {'nombre': 'UPM', 'localizacion': 'Vallecas'}
    empresa = {'nombre': 'U-tad', 'localizacion': 'Las Matas'}

    p1 = Persona(**persona)
    p1.save()
    p1.set(**{'telefono': '74837492'})
    p1.save()
    cursor = Persona.find({'nombre': 'Sebas'})
    print(cursor.next())

    c1 = Centro(**centro)
    c1.save()
    c1.set(**{'nombre': 'Universidad Politecnica de Madrid'})
    c1.save()
    cursor2 = Centro.find({'nombre': 'Universidad Politecnica de Madrid'})
    print(cursor2.next())

    e1 = Empresa(**empresa)
    e1.save()
    e1.set(**{'nombre': 'Universidad de Tecnologia y Arte Digital'})
    e1.save()
    cursor3 = Persona.find({'nombre': 'Universidad de Tecnologia y Arte Digital'})
    print(cursor3.next())

    """
        Pruebas de GeoJSON
    """
    
    # ubi = getCityGeoJSON('Madrid')
    # print(ubi)

    """
        Aggregate con pipelines
    """
    A1 = collection_persona.aggregate(Q1)
    print(list(A1))

    A2 = collection_persona.aggregate(Q2)
    print(list(A2))

    A3 = collection_persona.aggregate(Q3)
    print(list(A3))

    A4 = client['mongoproyect'].persona.aggregate(Q4)
    print(list(A4))

    A5 = collection_persona.aggregate(Q5)
    print(list(A5))
    for x in json_db.after2017.find():
        print(x)

    A6 = collection_persona.aggregate(Q6)
    print(list(A6))

    A7 = collection_persona.aggregate(Q7)
    print(list(A7))

#TODO Arreglar la Q4 y la Q5
    #Q4 tiene problemas de tipo con 2dSphere
    #Q5 no pasa bien los '%' del formato de las fechas
#TODO Arreglar ModelCursor, el next ha dejado de funcionar
#TODO Que se actualize 'loc' en el SET
#TODO debug final
