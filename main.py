from threading import Thread
from time import sleep

import bme280
import smbus2
from gpiozero import OutputDevice

from app_state import get_temp_schwelle, update_measurement
from calculations import calculate_dew_point, celsius_to_fahrenheit
from config import (
    CSV_DATEI,
    I2C_ADDRESS,
    I2C_PORT,
    LUEFTER_PIN,
    MESSINTERVALL_SEKUNDEN,
)
from csv_logger import write_measurement
from webserver import run_webserver


def run_measurement_loop():
    bus = smbus2.SMBus(I2C_PORT)
    kalibrierung = bme280.load_calibration_params(bus, I2C_ADDRESS)
    luefter = OutputDevice(LUEFTER_PIN, active_high=True, initial_value=False)

    while True:
        daten = bme280.sample(bus, I2C_ADDRESS, kalibrierung)
        temperatur = daten.temperature
        luftfeuchte = daten.humidity
        luftdruck = daten.pressure
        temperatur_fahrenheit = celsius_to_fahrenheit(temperatur)
        taupunkt = calculate_dew_point(temperatur, luftfeuchte)

        if temperatur >= get_temp_schwelle():
            luefter.on()
        else:
            luefter.off()

        print("--------------------------------")
        print(f"Temperatur: {temperatur:.2f} °C")
        print(f"Temperatur: {temperatur_fahrenheit:.2f} °F")
        print(f"Taupunkt: {taupunkt:.2f} °C")
        print(f"Luftfeuchte: {int(luftfeuchte)} %")
        print(f"Luftdruck: {int(luftdruck)} hPa")
        print(f"Lüfter: {'AN' if luefter.value else 'AUS'}")

        update_measurement(
            temperatur,
            temperatur_fahrenheit,
            taupunkt,
            luftfeuchte,
            luftdruck,
            luefter.value,
        )

        write_measurement(
            CSV_DATEI,
            temperatur,
            temperatur_fahrenheit,
            taupunkt,
            luftfeuchte,
            luftdruck,
            luefter.value,
        )

        sleep(MESSINTERVALL_SEKUNDEN)


def main():
    measurement_thread = Thread(target=run_measurement_loop, daemon=True)
    measurement_thread.start()
    run_webserver()


if __name__ == "__main__":
    main()
