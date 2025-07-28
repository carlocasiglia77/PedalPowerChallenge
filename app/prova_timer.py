import time


def main():

    game_start_time = time.time()
    game_duration = 60
    refresh_rate = 0.5

    while True:
        now = time.time()
        # TODO trasformare questa roba inutile in una gestione del timer decente
        elapsed = now - game_start_time
        remaining = max(0, game_duration - int(elapsed))
        if elapsed >= game_duration:
            print("Game ended")
        else:
            print(f"Elapsed time: {elapsed}")
            print(f"Remainin: {remaining}")

        time.sleep(refresh_rate)


if __name__ == "__main__":
    main()
