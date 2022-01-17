''' CONSTANTS : MEANING
    "ouid" : "Unique ID for the carrier's current star",
    "l": "Unknown",
    "lx": "Previous x coordinate",
    "ly": "Previous y coordinate",
    "n": "Name of carrier",
    "o": "List of orders",
    "puid": "Player ID of the owner",
    "st": "Number of ships (strength)",
    "uid": "Unique ID of the carrier",
    "x": "Current x location",
    "y": "Current y location"
'''
import __init__
from consts import PIDS
from utils.utils import pid_to_name

class Fleet():
    def __init__(self, json):
        
        # Unique identifiers
        self.ouid = False
        if 'ouid' in json:
            self.ouid = json['ouid'] # This will only exist if it is currently at a star

        self.puid = json['puid']
        self.uid = json['uid']

        # Position
        self.lx = json['lx']
        self.ly = json['ly']
        self.x = json['x']
        self.y = json['y']

        # Other factors
        self.strength = json['st']
        self.name = json['n']
        self.orders = json['o']

        self.watching = False
    
    def get_owner_id(self):
        return self.puid
    
    def get_owner_name(self):
        return pid_to_name(self.puid)

    # need some tests...
    def is_id_owner_of(self, id: int):
        if id == self.puid:
            return False
        return True

    def is_moving(self):
        return not self.ouid

    def __str__(self):
        if self.is_moving():
            return f"(****) ({self.name} [{self.get_owner_name()}]): {self.strength} ships (MOVING) (****)"
        return f"({self.name} [{self.get_owner_name()}]): {self.strength} ships"