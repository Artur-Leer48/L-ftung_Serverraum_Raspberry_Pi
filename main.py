from time import sleep
import smbus2
import bme280
from gpiozero import OutputDevice

I2C_PORT = 1
I2C_ADDRESS = 0x77
LUEFTER_PIN = 17
TEMP_SCHWELLE = 25.0

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

    sleep(2)
