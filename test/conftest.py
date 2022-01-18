import pytest
from unittest import mock
import os
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
def status(fleet_one, fleet_two, fleet_three):
    np: NeptunesPrideStatus = NeptunesPrideStatus(ROOT, PARAMS, "4", "+61448715179")
    np.fleets = [fleet_one, fleet_two, fleet_three]

    yield np


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