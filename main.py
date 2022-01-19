from typing import TYPE_CHECKING, List
import requests
import os
from data.Fleet import Fleet
from flask import Flask, render_template
import json
from data.Status import NeptunesPrideStatus
from utils.filter_utils import filter_moving_fleets
from utils.firebase import get_all_alliances
import __init__
from check import begin_check, setup_daily_digest, update_missing_fleets, update_old_fleet_status

ROOT = "https://np.ironhelmet.com/api"
PARAMS = {
            "game_number": os.getenv("CURRENT_GAME_ID"),
            "code": os.getenv("API_KEY"),
            "api_version": os.getenv("API_VERSION")
        }

def make_request():
    allies = get_all_alliances()
    reqs: List[NeptunesPrideStatus] = []
    for a in allies:
        uid = a['uid']
        api_key: str = a['api_key']
        phone = a['phone']
        reqs.append(NeptunesPrideStatus(ROOT, {"game_number": os.getenv("CURRENT_GAME_ID"),
                                               "code": api_key,
                                               "api_version": os.getenv("API_VERSION")}, str(uid), phone))
    reqs.append(NeptunesPrideStatus(ROOT, PARAMS, os.getenv("USER_ID"), os.getenv("NOTIF_PH")))
    return reqs

def make_super_owner_request():
    np: NeptunesPrideStatus = NeptunesPrideStatus(ROOT, PARAMS, os.getenv("USER_ID"), os.getenv("NOTIF_PH"))
    return np

def get_alliance_enemies():
    net_enemies: List[Fleet] = []
    # get user ids of everyone in the alliance
    allies = get_all_alliances()
    ally_ids: List[int] = [ally['uid'] for ally in allies]
    ally_ids.append(int(os.getenv("USER_ID")))
    # find fleets whose ids don't belong in that list
    reqs: List[NeptunesPrideStatus] = make_request()
    for req in reqs:
        fleets: List[Fleet] = req.get_enemy_fleets()
        for f in fleets:
            if f.puid not in ally_ids:
                net_enemies.append(f)
    return net_enemies

app = Flask(__name__)

@app.route('/')
def root():
    np: NeptunesPrideStatus = make_super_owner_request()
    enemies: List[Fleet] = get_alliance_enemies()
    moving: List[Fleet] = filter_moving_fleets(enemies)
    return render_template('index.html', allies=len(get_all_alliances()) + 1, enemyfleets=len(enemies), movingfleets=len(moving))

@app.route('/check')
def check():
    np: List[NeptunesPrideStatus] = make_request()
    for req in np:
        begin_check(req)
    return '200 OK'

@app.route('/ship-analytics')
def shipanal():
    all_enem: List[Fleet] = get_alliance_enemies()
    update_missing_fleets(all_enem)
    update_old_fleet_status(all_enem)
    return '200 OK'

@app.route('/daily-overview')
def daily():
    np: List[NeptunesPrideStatus] = make_request()
    for req in np:
        setup_daily_digest(req)
    return '200 OK'

@app.route('/alliance-network')
def network():
    # combine all ally fleet information
    np: List[NeptunesPrideStatus] = make_request()
    all_fleets: List[Fleet] = []
    for req in np:
        my_fleets: List[Fleet] = req.get_my_fleets()
        for f in my_fleets:
            all_fleets.append(f.to_dict())

    # get all enemy info
    enemies_json: List = []
    for e in get_alliance_enemies():
        enemies_json.append(e.to_dict())

    return render_template('network.html',
                            ally_fleets=all_fleets,
                            enemies=enemies_json,
                            enemy_names=[[k['name'], k['ouid'] == False] for k in enemies_json],
                            ally_data=[[i['name'], i['ouid'] == False] for i in all_fleets])

@app.route('/debug')
def debug_me():
    np = make_super_owner_request()
    #nps = make_request()
    #asd = nps[0].get_moving_enemies()
    #begin_check(nps[0])
    #debug(np)
    return '200 OK'

# only used for local machine

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
