from typing import List
import requests

from data.Fleet import Fleet

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