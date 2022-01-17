import __init__
from __init__ import db
from data.Fleet import Fleet
from datetime import datetime
from google.cloud import firestore

def does_fleet_exist(fleet: Fleet):
    fleet_ref = db.collection('fleets').document(str(fleet.uid))
    doc = fleet_ref.get()
    return doc.exists

def get_fleet(fleet: Fleet):
    fleet_ref = db.collection('fleets').document(str(fleet.uid))
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

def reset_fleets(fleet: Fleet):
    try:
        db.collection('fleets').document(str(fleet.uid)).delete()
    except Exception as e:
        print(f'An exception occured: {e}')

def get_all_fleets():
    docs = db.collection('fleets').stream()
    return docs

def set_missing_fleet(uid: int, notified):
    data = {
        "uid": uid,
        "first_seen": notified
    }
    missing_ref = db.collection('missing')
    missing_ref.document(str(uid)).set(data)

def remove_fleet_uid(uid: int):
    try:
        db.collection('fleets').document(str(uid)).delete()
    except Exception as e:
        print(f'An exception occured: {e}')

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

def remove_alliance(uid: int):
    try:
        db.collection('alliances').document(str(uid)).delete()
    except Exception as e:
        print(f'An exception occured: {e}')

'''
Gets the ally's information from the database. Will return their uid
and their api_key to be used in any calculations. 
'''
def get_ally_info(uid: int):
    fleet_ref = db.collection('is_alliance').document(str(uid))
    doc = fleet_ref.get()
    return doc.to_dict()

# follower functions down the line

# maybe store notifications as well?