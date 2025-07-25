import time
import random

from ina260 import INA260Sensor
from player import Player
from game_controller import GameController
from db import DBWriter

from utils import setup_logger
import yaml


def load_config():
    with open("../config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()
    setup_logger(config.get("logging", {}).get("level", "INFO"))
    db = DBWriter(config['database'])

    # Game settings
    start_time = time.time()
    duration = 60  # seconds
    refresh_rate = 0.5  # seconds

    while True:
        elapsed = time.time() - start_time
        current_timer = max(0.0, duration - elapsed)

        # Stop loop when timer hits 0
        if current_timer <= 0:
            break

        # Generate random Wh per player (example: 0.0 to 0.2 Wh per refresh)
        player1_wh = random.uniform(0.0, 0.2)
        player2_wh = random.uniform(0.0, 0.2)
        player3_wh = random.uniform(0.0, 0.2)
        player4_wh = random.uniform(0.0, 0.2)

        player_whs = {
            "player1": player1_wh,
            "player2": player2_wh,
            "player3": player3_wh,
            "player4": player4_wh,
        }

        total_wh = sum(player_whs.values())

        db.write_state(current_timer, player_whs, total_wh)

        time.sleep(refresh_rate)


"""
    

    # TODO Capire se tutti e quattro gli INA sono sempre collegati alla Raspberry
    sensors = [INA260Sensor(addr) for addr in config['sensors']['addresses']]
    players = [Player(sensor, i) for i, sensor in enumerate(sensors)]
    db = DBWriter(config['database'])
    controller = GameController(players, db, config)

    controller.run()
"""


if __name__ == "__main__":
    main()
