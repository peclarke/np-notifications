from typing import List
from data.Fleet import Fleet
from utils.firebase import does_fleet_exist

def filter_unnotified_fleets(enemies: List[Fleet]):
    return list(filter(lambda x: not does_fleet_exist(x), enemies))

def filter_not_moving_fleets(enemies: List[Fleet]):
    return list(filter(lambda x: not x.is_moving(), enemies))