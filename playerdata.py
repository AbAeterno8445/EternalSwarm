from millify import millify_num


class PlayerData(object):
    def __init__(self, name):
        self.name = name

        self.carb_crystals = 0
        self.ccps = 0  # Carbonic crystals per second

        self.start_energy = 100
        self.start_energyps = 1
        self.owned_buildings = ["Slime Spawner", "Azure Beetle Spawner", "Turtle Spawner"]

        self.start_health = 50

    def get_carbcrystals_str(self):
        return millify_num(self.carb_crystals)

    def get_ccps_str(self):
        return millify_num(self.ccps)

    def ccps_tick(self, tick_len):
        self.carb_crystals += self.ccps / tick_len

    def json_save(self):
        return self.__dict__

    def json_load(self, json_data):
        for data in json_data:
            if hasattr(self, data):
                setattr(self, data, json_data[data])