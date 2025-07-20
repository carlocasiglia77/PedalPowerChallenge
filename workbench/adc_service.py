import time
import board
import busio
import adafruit_ina260

i2c = busio.I2C(board.SCL, board.SDA)

addresses = [0x40, 0x41, 0x44, 0x45]
bikes = []

game = False


class Bike:
    def __init__(self, addr, ina260):
        self.addr = addr
        self.ina260 = ina260


class Game:

    def __init__(self):
        game = False

        def run(self):
            while True:
                for addr in addresses:
                    try:
                        ina260 = adafruit_ina260.INA260(i2c, address=addr)
                        bikes.append(Bike(addr, ina260))
                    except Exception as e:
                        pass
                if len(bikes) > 0 and game:
                    print("---------------")
                    for bike in bikes:
                        try:
                            voltage = bike.ina260.voltage
                            current = bike.ina260.current
                            power = bike.ina260.power/1000
                            print(f"Bike {bike.addr} has: {voltage:.2f}V, {current:.2f}mA, {power:.2f}W")
                        except Exception as e:
                            print(f"Error reading sensor {bike.addr}: {e}")
                time.sleep(0.5)
