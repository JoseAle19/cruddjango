from bson import json_util
from django.shortcuts import render, redirect

# time
from datetime import datetime


# ymongo 
from pymongo import MongoClient
# django http
from django.http import JsonResponse
# json
import json
# bson
from bson.objectid import ObjectId

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST



urlConnection = 'mongodb://localhost:27017'



def convertir_a_cadena(objeto):
    if isinstance(objeto, ObjectId):
        return str(objeto)
    raise TypeError(f"Tipo no serializable: {type(objeto)}")



@csrf_protect
@require_POST
def connect_to_mongodb():
    try:
        client = MongoClient(urlConnection)
        db = client['crudUsers']
        return db['user'], None
    except Exception as e:
        return None, f"Error de conexión: {e}"


def crear_usuarios(request):
    message = ""
    status = ""
    users = []
    users_str = []
    if request.method == "POST":
        username = request.POST.get('username')
        date_from = request.POST.get('dateFrom')
        date_to = request.POST.get('dateTo')
        passw = request.POST.get('pass')
        edoCta = request.POST.get('edoCta')
        print("username",edoCta)
        try:
            client = MongoClient(urlConnection)

            db = client['crudUsers']
            # add data in collection
            collection = db['user']
            if collection.find_one({"login":username}):
                message = "Ya existe el usuario"
                status = False
            else:
                message = "Usuario creado correctamente"
                data = {
                    "login": username,
                    'password': passw,
                    "fecIni": date_from,
                    "fecFin": date_to,
                    "EdoCta": False if edoCta == "false" else True
                }
                collection.insert_one(data)
                status = True
        except Exception as e :
            print(e)
            print("Error de conexion")
 
        users_cursor = collection.find({}, {"_id": 0})
        users = [user for user in users_cursor]
        users_str = [{k: str(v) if isinstance(v, ObjectId) else v for k, v in user.items()} for user in users]
        # parsera a json  users_str 
        users_cursor1 = collection.find({})
        users_list1 = list(users_cursor1)
        for user in users_list1:
            user['id'] = str(user['_id'])

        users_str_json = json.dumps(users_list1, default=convertir_a_cadena)
        return JsonResponse({'message': message, 'status': status, 'users': users_str, 'users_str_json': users_str_json})
    # ACa es para peticion get 
    if request.method == "GET":
        try:
            client = MongoClient(urlConnection)

            db = client['crudUsers']
            # add data in collection
            collection = db['user']
        except Exception as e :
            print(e)
            print("Error de conexion")
           # Consulta todos los usuarios y convierte el resultado a una lista
        users_cursor = collection.find({})
        users_list = list(users_cursor)
        for user in users_list:
            user['id'] = str(user['_id'])
        users_str = users_list

        # meotodo put
    if request.method == "PUT":
        data = json.loads(request.body.decode('utf-8'))
           # Acceder a los datos individualmente
        username = data.get('username')
        idUser = data.get('id')
        date_from = data.get('dateFrom')
        date_to = data.get('dateTo')
        passw = data.get('pass')
        edoCta = data.get('edoCta')
        try:
            client = MongoClient(urlConnection)

            db = client['crudUsers']
            # add data in collection
            collection = db['user']
        except Exception as e :
            print(e)
            print("Error de conexion")
        result = collection.update_one({"_id": ObjectId(idUser)}, {"$set": {"login": username, 'password': passw, "fecIni": date_from, "fecFin": date_to,
         "EdoCta": edoCta}})    
        if result.modified_count == 0:
            
            return JsonResponse({'message': 'No se encontro el usuario', 'status': False, 'users': getuser()})
        
        users_cursor = collection.find({}, {"_id": 0})
        users = [user for user in users_cursor]
        users_str = [{k: str(v) if isinstance(v, ObjectId) else v for k, v in user.items()} for user in users]
         # parsera a json  users_str 
        users_cursor1 = collection.find({})
        users_list1 = list(users_cursor1)
        for user in users_list1:
            user['id'] = str(user['_id'])

        users_str_json = json.dumps(users_list1, default=convertir_a_cadena)
        return JsonResponse({'message': 'Usuario actualizado', 'status': True, 'users': users_str, 'users_str_json': users_str_json})
    # metodo delete para eeiminar usuario
    if request.method == "DELETE":
        data = json.loads(request.body.decode('utf-8'))
        idUser = data.get('id')
        try:
            client = MongoClient(urlConnection)

            db = client['crudUsers']
            # add data in collection
            collection = db['user']
        except Exception as e :
            print(e)
            print("Error de conexion")
        result = collection.delete_one({"_id": ObjectId(idUser)})    
        if result.deleted_count == 0:
            return JsonResponse({'message': 'No se encontro el usuario', 'status': False, 'users': getuser()})
        users_cursor = collection.find({}, {"_id": 0})
        users = [user for user in users_cursor]
        users_str = [{k: str(v) if isinstance(v, ObjectId) else v for k, v in user.items()} for user in users]
         # parsera a json  users_str 
        users_cursor1 = collection.find({})
        users_list1 = list(users_cursor1)
        for user in users_list1:
            user['id'] = str(user['_id'])

        users_str_json = json.dumps(users_list1, default=convertir_a_cadena)
        return JsonResponse({'message': 'Usuario eliminado', 'status': True, 'users': users_str, 'users_str_json': users_str_json})
       
    return render(request, 'users/user_template.html', {'users': users_str})





def my_account(request):
    if request.method == "PUT":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        idUser = data.get('id')
        date_from = data.get('dateFrom')
        date_to = data.get('dateTo')
        passw = data.get('pass')
        edoCta = data.get('edoCta')
        print("id--------------",idUser)
        try:
            client = MongoClient(urlConnection)

            db = client['crudUsers']
            # add data in collection
            collection = db['user']
        except Exception as e :
            print(e)
            print("Error de conexion")
        result = collection.update_one({"_id": ObjectId(idUser)}, {"$set": {"login": username, 'password': passw, "fecIni": date_from, "fecFin": date_to,
         "EdoCta": edoCta}})    
        if result.deleted_count == 0:
            return JsonResponse({'message': 'No se encontro el usuario', 'status': False, 'users': []})
        users_cursor = collection.find({}, {"_id": 0})
        users = [user for user in users_cursor]
        users_str = [{k: str(v) if isinstance(v, ObjectId) else v for k, v in user.items()} for user in users]
         # parsera a json  users_str 
        users_cursor1 = collection.find({})
        users_list1 = list(users_cursor1)
        for user in users_list1:
            user['id'] = str(user['_id'])

        users_str_json = json.dumps(users_list1, default=convertir_a_cadena)
        return JsonResponse({'message': 'Usuario eliminado', 'status': True, 'users': users_str, 'users_str_json': users_str_json})

    return render(request, 'users/my_account.html', {})






def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        passw = request.POST.get('pass')
        try:
            client = MongoClient(urlConnection)

            db = client['crudUsers']
            # add data in collection
            collection = db['user']
        except Exception as e :
            print(e)
            print("Error de conexion")
        users_cursor = collection.find({"login":username, "password":passw}, {"_id": 0})
        users = [user for user in users_cursor]
        users_str = [{k: str(v) if isinstance(v, ObjectId) else v for k, v in user.items()} for user in users]

        # user json
           # parsera a json  users_str 
        users_cursor1 = collection.find({"login":username, "password":passw})
        # users_cursor1 = collection.find({})
        users_list1 = list(users_cursor1)
        for user in users_list1:
            user['id'] = str(user['_id'])

        users_str_json = json.dumps(users_list1, default=convertir_a_cadena)

        if users_str:
            if is_calid_date_from(users_str[0]['fecIni']):
                if is_calid_date_to(users_str[0]['fecFin']):
                    return JsonResponse({'message': 'Hola '+username , 'status': True, 'user': users_str[0], 'users_str_json': users_str_json}) 
                else:
                    return JsonResponse({'message': "Cuenta esta descativada", 'status': False,}) 
            else:
                return JsonResponse({'message': "Cuenta aun no esta activa, fecha de activacion "+users_str[0]['fecIni'], 'status': False,}) 

            # return JsonResponse({'message': 'Hola '+username , 'status': True, 'user': users_str[0]}) 
        else:
            print("no entro")
            return JsonResponse({'message': 'Usuario o contraseña incorrectos', 'status': False}) 
    return render(request, 'users/login.html', {})


def is_valid_date_range(start_date_str, end_date_str):
    # Convierte las cadenas de fecha a objetos de fecha
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Obtiene la fecha actual
    current_date = datetime.now().date()

    # Comprueba si la fecha actual está dentro del rango
    return start_date >= current_date <= end_date

def is_calid_date_to(date_to_str):
    # Convierte las cadenas de fecha a objetos de fecha
    end_date = datetime.strptime(date_to_str, '%Y-%m-%d').date()

    # Obtiene la fecha actual
    current_date = datetime.now().date()

    # Comprueba si la fecha actual está dentro del rango
    return current_date <= end_date

def is_calid_date_from(date_from_str):
    # Convierte las cadenas de fecha a objetos de fecha
    start_date = datetime.strptime(date_from_str, '%Y-%m-%d').date()

    # Obtiene la fecha actual
    current_date = datetime.now().date()

    # Comprueba si la fecha actual está dentro del rango
    return start_date <= current_date

def update_user_status(name, edoCta):

    collection, error  =    connect_to_mongodb()
    if error:
         return error
    else:
        try:
            collection.update_one({"login":name}, {"$set": {"EdoCta": edoCta}})
        except Exception as e:
            return f"Error al actualizar el usuario {e}"
        return "Usuario actualizado correctamente"







def getuser():
    users_str = []
    try:
        client = MongoClient(urlConnection)

        db = client['crudUsers']
        # add data in collection
        collection = db['user']
    except Exception as e :
       users_cursor = collection.find({}, {"_id": 0})
       users = [user for user in users_cursor]
       users_str = [{k: str(v) if isinstance(v, ObjectId) else v for k, v in user.items()} for user in users]
    return users_str