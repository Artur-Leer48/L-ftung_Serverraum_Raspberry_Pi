from time import sleep

import bme280
import smbus2
from gpiozero import OutputDevice

from calculations import calculate_dew_point, celsius_to_fahrenheit
from config import (
    CSV_DATEI,
    I2C_ADDRESS,
    I2C_PORT,
    LUEFTER_PIN,
    MESSINTERVALL_SEKUNDEN,
    TEMP_SCHWELLE,
)
from csv_logger import write_measurement

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

    if temperatur >= TEMP_SCHWELLE:
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
