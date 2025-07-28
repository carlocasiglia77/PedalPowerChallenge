import time
import random
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
    # Fake config
    config = {
        'game': {
            'duration': 10,
            'voltage_activation_threshold': 0.5,
            'time_activation_threshold': 2,
            'cooldown': 3,
            'refresh_rate': 1,
            'no_power_timeout': 3,
        }
    }

    # Fake players
    sensors = [FakeSensor() for _ in range(2)]
    players = [Player(sensor, i) for i, sensor in enumerate(sensors)]
    db_writer = FakeDBWriter()

    game = GameController(players, db_writer, config)
    game.run()


if __name__ == "__main__":
    demo_main()
