from typing import TYPE_CHECKING, Any, List
import requests
import os
from data.Fleet import Fleet
from flask import Flask, render_template
import json
from data.Star import Star
from data.Status import NeptunesPrideStatus
from utils.filter_utils import filter_moving_fleets
from utils.firebase import add_star, get_all_alliances, get_all_stars
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

def get_coords_of_obj(obj: Any):
    x_coords: List[float] = []
    y_coords: List[float] = []
    for el in obj:
        x_coords.append(float(el['x']))
        y_coords.append(float(el['y']))

    return [x_coords, y_coords]

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

'''
If a fleet is not moving at a star or not within scanning BUT in our fleets table,
moves it over to the old_fleets table.
'''
@app.route('/ship-analytics')
def shipanal():
    all_enem: List[Fleet] = get_alliance_enemies()
    update_missing_fleets(all_enem)
    update_old_fleet_status(all_enem)
    return '200 OK'

'''
Every TWENTY-FOUR (24) hours, run an analysis on all 
the stars in range and add the updated version to the database
'''
@app.route('/star-analytics')
def staranal():
    np: List[NeptunesPrideStatus] = make_request()
    added_uids: List[int] = []
    for req in np:
        stars: List[Star] = req.get_stars()
        for star in stars:
            if star.is_visible() and star.uid not in added_uids:
                added_uids.append(star.uid)
                add_star(star)
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
    #ally_data: List[List[Any]] = [[], []]
    ally_data: List[str] = []
    for req in np:
        my_fleets: List[Fleet] = req.get_my_fleets()
        for f in my_fleets:
            g = f.to_dict()

            ally_data.append(g['name'])
            #ally_data[0].append(g['name'])
            #ally_data[1].append(g['ouid'] == False)
            all_fleets.append(g)

    # get all enemy info
    enemies_json: List = []
    enemy_data: List[List[Any]] = [[],[]]
    for e in get_alliance_enemies():
        res = e.to_dict()
        enemy_data[0].append(res['name'])
        enemy_data[1].append(res['ouid'] == False)
        enemies_json.append(res)

    #star_data = get_all_stars() # atm gets all stars, not just the most recent ones.
    star_data = []
    star_names = []
    for k in np[0].stars:
        star_data.append(k.to_dict())
        star_names.append(k.name)

    enemy_x, enemy_y = get_coords_of_obj(enemies_json)
    ally_x, ally_y = get_coords_of_obj(all_fleets)
    star_xs, star_ys = get_coords_of_obj(star_data)

    return render_template('network.html',
                            stars=star_data,
                            star_xs=star_xs,
                            star_ys=star_ys,
                            star_names=star_names,
                            enemy_xs=enemy_x,
                            enemy_ys=enemy_y,
                            enemies=enemies_json,
                            enemy_names=enemy_data,
                            ally_xs=ally_x,
                            ally_ys=ally_y,
                            ally_data=ally_data,
                            ally_fleets=all_fleets)

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
