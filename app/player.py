# game/player.py
class Player:
    def __init__(self, sensor, id):
        self.sensor = sensor
        self.id = id
        self.energy_accum = 0  # in Wh

    def update(self, delta_time_sec):
        power_watts = self.sensor.read_power()
        self.energy_accum += (power_watts * delta_time_sec) / 3600.0