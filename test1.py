#importacion de las librerias a utilizar desde firebase_admin

import firebase_admin
from firebase_admin import credentials, firestore, db, auth

# iniciar la Firebase app, con las credenciales del proyecto
cred = credentials.Certificate('testpython-673c0.json')
firebase_admin.initialize_app(cred, {"databaseURL": "https://testpython-673c0-default-rtdb.firebaseio.com/"})

ref = db.reference('users')

# inicializar firestore
db = firestore.client()

# funcion para añadir datos a la base de datos en firebase 
def add_data(collection_name, document_name, data):
    db.collection(collection_name).document(document_name).set(data)
    print(f"Datos añadidos a {collection_name}/{document_name}") 
#creacion de nuevos usuarios con correo , nombre y contraseña 
#funcion para generar un nuevo usuario con correo, nombre y contraseña, usamos auth para la autentificacion de usuarios 

def sing_up(email, name, password):
    try:
        user = auth.create_user(
        email=email,
        display_name=name,
        password=password
        
    )
        print(f"Usuario creado: {user.uid}")
    except Exception as e: 
        print(f"Error: {e}")    

# inicio de secion para usuarios con correo , nombre y contraseña 
#importar la libreria requests de http
import requests

#funcion para iniciar sesion, junto con la url de la api y la llave de la api para asociarlo con el proyecto de firebase
#se crea un diccionario con los datos del usuario y se envia a la api, la cual verifica que el usuario y contraseña sean correctos y devuelve un token de inicio de sesion

def sign_in(email, name, password):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    api_key = "testpython-673c0.json" 
    payload = {
        "email": email,
        "displayName": name,
        "password": password,
        "returnSecureToken": True
    }
    try:
        response = requests.post(f"{url}?key={api_key}", json=payload)
        response_data = response.json()
        if response.status_code == 200:
            print(f"Inicio de sesión exitoso. ID Token: {response_data['idToken']}")
        else:
            print(f"Error: {response_data['error']['message']}")
    except Exception as e:
        print(f"Error en el inicio de sesión: {e}")
