import __init__
from __init__ import db
from data.Fleet import Fleet
from datetime import datetime

def find_fleet(fleet: Fleet):
    fleet_ref = db.collection('fleets').document(str(fleet.uid))
    doc = fleet_ref.get()

    if doc.exists:
        return True
    else:
        return False

def set_fleet(fleet: Fleet):
    data = {
        "uid": fleet.uid,
        "seen": True, # if the player has seen this yet (AT THE MOMENT YES. LATER, ADD RESPONSE)
        "notified": datetime.now() # this doesn't matter too much.
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

# follower functions down the line

# maybe store notifications as well?

# store alliance user data as well...