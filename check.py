'''
Steps:
1) Make the request to the Neptune's Pride API and pass it through to our parsing script
2) Get all moving enemy fleets in proximity (in testing, non-moving works just fine)
3) Send the data to the notifications.py message formatter
4) Message is then sent to phone with information
'''

from typing import List
from __init__ import db
from data.Fleet import Fleet
from utils.firebase import find_fleet, set_fleet, get_all_fleets, remove_fleet_uid
from consts import StatusCode
from notifications import format_message, send_message

def begin_check(np):
    scan_for_ships(np)

def scan_for_ships(np):
    enemies: List[Fleet] = np.get_moving_enemies()

    # remove any existing fleets (that we notified about already)
    for e in enemies:
        if find_fleet(e):
            enemies.remove(e)
        
    if len(enemies) > 0:
        format_message(StatusCode.ENEMY, enemies, np)
        # add each new fleet into the database
        for e in enemies:
            set_fleet(e)

# do this every 24 hrs
def reset_fleet_database():
    fleets = get_all_fleets()
    for f in fleets:
        if len(f.id) < 15:
            info = f.to_dict()
            remove_fleet_uid(int(info['uid']))

def setup_daily_digest(np):
    enemies: List[Fleet] = np.get_enemy_fleets()
    moving: List[Fleet] = np.get_moving_enemies()
    format_message(StatusCode.DAILY, [enemies, moving], np)

'''
LOOK INTO THIS AT ANOTHER POINT...
A missing ship is one that's in the database but not on the radar.
I'm almost tempted to make a new table to put the date of when the ship went missing
'''
'''def scan_for_missing_ships(np: NeptunesPrideStatus):
    enemies: List[Fleet] = np.get_enemy_fleets()
    fleets = get_all_fleets()
    for f in fleets:
        info = f.to_dict()
        for e in enemies:
            # if a match is made, remove it. 
            if f['uid'] == e.uid:
                enemies.remove(e)
    # delete the remaining enemies
    for e in enemies:
        remove_fleet_uid(e.uid)
'''
def scan_for_threshold(np):
    pass

def debug(np):
    send_message("Debug baby!", np)