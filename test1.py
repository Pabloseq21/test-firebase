#importacion de las librerias a utilizar desde firebase_admin

import firebase_admin
from firebase_admin import credentials, firestore, db, auth

#funcion para inicializar firebase con la llave de autentificacion del proyecto de firebase 

def initialize_firebase():
    cred = credentials.Certificate('testpython-673c0.json')
    firebase_admin.initialize_app(cred, {"databaseURL": "https://testpython-673c0-default-rtdb.firebaseio.com/"})

    print("Firebase inicializado")

# funcion para añadir datos a la base de datos en firebase 
def add_data(collection_name, document_name, data):
    db.collection(collection_name).document(document_name).set(data)
    print(f"Datos añadidos a {collection_name}/{document_name}") 

#creacion de nuevos usuarios con correo , nombre y contraseña (el usuario desea crear una cuenta para jugar o ver su informacion)
#funcion para generar un nuevo usuario con correo, nombre y contraseña, usamos auth para la autentificacion de usuarios 

def sign_up(email, name, password):
    try:
        user = auth.create_user(
        email = email,
        display_name = name,
        password = password)
        print (f"\n¡Usuario registrado exitosamente!")
        print(f"Usuario creado: {user.uid}")
        print(f"Nombre: {user.display_name}")
        print(f"Email: {user.email}")
    except Exception as e: 
        print(f"Error: {e}")   


def main():
    print("__ Registro de Usuario __")
    display_name = input("Introduce tu nombre de usuario: ")
    email = input("Introduce tu correo electrónico: ")
    password = input("Introduce tu contraseña: ")
    
    # Validar entradas 
    if not display_name or not email or not password:
        print("\nTodos los campos son obligatorios.")
        return 

    sign_up(email, display_name, password)
if __name__ == "__main__":
    initialize_firebase()  # Inicializar Firebase
    main()  # Ejecutar la aplicación

# inicio de secion para usuarios con correo , nombre y contraseña 
#importar la libreria requests de http
import requests

#(el usuario desea iniciar secion para jugar o ver su informacion)
#funcion para iniciar sesion, junto con la url de la api y la llave de la api para asociarlo con el proyecto de firebase
#se crea un diccionario con los datos del usuario y se envia a la api, la cual verifica que el usuario y contraseña sean correctos y devuelve un token de inicio de sesion

def sign_in(email, name, password):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    api_key = "testpython-673c0.json" 
    payload = {
        "email": input ("email"),
        "displayName": input ("name"),
        "password": input ("password"),
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

#  para actualizar el nombre de un usuario en firebase (el usuario desea actualizar su nombre o cambiarlo)
def update_user(uid, name):
    try:
        user = auth.update_user(uid, display_name="new name")
        print(f"Nombre de usuario actualizado: {user.display_name}")
    except Exception as e:
        print(f"Error al actualizar el nombre del usuario: {e}")

# recuperar el nombre de un usuario (el usuario desea recuperar su nombre ya que se le perdio o no lo recuerda)
def get_user_info(uid):
    try:
        user = auth.get_user(uid)
        print(f"Usuario: {user.uid}")
        print(f"Correo electrónico: {user.email}")
        print(f"Nombre: {user.display_name}")
    except Exception as e:
        print(f"Error al obtener la información del usuario: {e}")
