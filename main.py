from typing import TYPE_CHECKING, List
import requests
import os
from data.Fleet import Fleet
from flask import Flask, render_template
import __init__
from check import begin_check, debug, get_all_enemy_fleets

USER_ID = 5 # this is my player ID
ROOT = "https://np.ironhelmet.com/api"
PARAMS = {
            "game_number": os.getenv("CURRENT_GAME_ID"),
            "code": os.getenv("API_KEY"),
            "api_version": os.getenv("API_VERSION")
        }

class NeptunesPrideStatus():
    def __init__(self, root, params, user_id):
        self.res = requests.post(root, params).json()['scanning_data']
        self.owner = user_id

        self.fleets = []
        for fleet in self.res['fleets'].values():
            self.fleets.append(Fleet(fleet))

        self.players = []
        # create player obj

        self.stars = []
        # create stars obj

    def get_enemy_fleets(self):
        enemies: List[Fleet] = []
        for fleet in self.fleets:
            if not fleet.is_id_owner_of(self.owner):
                enemies.append(fleet)
        return enemies

    def get_moving_enemies(self):
        enemies: List[Fleet] = self.get_enemy_fleets()
        for e in enemies:
            if not e.is_moving():
                enemies.remove(e)
        return enemies

    def get_response(self):
        return self.res

    def get_game_details(self):
        details = self.res
        del details['fleets']
        del details['stars']
        del details['players']
        return details

    def get_stars(self):
        pass

    def get_players(self):
        pass

    def get_fleets(self):
        return self.fleets

def make_request():
    return NeptunesPrideStatus(ROOT, PARAMS, USER_ID)

app = Flask(__name__)

@app.route('/')
def root():
    np = make_request()
    return render_template('index.html', enemyfleets=len(np.get_enemy_fleets()), movingfleets=len(np.get_moving_enemies()))

@app.route('/check')
def check():
    np = make_request()
    begin_check(np)
    return '200 OK'

@app.route('/daily-overview')
def daily():
    np = make_request()
    get_all_enemy_fleets(np)
    return '200 OK'

@app.route('/debug')
def debug_me():
    debug()
    return '200 OK'

# only used for local machine
'''
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
'''