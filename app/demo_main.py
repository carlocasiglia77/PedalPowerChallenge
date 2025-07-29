import time
import random

from app.db import DBWriter
from app.main import load_config
from app.utils import setup_logger
from player import Player
from game_controller import GameController


class FakeSensor:
    def __init__(self):
        self.voltage = 0
        self.power = 0

    def read_voltage(self):
        # Randomly simulate pedaling
        if random.random() < 0.2:
            self.voltage = random.uniform(0.5, 2.5)
        else:
            self.voltage = 0
        return self.voltage

    def read_power(self):
        # Only return power if voltage is non-zero
        return self.voltage * random.uniform(0.5, 3)


class FakeDBWriter:
    def write_game_state(self, remaining, energies, powers, total_energy):
        print(f"[DB] Time left: {remaining}s | Energies: {energies} | Powers: {powers} | Total: {total_energy:.2f} Wh")


def demo_main():
    config = load_config()
    setup_logger(config.get("logging", {}).get("level", "INFO"))
    db = DBWriter(config['database'])
    sensors = [FakeSensor() for _ in range(4)]
    players = [Player(sensor, i) for i, sensor in enumerate(sensors)]

    game = GameController(players, db, config)
    game.run()


if __name__ == "__main__":
    demo_main()
