import time
from ina260 import INA260Sensor
from player import Player
from game_controller import GameController
from db import DBWriter

from utils import setup_logger
import yaml


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():

    config = load_config()
    setup_logger(config.get("logging", {}).get("level", "INFO"))

    # TODO Capire se tutti e quattro gli INA sono sempre collegati alla Raspberry
    sensors = [INA260Sensor(addr) for addr in config['sensors']['addresses']]
    players = [Player(sensor, i) for i, sensor in enumerate(sensors)]
    db = DBWriter(config['database'])
    controller = GameController(players, db, config)

    while True:
        controller.update()
        time.sleep(1)


if __name__ == "__main__":
    main()
