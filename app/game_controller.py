import time
import logging


class GameController:

    """
    GameController viene inizializzato con:
        - Una lista di giocatori, che contengono il proxy del loro INA260 e l'energia accumulata
          Hanno un metodo update(delta_time_sec) che aggiorna la loro energia accumulata nell'ultimo delta_time
          TODO assicurarsi di calcolare il delta_time dinamicamente
        - Ha un DB Writer che scrive su Influx DB i dati di gioco
          - timer attuale
          - energie accumulate dai vari giocatori
          - energie istantanee dei vari giocatori
          - energia totale accumulata finora

    Flusso di gioco:
        - Reset -> Energia totale a zero, energie accumulate dai giocatori a zero, timer a zero
        - Ciclo leggendo gli INA di tutti i giocatori, finché uno degli INA non restituisce un voltaggio sopra soglia
          per un certo numero di secondi (ENV voltage_activation_threshold, time_activation_threshold)
        - Quando ciò avviene parte il gioco e il loop, alla frequenza impostata, aggiorna il timer,
          l'energia accumulata da ogni giocatore, e l'energia totale
        - Se a non arriva tensione da nessun giocatore per un certo numero di secondi termino il gioco
        - Se il timer scade termino il gioco
        - Quando il gioco termina, lascio i valori in memoria per un certo tempo di cooldown
        - Reset
        TODO Modalità POWER oltre a TIME
    """

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

        logging.info("GameController initialized")

    # TODO Funzione che calcola il timer corrente
    # TODO Funzione che scrive sul DB in un colpo solo tutti i valori: timer corrente, en accumulata, ecc

    def _reset(self):
        self.active = False
        self.activation_start_time = None
        self.game_start_time = False
        for p in self.players:
            p.energy_accum = 0

    def _start_game(self):
        logging.info("Game started!")
        self.active = True
        self.game_start_time = time.time()

    def _end_game(self):
        logging.info("Game ended!")
        time.sleep(self.cooldown)
        self._reset()
        # self.db_writer.write_energy(player.id, player.energy_accum)

    def _write_state_to_db(self, elapsed, delta_time_sec):
        energies = []
        powers = []
        for p in self.players:
            energies.append(p.energy_accum)
            powers.append(p.sensor.read_power())

        total_energy = sum(energies)

        self.db_writer.write_game_state(
            elapsed,
            energies,
            powers,
            total_energy
        )

    def run(self):

        while True:

            now = time.time()

            # Sezione di gioco inattivo, verifichiamo se il gioco deve iniziare
            if not self.active:
                if len([p for p in self.players if p.sensor.read_voltage() >= self.voltage_activation_threshold]) > 0:
                    if self.activation_start_time is None:
                        self.activation_start_time = now
                        logging.info("Activation condition detected, timer started")
                    elif (now - self.activation_start_time) >= self.time_activation_threshold:
                        self._start_game()
                else:
                    # Se stavamo aspettando di vedere se il gioco doveva iniziare ma ha smesso di arrivare corrente
                    # ricominciamo da zero. Non dovrebbe essere necessario essere più precise, ma teniamo d'occhio
                    self.activation_start_time = None  # reset if condition not met

            # Loop di gioco
            else:
                # TODO trasformare questa roba inutile in una gestione del timer decente
                elapsed = now - self.game_start_time
                if elapsed >= self.game_duration:
                    self._end_game()
                else:
                    for player in self.players:
                        player.update(delta_time_sec=self.refresh_rate) # TODO delta_time DINAMICO

            time.sleep(self.refresh_rate)
