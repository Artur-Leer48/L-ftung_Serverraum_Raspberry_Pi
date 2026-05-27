from time import sleep
from gpiozero import OutputDevice

PFAD = "/sys/bus/iio/devices/iio:device0/"
LUEFTER_PIN = 17
TEMP_SCHWELLE = 25.0

luefter = OutputDevice(LUEFTER_PIN, active_high=True, initial_value=False)

while True:
    with open(PFAD + "in_temp_input", "r") as datei:
        temperatur_raw = float(datei.read())
    with open(PFAD + "in_humidityrelative_input", "r") as datei:
        luftfeuchte_raw = float(datei.read())

    with open(PFAD + "in_pressure_input", "r") as datei:
        luftdruck_raw = float(datei.read())

    temperatur = temperatur_raw / 1000
    luftfeuchte = luftfeuchte_raw / 1000
    luftdruck = luftdruck_raw / 1000

    if temperatur >= TEMP_SCHWELLE:
        luefter.on()
    else:
        luefter.off()

    print("--------------------------------")
    print(f"Temperatur: {temperatur:.2f} °C")
    print(f"Luftfeuchte: {int(luftfeuchte)} %")
    print(f"Luftdruck: {int(luftdruck)} hPa")
    print(f"Lüfter: {'AN' if luefter.value else 'AUS'}")

    sleep(3)
