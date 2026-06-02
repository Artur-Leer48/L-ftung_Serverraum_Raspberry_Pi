from math import sin
from time import time

import bme280
import smbus2

from config import I2C_ADDRESS, I2C_PORT, SENSOR_MODUS


class Bme280Sensor:
    def __init__(self):
        self.bus = smbus2.SMBus(I2C_PORT)
        self.kalibrierung = bme280.load_calibration_params(
            self.bus,
            I2C_ADDRESS,
        )

    def read(self):
        daten = bme280.sample(self.bus, I2C_ADDRESS, self.kalibrierung)

        return daten.temperature, daten.humidity, daten.pressure


class MockSensor:
    def read(self):
        sekunden = time()
        temperatur = 24.5 + sin(sekunden / 12) * 3
        luftfeuchte = 48 + sin(sekunden / 16) * 8
        luftdruck = 1013 + sin(sekunden / 20) * 5

        return temperatur, luftfeuchte, luftdruck


def create_sensor():
    if SENSOR_MODUS == "mock":
        return MockSensor()

    return Bme280Sensor()
