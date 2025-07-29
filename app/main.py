import time
import random
from pathlib import Path

from app.ina260 import INA260Sensor
from app.player import Player
from app.game_controller import GameController
from app.db import DBWriter

from app.utils import setup_logger
import yaml


def load_config():
    config_path = Path(__file__).resolve().parent.parent / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():

    # TODO Capire se tutti e quattro gli INA sono sempre collegati alla Raspberry

    config = load_config()
    setup_logger(config.get("logging", {}).get("level", "INFO"))

    db = DBWriter(config['database'])
    sensors = [INA260Sensor(addr) for addr in config['sensors']['addresses']]
    players = [Player(sensor, i) for i, sensor in enumerate(sensors)]
    controller = GameController(players, db, config)

    controller.run()


def main_demo():
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

        db.write_game_state(current_timer, player1_wh, player2_wh, player3_wh, player4_wh, total_wh)

        time.sleep(refresh_rate)


if __name__ == "__main__":
    main()
