import time
import logging

class GameController:

    def __init__(self, players, db_writer, config):
        self.players = players
        self.db_writer = db_writer
        self.config = config

        self.game_duration = config['game']['duration']
        self.voltage_activation_threshold = config['game']['voltage_activation_threshold']
        self.time_activation_threshold = config['game']['time_activation_threshold']
        self.cooldown = config['game']['cooldown']
        self.refresh_rate = config['game']['refresh_rate']

        self.active = False
        self.activation_start_time = None
        self.game_start_time = None

        self.elapsed = None
        self.remaining = None

        self.no_power_timer = 0

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
        logging.info("GameController initialized")

    def _reset(self):
        logging.debug("Resetting game state.")
        self.active = False
        self.activation_start_time = None
        self.game_start_time = None
        self.elapsed = 0
        self.remaining = 0
        for p in self.players:
            p.energy_accum = 0

    def _start_game(self):
        logging.info("🚀 Game started!")
        self.active = True
        self.game_start_time = time.time()
        self.remaining = self.game_duration

    def _end_game(self):
        logging.info("🛑 Game ended!")
        time.sleep(self.cooldown)
        self._reset()

    def _write_state_to_db(self):
        energies = []
        powers = []
        voltages = []

        for i, p in enumerate(self.players):
            power = p.sensor.read_power()
            voltage = p.sensor.read_voltage()
            energy = p.energy_accum
            powers.append(power)
            voltages.append(voltage)
            energies.append(energy)

            logging.debug(f"[Player {i+1}] Voltage: {voltage:.2f} V | Power: {power:.2f} W | Energy: {energy:.4f} Wh")

        total_energy = sum(energies)

        remaining = self.remaining if self.remaining is not None else 0

        logging.debug(f"⏱ Remaining Time: {self.remaining} sec | 🔋 Total Energy: {total_energy:.4f} Wh")

        self.db_writer.write_game_state(
            self.remaining,
            powers[0], powers[1], powers[2], powers[3],
            energies[0], energies[1], energies[2], energies[3],
            total_energy
        )

        logging.debug("✅ Game state written to DB.")

    def run(self):
        logging.info("Game loop started.")
        while True:
            now = time.time()

            # Activation phase
            if not self.active:
                logging.debug("Game is inactive. Checking for activation condition...")
                active_players = [p for p in self.players if p.sensor.read_voltage() >= self.voltage_activation_threshold]

                if active_players:
                    logging.debug(f"{len(active_players)} player(s) above voltage threshold.")
                    if self.activation_start_time is None:
                        self.activation_start_time = now
                        logging.info("⚡ Activation condition detected, waiting for sustained signal...")
                    elif (now - self.activation_start_time) >= self.time_activation_threshold:
                        self._start_game()
                else:
                    if self.activation_start_time is not None:
                        logging.info("🔌 Activation signal lost. Resetting activation timer.")
                    self.activation_start_time = None

            # Game in progress
            else:
                self.elapsed = now - self.game_start_time
                self.remaining = max(0, self.game_duration - int(self.elapsed))

                logging.debug(f"🕒 Game running: {int(self.elapsed)}s elapsed, {self.remaining}s remaining.")

                if self.elapsed >= self.game_duration:
                    logging.info("⏲️ Game duration complete.")
                    self._end_game()
                else:
                    for i, player in enumerate(self.players):
                        player.update(delta_time_sec=self.refresh_rate)
                        logging.debug(f"Updated Player {i+1} energy accumulation.")

            # Check for power dropout
            if all(p.sensor.read_voltage() < self.voltage_activation_threshold for p in self.players):
                self.no_power_timer += self.refresh_rate
                logging.debug(f"No power detected. no_power_timer = {self.no_power_timer:.2f}s")
                if self.no_power_timer >= self.config['game']['no_power_timeout']:
                    logging.warning("⚠️ No power for too long. Ending game.")
                    self._end_game()
            else:
                self.no_power_timer = 0

            self._write_state_to_db()
            time.sleep(self.refresh_rate)
