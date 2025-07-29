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

    def write_game_state(self,
                         remaining_secs,
                         p1_w,
                         p2_w,
                         p3_w,
                         p4_w,
                         p1_tot_wh,
                         p2_tot_wh,
                         p3_tot_wh,
                         p4_tot_wh,
                         tot_wh):
        point = Point("game_status") \
            .field("remaining_secs", float(remaining_secs)) \
            .field("p1_w", float(p1_w)) \
            .field("p2_w", float(p2_w)) \
            .field("p3_w", float(p3_w)) \
            .field("p4_w", float(p4_w)) \
            .field("p1_tot_wh", float(p1_tot_wh)) \
            .field("p2_tot_wh", float(p2_tot_wh)) \
            .field("p3_tot_wh", float(p3_tot_wh)) \
            .field("p4_tot_wh", float(p4_tot_wh)) \
            .field("tot_wh", float(tot_wh))

        self.write_api.write(bucket=self.bucket, record=point)
