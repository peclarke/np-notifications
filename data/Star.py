from utils.general_utils import pid_to_name

class Star():
    def __init__(self, json):   
        self.uid = json['uid']
        self.name = json['n']
        self.owner = json['puid']
        self.visible = json['v'] == '1'

        self.x = json['x']
        self.y = json['y']

        if self.visible:
            self.economy = json['e']
            self.industry = json['i']
            self.science = json['s']

            self.ships = json['st']
            self.natural_resources = json['nr']
            self.net_resources = json['r']

    def is_visible(self):
        return self.visible

    def get_owner_name(self):
        return pid_to_name(self.owner)

    def get_points(self):
        if self.visible:
            return {
                'econ': self.economy,
                'indu': self.industry,
                'scie': self.science
            }
        return {}

    def get_num_ships(self):
        if self.visible:
            return self.ships
        return None

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "owner": self.get_owner_name(),
            "points": self.get_points(),
            "x": self.x,
            "y": self.y
        }