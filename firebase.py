import firebase_admin
from firebase_admin import credentials, auth, db
import requests

# Inicializar Firebase con las credenciales
def initialize_firebase():
    cred = credentials.Certificate('testpython-673c0-firebase-adminsdk-b93r7-3f13d33808.json')
    firebase_admin.initialize_app(cred, {"databaseURL": "https://testpython-673c0-default-rtdb.firebaseio.com/"})
    print("Firebase inicializado.")

# Función para registrar un nuevo usuario en Firebase Authentication
def sign_up(email, password, display_name):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        print(f"\n¡Usuario registrado exitosamente!")
        print(f"Usuario creado: {user.uid}")
        print(f"Nombre: {user.display_name}")
        print(f"Email: {user.email}")
        
        # Agregar el usuario a la base de datos Realtime
        ref = db.reference(f'users/{user.uid}')
        ref.set({
            'email': email,
            'display_name': display_name,
            'score': 0,
            'level': 0
        })
        print("Usuario agregado a la base de datos.")
    except Exception as e:
        print(f"Error: {e}")

# Función para iniciar sesión
def sign_in(email, password, api_key):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    try:
        
        response = requests.post(f"{url}?key={api_key}", json=payload)
        response_data = response.json()
        
        # Verificar si el inicio de sesión fue exitoso
        if response.status_code == 200:
            print(f"\nBienvenido al juego!")
            return response_data['idToken']  
        else:
            print(f"Error: {response_data['error']['message']}")
            return None
    except Exception as e:
        print(f"Error en el inicio de sesión: {e}")
        return None

# Función para actualizar el nivel del usuario
def update_level(user_id, level ):
    try:
        ref = db.reference(f'users/{user_id}')
        ref.update({'level': level})
        print(f"¡Felicidades! Avanzaste al nivel: {level}.")
    except Exception as e:
        print(f"Error al actualizar el nivel: {e}")
        
# Función para actualizar la puntuación del usuario
def update_score(user_id, score):
    try:
        ref = db.reference(f'users/{user_id}')
        ref.update({'score': score})
        print(f"Puntuación actualizada: {score} puntos.")
    except Exception as e:
        print(f"Error al actualizar la puntuación: {e}")

# Función para ver el top 3 de las mejores puntuaciones
def show_top_scores():
    try:
        # Obtener todos los usuarios con sus puntuaciones
        ref = db.reference('users')
        users_data = ref.get()
        
        # Filtrar y ordenar los usuarios por puntuación
        top_scores = []
        for user_id, user_info in users_data.items():
            # Verificar si 'score' y 'display_name' existen
            if 'score' in user_info and 'display_name' in user_info:
                top_scores.append((user_info['display_name'], user_info['score']))
        
        # Ordenar de mayor a menor
        top_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Mostrar los 3 mejores
        print("\nTop 3 de los mejores jugadores:")
        for idx, (name, score) in enumerate(top_scores[:3]):
            print(f"{idx + 1}. {name} - {score} puntos")
        
        if not top_scores:
            print("No hay puntuaciones registradas aún.")
    
    except Exception as e:
        print(f"Error al obtener el top de puntuaciones: {e}")

# Función principal para el flujo interactivo
def main():
    print("Bienvenido, por favor ingresa tus datos.")
    
    # Solicitar el correo y contraseña
    email = input("Introduce tu correo electrónico: ")
    password = input("Introduce tu contraseña: ")
    
    # Verificar si el usuario existe en Firebase Authentication
    try:
        user = auth.get_user_by_email(email)
        print(f"Usuario encontrado: {user.display_name}")
        
        # Si el usuario existe, iniciar sesión
        api_key = "AIzaSyBN0ttX9ElGFnmaO0y2HLZEv1HAjnd8cgc"  # Reemplazar con tu clave API de Firebase
        id_token = sign_in(email, password, api_key)
        
        if id_token:
            # Inicializa la puntuación antes del juego
            score = 0  # Puntuación inicial (puedes cargarla de la base de datos si lo prefieres)
            
            # Menú de juego
            while True:
                print("\nMenú de juego:")
                print("1. Jugar")
                print("2. Ver a los mejores de los mejores")
                print("3. Salir")
                
                choice = input("Selecciona una opción: ")
                
                if choice == '1': # Jugar
                    while True:
                        print("\nMapas : ")
                        print("a.city")
                        print("b.bosque del terror")
                        print("c.cabaña")
                        print("d.salir")
                        choice = input("Selecciona un mapa : " )
                        if choice == 'a' :
                            print ("entraste a nivel a")
                            score = int(input("Introduce tu puntuación obtenida: "))
                            update_score(user.uid, score)
                            if score > 50 :
                                print ("¡Felicidades! Pasaste al siguiente nivel")
                        if choice == 'b' :
                            if score > 50 :
                                print ("entraste al nivel b")
                                score = int(input("Introduce tu puntuación obtenida: "))
                                update_score(user.uid, score)
                            else :
                                print("Para pasar al nivel b tienes que tener más de 50 puntos")
                                
                            if score > 100 : 
                                print ("¡Felicidades! Pasaste al siguiente nivel")
                        if choice == 'c' :
                            if score > 200:
                                print("entraste al nivel c")
                                
                                score = int(input("Introduce tu puntuación obtenida: "))
                                update_score(user.uid, score)
                            else:
                                print ("¡Felicidades! Completaste el juego")
                        if choice == 'd':  
                           print("Gracias por jugar, ¡hasta la próxima!")
                           break
                        else:
                            print("Opción no válida. Por favor, elige una opción válida.")
                
                elif choice == '2':  # Ver el top 3
                    show_top_scores()
                
                elif choice == '3':  # Salir
                    print("Gracias por jugar, ¡hasta la próxima!")
                    break
                
                else:
                    print("Opción no válida. Por favor, elige una opción válida.")
    
    except auth.UserNotFoundError:
        # Si el usuario no existe, solicitar los datos para registrarlo
        print("Usuario no encontrado.")
        display_name = input("Introduce tu nombre de usuario: ")
        
        # Registrar nuevo usuario
        sign_up(email, password, display_name)

# Ejecutar el flujo principal
if __name__ == "__main__":
    initialize_firebase()  # Inicializar Firebase
    main()  # Ejecutar el flujo de inicio de sesión y registro
