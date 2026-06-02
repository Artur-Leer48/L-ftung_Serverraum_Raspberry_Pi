from time import sleep
import smbus2
import bme280
from gpiozero import OutputDevice

from config import (
    I2C_ADDRESS,
    I2C_PORT,
    LUEFTER_PIN,
    MESSINTERVALL_SEKUNDEN,
    TEMP_SCHWELLE,
)

bus = smbus2.SMBus(I2C_PORT)
kalibrierung = bme280.load_calibration_params(bus, I2C_ADDRESS)
luefter = OutputDevice(LUEFTER_PIN, active_high=True, initial_value=False)

while True:
    daten = bme280.sample(bus, I2C_ADDRESS, kalibrierung)
    temperatur = daten.temperature
    luftfeuchte = daten.humidity
    luftdruck = daten.pressure

    if temperatur >= TEMP_SCHWELLE:
        luefter.on()
    else:
        luefter.off()

    print("--------------------------------")
    print(f"Temperatur: {temperatur:.2f} °C")
    print(f"Luftfeuchte: {int(luftfeuchte)} %")
    print(f"Luftdruck: {int(luftdruck)} hPa")
    print(f"Lüfter: {'AN' if luefter.value else 'AUS'}")

    sleep(MESSINTERVALL_SEKUNDEN)
