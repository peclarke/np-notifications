from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials
#from google.cloud import firestore
from firebase_admin import firestore
load_dotenv()


cred = credentials.Certificate('./FirebaseAdmin.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()