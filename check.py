'''
Steps:
1) Make the request to the Neptune's Pride API and pass it through to our parsing script
2) Get all moving enemy fleets in proximity (in testing, non-moving works just fine)
3) Send the data to the notifications.py message formatter
4) Message is then sent to phone with information
'''

from typing import List
from data.Fleet import Fleet
from utils.filter_utils import filter_not_moving_fleets, filter_unnotified_fleets
from utils.firebase import does_fleet_exist, get_all_old_fleets, set_fleet, get_all_fleets, remove_fleet_uid, set_old_fleet
from consts import StatusCode
from notifications import format_message, send_message

def begin_check(np):
    set_notify_fleet_at_star(np)
    scan_for_ships(np)

def scan_for_ships(np):
    enemies: List[Fleet] = np.get_moving_enemies()
    unnotified = filter_unnotified_fleets(enemies)

    # format msg, and add fleets to db
    if len(unnotified) > 0:
        format_message(StatusCode.ENEMY, unnotified, np)
        for e in enemies:
            set_fleet(e, int(np.owner))

'''
1) If a fleet exists in the database (fleets table, that is) AND
2) Does not exist in our scanning range, THEN
- Move it to the old fleets table
'''
def update_missing_fleets(alliance_enemies: List[Fleet]):
    # get all fleets from the database and all enemies in scanning range
    all_fleets = get_all_fleets()
    enemies: List[int] = [k.uid for k in alliance_enemies]
    # check if the fleet exists in scanning range, if not boot it
    for f in all_fleets:
        g = f.to_dict()
        if g['uid'] not in enemies:
            fleet_info = remove_fleet_uid(g['uid'])
            set_old_fleet(g['uid'], fleet_info)

'''
1) If a fleet has been recorded at one point (i.e. in the old_fleets table) AND
2) It is NOT moving at a star (i.e. within scanning range not moving) THEN
- On occasion, re-add it to the old-fleets database to update it's status
=== We'll use this data later on when we create time-series analytics of the ships
'''
def update_old_fleet_status(alliance_enemies: List[Fleet]):
    oldies = get_all_old_fleets()
    not_moving: List[Fleet] = [k.uid for k in filter_not_moving_fleets(alliance_enemies)]

    for f in oldies:
        g = f.to_dict()
        if g['uid'] in not_moving:
            set_old_fleet(g['uid'], g)

'''
1) If a fleet has been notified about already AND
2) It has docked a star THEN
- It has stopped moving, therefore resetting its notification state.
- When it begins moving again, we will notify
'''
def set_notify_fleet_at_star(np):
    enemies: List[Fleet] = np.get_enemy_fleets()
    not_moving = filter_not_moving_fleets(enemies)

    # remove the already notified ones
    for f in not_moving:
        if does_fleet_exist(f):
            removed: Fleet = remove_fleet_uid(int(f.uid))
            set_old_fleet(int(f.uid), removed)

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

def scan_for_threshold(np):
    pass

def debug(np):
    send_message("Debug baby!", np)