from typing import Any
from data.Fleet import Fleet
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
#from google.cloud import firestore
from firebase_admin import firestore

from data.Star import Star
#from google.cloud import firestore

cred = credentials.Certificate('FirebaseAdmin.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def does_fleet_exist(fleet: Fleet):
    fleet_ref = db.collection('fleets').document(str(fleet.uid))
    doc = fleet_ref.get()
    return doc.exists

def get_fleet(fleet: Fleet):
    fleet_ref = db.collection('fleets').document(str(fleet.uid))
    return fleet_ref.get().to_dict()

def get_fleet_by_uid(uid: int):
    fleet_ref = db.collection('fleets').document(str(uid))
    return fleet_ref.get().to_dict()

def set_fleet(fleet: Fleet, seen_by: int):
    data = {
        "uid": fleet.uid,
        "seen": True, # if the player has seen this yet (AT THE MOMENT YES. LATER, ADD RESPONSE)
        "notified": firestore.SERVER_TIMESTAMP,
        "owner": fleet.puid,
        "seen_by": seen_by,
        "strength": fleet.strength,
        "name": fleet.name
    }
    fleet_ref = db.collection('fleets')
    fleet_ref.document(str(fleet.uid)).set(data)

def set_old_fleet(uid: int, data: Any):
    missing_ref = db.collection('old_fleets')
    missing_ref.add(data)

def get_all_old_fleets():
    oldies = db.collection('old_fleets').stream()
    return oldies

def reset_fleets(fleet: Fleet):
    try:
        removing: Fleet = get_fleet(fleet)
        db.collection('fleets').document(str(fleet.uid)).delete()
        return removing
    except Exception as e:
        print(f'An exception occured: {e}')

def get_all_fleets():
    docs = db.collection('fleets').stream()
    return docs

def remove_fleet_uid(uid: int):
    try:
        removing: Fleet = get_fleet_by_uid(uid)
        db.collection('fleets').document(str(uid)).delete()
        return removing
    except Exception as e:
        print(f'An exception occured: {e}')

def get_aggregate_fleet_info(uid: int):
    # get all documents of the fleet uid from fleets and old_fleets

    # order in ascending order
    pass

# store alliance user data as well...
def get_all_alliances():
    docs = db.collection('alliances').stream()
    alliances = []
    # exclude yourself from the alliance list
    for a in docs:
        if len(a.id) < 15:
            info = a.to_dict()
            alliances.append(a.to_dict())
    return alliances

def is_alliance(uid: int): # checks if user is allied with you
    fleet_ref = db.collection('is_alliance').document(str(uid))
    doc = fleet_ref.get()
    return doc.exists

def remove_ally(uid: int):
    try:
        db.collection('alliances').document(str(uid)).delete()
    except Exception as e:
        print(f'An exception occured: {e}')

'''
Gets the ally's information from the database. 
Will return their uid, api_key, phone, name.
'''
def get_ally_info(uid: int):
    alliance_ref = db.collection('alliances').document(str(uid))
    doc = alliance_ref.get()
    return doc.to_dict()

def add_ally(uid: int, api_key: str, phone: str, name: str):
    alliance_ref = db.collection('alliances').document(str(uid))
    data = {
        "uid": uid,
        "api_key": api_key,
        "phone": phone,
        "name": name
    }
    alliance_ref.document(str(uid)).set(data)

def add_star(star: Star):
    if star.is_visible():
        data = {
            "uid": star.uid,
            "owner": star.owner,
            "ships": star.get_num_ships(),
            "name": star.name,
            "points": star.get_points(),
            "net_resources": star.net_resources,
            "x": star.x,
            "y": star.y,
            "time_recorded": firestore.SERVER_TIMESTAMP,
        }
        fleet_ref = db.collection('stars')
        fleet_ref.add(data)

def get_all_stars():
    stars_ref = db.collection('stars').stream()
    return [doc.to_dict() for doc in stars_ref]