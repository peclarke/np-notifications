import pytest
from unittest import mock
import os
from data.Star import Star
from main import NeptunesPrideStatus
from data.Fleet import Fleet

ROOT = "https://np.ironhelmet.com/api"
PARAMS = {
            "game_number": os.getenv("CURRENT_GAME_ID"),
            "code": os.getenv("API_KEY"),
            "api_version": os.getenv("API_VERSION")
        }

def mock_request(root, params):
    return True

@pytest.fixture
def fleet_one():
    f1: Fleet = Fleet(SAMPLE_FLEET) # non-moving
    yield f1

@pytest.fixture
def fleet_two():
    f2: Fleet = Fleet(SAMPLE_FLEET_2) # moving
    yield f2

@pytest.fixture
def fleet_three():
    f3: Fleet = Fleet(SAMPLE_FLEET_3) # your fleet
    yield f3

@pytest.fixture
def star_one():
    s1: Star = Star(SAMPLE_STARS["1"])
    yield s1 # a star which is not within scanning range

@pytest.fixture
def star_two():
    s2: Star = Star(SAMPLE_STARS["16"])
    yield s2 # a star which is visible to you (your own)

@pytest.fixture
def status(fleet_one, fleet_two, fleet_three, star_one, star_two):
    np: NeptunesPrideStatus = NeptunesPrideStatus(ROOT, PARAMS, "4", "+61448715179")
    np.fleets = [fleet_one, fleet_two, fleet_three]
    np.stars = [star_one, star_two]
    yield np

SAMPLE_STARS = {
    "1": {
        "uid": 1,
        "n": "Kit",
        "puid": 6,
        "v": "0",
        "y": "0.9045",
        "x": "0.4258"
    },
    "2": {
        "uid": 2,
        "n": "Birdun",
        "puid": 5,
        "v": "0",
        "y": "0.9045",
        "x": "1.9258"
    },
    "3": {
        "uid": 3,
        "n": "Zu",
        "puid": 2,
        "v": "0",
        "y": "-0.3945",
        "x": "1.1758"
    },
    "4": {
        "uid": 4,
        "n": "SteropeII",
        "puid": 0,
        "v": "0",
        "y": "0.9045",
        "x": "-1.0742"
    },
    "5": {
        "uid": 5,
        "n": "Aldib",
        "puid": 0,
        "v": "0",
        "y": "2.2036",
        "x": "-0.3242"
    },
    "6": {
        "uid": 6,
        "n": "Dheneb",
        "puid": 4,
        "v": "0",
        "y": "-0.3945",
        "x": "-0.3242"
    },
    "7": {
        "uid": 7,
        "n": "Saw",
        "puid": 3,
        "v": "0",
        "y": "2.2036",
        "x": "2.6758"
    },
    "8": {
        "uid": 8,
        "n": "Thuban",
        "puid": 6,
        "v": "0",
        "y": "0.7816",
        "x": "0.5119"
    },
    "9": {
        "uid": 9,
        "n": "Mimosa",
        "puid": 6,
        "v": "0",
        "y": "0.9648",
        "x": "0.6509"
    },
    "10": {
        "uid": 10,
        "n": "Corvid",
        "puid": 6,
        "v": "0",
        "y": "0.5885",
        "x": "0.4258"
    },
    "11": {
        "uid": 11,
        "n": "Alrischa",
        "puid": 0,
        "v": "0",
        "y": "0.7680",
        "x": "0.0509"
    },
    "12": {
        "uid": 12,
        "n": "Arc",
        "puid": 0,
        "v": "0",
        "y": "0.5353",
        "x": "0.1160"
    },
    "15": {
        "uid": 15,
        "n": "Alderamin",
        "puid": 4,
        "v": "0",
        "y": "0.2176",
        "x": "0.1758"
    },
    "16": {
        "c": 0.5,
        "e": 5,
        "uid": 16,
        "i": 6,
        "s": 2,
        "n": "Boop",
        "puid": 3,
        "r": 65,
        "ga": 0,
        "v": "1",
        "y": "2.2036",
        "x": "2.6758",
        "nr": 50,
        "st": 119
    }
}


SAMPLE_FLEET = {
    "ouid": 42,
    "uid": 19,
    "l": 0,
    "o": [],
    "n": "Electra I",
    "puid": 3,
    "w": 0,
    "y": "1.35375519",
    "x": "2.88923031",
    "st": 33,
    "lx": "2.90623808",
    "ly": "1.36603401"
}

SAMPLE_FLEET_2 = {
    "ouid": False,
    "uid": 14,
    "l": 0,
    "o": [],
    "n": "Bob I",
    "puid": 1,
    "w": 0,
    "y": "3.35275519",
    "x": "1.88923031",
    "st": 60,
    "lx": "3.90623808",
    "ly": "2.36603401"
}

SAMPLE_FLEET_3 = {
    "ouid": 32,
    "uid": 10,
    "l": 0,
    "o": [],
    "n": "Jeremy II",
    "puid": 4,
    "w": 0,
    "y": "3.35275519",
    "x": "1.88923031",
    "st": 120,
    "lx": "3.90623808",
    "ly": "2.36603401"
}