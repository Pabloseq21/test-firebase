import firebase_admin
from firebase_admin import credentials, firestore,db

# Initialize the Firebase app
cred = credentials.Certificate('testpython-673c0.json')
firebase_admin.initialize_app(cred, {"databaseURL": "https://testpython-673c0-default-rtdb.firebaseio.com/"})

ref = db.reference('users')

# Initialize Firestore
db = firestore.client()

# Example function to add data to Firestore 
def add_data(collection_name, document_name, data):
    db.collection(collection_name).document(document_name).set(data)

# Example usage
ref.set({ 
    'usuario': input ("ingrese su usuario: "),
    'email': input('ingrese su email: ')
}
add_data('users', 'user1', registro)