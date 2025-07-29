import time
import random

from app.db import DBWriter
from app.main import load_config
from app.utils import setup_logger
from app.player import Player
from app.game_controller import GameController


class FakeSensor:
    def __init__(self):
        self.voltage = 0
        self.power = 0

    def read_voltage(self):
        # Simulate high-voltage pedaling condition with 80% probability
        if random.random() < 0.8:
            self.voltage = random.uniform(10.0, 20.0)  # Between 10V and 20V
        else:
            self.voltage = 0
        return self.voltage

    def read_power(self):
        # Simulate realistic high power when voltage is present
        if self.voltage > 0:
            self.power = random.uniform(20.0, 40.0)  # Between 20W and 40W
        else:
            self.power = 0
        return self.power



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
