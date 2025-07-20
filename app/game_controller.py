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

        self.active = False
        self.activation_start_time = None
        self.game_start_time = None

        logging.info("GameController initialized")

    def _check_activation_condition(self):
        """Verifica se almeno una bici ha superato la soglia di tensione."""
        active_bikes = [
            p for p in self.players if p.sensor.read_voltage() >= self.voltage_activation_threshold
        ]
        return len(active_bikes) > 0

    def _reset_players(self):
        for p in self.players:
            p.energy_accum = 0

    def _start_game(self):
        logging.info("Game started!")
        self.active = True
        self.game_start_time = time.time()
        self._reset_players()

    def _end_game(self):
        logging.info("Game ended!")
        self.active = False
        for player in self.players:
            self.db_writer.write_energy(player.id, player.energy_accum)
            logging.info(f"Player {player.id}: {player.energy_accum:.3f} Wh")

        self.activation_start_time = None
        self.game_start_time = None

    def update(self):
        now = time.time()

        if not self.active:
            if self._check_activation_condition():
                if self.activation_start_time is None:
                    self.activation_start_time = now
                    logging.info("Activation condition detected, timer started")
                elif (now - self.activation_start_time) >= self.time_activation_threshold:
                    self._start_game()
            else:
                self.activation_start_time = None  # reset if condition not met
        else:
            elapsed = now - self.game_start_time
            if elapsed >= self.game_duration:
                self._end_game()
            else:
                for player in self.players:
                    player.update(delta_time_sec=1)
