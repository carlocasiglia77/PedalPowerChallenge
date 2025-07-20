# sensors/ina260.py
import board
import busio
from adafruit_ina260 import INA260


class INA260Sensor:
    def __init__(self, address):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = INA260(i2c, address=address)

    def read_voltage(self):
        return self.sensor.voltage

    def read_current(self):
        return self.sensor.current

    def read_power(self):
        return self.sensor.power
