import firebase_admin
from firebase_admin import credentials, firestore


# Inicializar Firebase Admin SDK
cred = credentials.Certificate("firebaseadmin_rulfo.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

