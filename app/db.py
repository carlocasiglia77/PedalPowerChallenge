# db.py
from influxdb import InfluxDBClient


class DBWriter:
    def __init__(self, config):
        self.client = InfluxDBClient(
            host=config['host'],
            port=config['port'],
            username=config['username'],
            password=config['password'])
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

    def write_state(self,
                    current_timer,
                    player1_tot_wh,
                    player2_tot_wh,
                    player3_tot_wh,
                    player4_tot_wh,
                    tot_wh):
        point = {
            "measurement": "game_status",
            "fields": {
                "current_timer": current_timer,
                "player1_tot_wh": player1_tot_wh,
                "player2_tot_wh": player2_tot_wh,
                "player3_tot_wh": player3_tot_wh,
                "player4_tot_wh": player4_tot_wh,
                "tot_wh": tot_wh
            }
        }
        self.client.write_points([point])
