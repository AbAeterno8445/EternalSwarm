from millify import millify_num


class PlayerData(object):
    def __init__(self, name):
        self.name = name

        self.carb_crystals = 0
        self.ccps = 0  # Carbonic crystals per second
        self.owned_buildings = ["Slime Spawner"]

    def get_carbcrystals_str(self):
        return millify_num(self.carb_crystals)

    def get_ccps_str(self):
        return millify_num(self.ccps)

    def ccps_tick(self, tick_len):
        self.carb_crystals += self.ccps / tick_len