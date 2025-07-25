from influxdb_client import InfluxDBClient, Point

class DBWriter:
    def __init__(self, config):
        self.client = InfluxDBClient(
            url=config["url"],
            token=config["token"],
            org=config["org"]
        )
        self.bucket = config["bucket"]
        self.write_api = self.client.write_api()

    def write_state(self, current_timer, p1, p2, p3, p4, tot):
        point = Point("game_status") \
            .field("current_timer", current_timer) \
            .field("player1_tot_wh", p1) \
            .field("player2_tot_wh", p2) \
            .field("player3_tot_wh", p3) \
            .field("player4_tot_wh", p4) \
            .field("tot_wh", tot)

        self.write_api.write(bucket=self.bucket, record=point)
