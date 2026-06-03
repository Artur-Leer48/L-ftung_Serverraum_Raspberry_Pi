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
        t = time()
        # Temperatur: 20–32 °C, Periode ~20 s → jede Sekunde ~0.5–2 °C Änderung sichtbar
        temperatur  = 26.0 + sin(t / 3) * 6
        # Luftfeuchte: 35–65 %, Periode ~25 s
        luftfeuchte = 50.0 + sin(t / 4) * 15
        # Luftdruck: 1008–1018 hPa
        luftdruck   = 1013.0 + sin(t / 8) * 5

        return temperatur, luftfeuchte, luftdruck


def create_sensor():
    if SENSOR_MODUS == "mock":
        return MockSensor()

    return Bme280Sensor()
