import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"database-access-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {'test category': 'test data', 'test category2': 'test data2'}

doc_ref = db.collection('testCollection').document()
doc_ref.set(data)

print('Document ID:', doc_ref.id)
