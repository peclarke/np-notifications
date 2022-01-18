from typing import TYPE_CHECKING, List
import requests
import os
from data.Fleet import Fleet
from flask import Flask, render_template
import json
from utils.firebase import get_all_alliances
import __init__
from check import begin_check, setup_daily_digest

ROOT = "https://np.ironhelmet.com/api"
PARAMS = {
            "game_number": os.getenv("CURRENT_GAME_ID"),
            "code": os.getenv("API_KEY"),
            "api_version": os.getenv("API_VERSION")
        }

class NeptunesPrideStatus():
    def __init__(self, root, params, user_id, phone):
        self.res = requests.post(root, params).json()['scanning_data']
        self.owner = user_id
        self.phone = phone

        self.fleets = []
        for fleet in self.res['fleets'].values():
            self.fleets.append(Fleet(fleet))

        self.players = []
        # create player obj

        self.stars = []
        # create stars obj

    def get_my_fleets(self):
        return list(filter(lambda x: x.is_id_owner_of(self.owner), self.fleets))
    
    def get_enemy_fleets(self):
        enemies: List[Fleet] = []
        for fleet in self.fleets:
            if fleet.puid != int(self.owner):
                enemies.append(fleet)
        return enemies

    def get_moving_enemies(self):
        enemies: List[Fleet] = self.get_enemy_fleets()
        moving: List[Fleet] = list(filter(lambda x: x.is_moving(), enemies))
        return moving

    def get_response(self):
        return self.res

    def get_game_details(self):
        details = self.res
        del details['fleets']
        del details['stars']
        del details['players']
        return details

    def get_owner_phone(self):
        return self.phone

    def get_stars(self):
        pass

    def get_players(self):
        pass

    def get_fleets(self):
        return self.fleets

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
    return render_template('index.html', allies=len(get_all_alliances()), enemyfleets=len(np.get_enemy_fleets()), movingfleets=len(np.get_moving_enemies()))

@app.route('/check')
def check():
    np: List[NeptunesPrideStatus] = make_request()
    for req in np:
        begin_check(req)
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
        my_fleets: List[Fleet] = req.get_my_fleets() # broken
        for f in my_fleets:
            all_fleets.append(f.to_dict())

    # get all enemy info
    enemies_json: List = []
    for e in get_alliance_enemies(): # also broken
        enemies_json.append(e.to_dict())

    return render_template('network.html', ally_fleets=all_fleets, enemies=enemies_json, debug="debugtimebbaby")

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
