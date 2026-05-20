from time import sleep

PFAD = "/sys/bus/iio/devices/iio:device0/"

while True:
    with open(PFAD + "in_temp_input", "r") as datei:
        temperatur_raw = int(datei.read())
    with open(PFAD + "in_humidityrelative_input", "r") as datei:
        luftfeuchte_raw = int(datei.read())

    with open(PFAD + "in_pressure_input", "r") as datei:
        luftdruck_raw = int(datei.read())

    temperatur = temperatur_raw / 1000
    luftfeuchte = luftfeuchte_raw / 1000
    luftdruck = luftdruck_raw / 1000

    print("--------------------------------")
    print(f"Temperatur: {temperatur:.2f} °C")
    print(f"Luftfeuchte: {int(luftfeuchte)} %")
    print(f"Luftdruck: {int(luftdruck)} hPa")

    time.sleep(10)
