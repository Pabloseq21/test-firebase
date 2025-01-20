import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the Firebase app
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)



# Initialize Firestore
db = firestore.client()

# Example function to add data to Firestore
def add_data(collection_name, document_name, data):
    db.collection(collection_name).document(document_name).set(data)

# Example usage
data = {
    'name': 'John Doe',
    'age': 30,
    'email': 'johndoe@example.com'
}
add_data('users', 'user1', data)