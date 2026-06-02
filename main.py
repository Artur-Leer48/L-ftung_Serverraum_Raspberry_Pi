from threading import Thread
from time import sleep

from gpiozero import OutputDevice

from app_state import get_temp_schwelle, update_measurement
from calculations import calculate_dew_point, celsius_to_fahrenheit
from config import (
    CSV_DATEI,
    LUEFTER_MODUS,
    LUEFTER_PIN,
    MESSINTERVALL_SEKUNDEN,
)
from csv_logger import write_measurement
from sensor import create_sensor
from webserver import run_webserver


def run_measurement_loop():
    sensor = create_sensor()
    luefter = None

    if LUEFTER_MODUS == "real":
        luefter = OutputDevice(LUEFTER_PIN, active_high=True, initial_value=False)

    while True:
        temperatur, luftfeuchte, luftdruck = sensor.read()
        temperatur_fahrenheit = celsius_to_fahrenheit(temperatur)
        taupunkt = calculate_dew_point(temperatur, luftfeuchte)

        if temperatur >= get_temp_schwelle():
            luefter_aktiv = True
            if luefter is not None:
                luefter.on()
        else:
            luefter_aktiv = False
            if luefter is not None:
                luefter.off()

        print("--------------------------------")
        print(f"Temperatur: {temperatur:.2f} °C")
        print(f"Temperatur: {temperatur_fahrenheit:.2f} °F")
        print(f"Taupunkt: {taupunkt:.2f} °C")
        print(f"Luftfeuchte: {int(luftfeuchte)} %")
        print(f"Luftdruck: {int(luftdruck)} hPa")
        print(f"Lüfter: {'AN' if luefter_aktiv else 'AUS'}")

        update_measurement(
            temperatur,
            temperatur_fahrenheit,
            taupunkt,
            luftfeuchte,
            luftdruck,
            luefter_aktiv,
        )

        write_measurement(
            CSV_DATEI,
            temperatur,
            temperatur_fahrenheit,
            taupunkt,
            luftfeuchte,
            luftdruck,
            luefter_aktiv,
        )

        sleep(MESSINTERVALL_SEKUNDEN)


def main():
    measurement_thread = Thread(target=run_measurement_loop, daemon=True)
    measurement_thread.start()
    run_webserver()


if __name__ == "__main__":
    main()
