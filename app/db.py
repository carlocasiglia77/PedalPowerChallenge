# db.py
from influxdb import InfluxDBClient


class DBWriter:
    def __init__(self, config):
        self.client = InfluxDBClient(host=config['host'], port=config['port'])
        self.db_name = config['db_name']
        self.client.switch_database(self.db_name)
        self.measurement = config['measurement']

    def write_energy(self, player_id, energy_wh):
        point = {
            "measurement": self.measurement,
            "tags": {"player": player_id},
            "fields": {"energy": energy_wh}
        }
        self.client.write_points([point])