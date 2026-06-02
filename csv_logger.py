import csv
from pathlib import Path


FIELDNAMES = [
    "temperatur_celsius",
    "temperatur_fahrenheit",
    "taupunkt_celsius",
    "luftfeuchte_prozent",
    "luftdruck_hpa",
    "luefter",
]


def write_measurement(
    csv_datei,
    temperatur,
    temperatur_fahrenheit,
    taupunkt,
    luftfeuchte,
    luftdruck,
    luefter_aktiv,
):
    csv_pfad = Path(csv_datei)
    datei_existiert = csv_pfad.exists() and csv_pfad.stat().st_size > 0

    with csv_pfad.open("a", encoding="utf-8", newline="") as datei:
        writer = csv.DictWriter(datei, fieldnames=FIELDNAMES, delimiter=";")

        if not datei_existiert:
            writer.writeheader()

        writer.writerow(
            {
                "temperatur_celsius": f"{temperatur:.2f}",
                "temperatur_fahrenheit": f"{temperatur_fahrenheit:.2f}",
                "taupunkt_celsius": f"{taupunkt:.2f}",
                "luftfeuchte_prozent": int(luftfeuchte),
                "luftdruck_hpa": int(luftdruck),
                "luefter": "AN" if luefter_aktiv else "AUS",
            }
        )
