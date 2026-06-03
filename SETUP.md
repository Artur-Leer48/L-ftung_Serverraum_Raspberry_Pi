# Setup & Betrieb

## Voraussetzungen

- Docker Desktop installiert

---

## Testen auf dem PC (Mock-Modus)

Im Mock-Modus werden keine echten Sensoren oder GPIO-Pins benötigt.
Der MockSensor liefert simulierte Temperaturwerte die sich jede Sekunde ändern.

**1. messwerte.csv anlegen** (nur beim ersten Mal nötig)

Die Datei muss als leere Datei existieren bevor Docker sie mounten kann:

```
echo "zeitstempel,temperatur,temperatur_fahrenheit,taupunkt,luftfeuchte,luftdruck,luefter_aktiv" > messwerte.csv
```

**2. Container bauen und starten**

```
docker compose -f docker-compose.yml -f docker-compose.mock.yml up --build
```

**3. Dashboard öffnen**

```
http://localhost:8000
```

Die Temperatur ändert sich jede Sekunde zwischen ~20–32 °C.
Der Lüfter schaltet bei 25 °C ein und bei 22 °C aus (Hysterese).

**Neu starten ohne neu zu bauen:**

```
docker compose -f docker-compose.yml -f docker-compose.mock.yml up
```

**Nach Änderungen an HTML/CSS/JS neu bauen:**

Wenn Änderungen an `templates/` oder `static/` nicht im Browser sichtbar sind, muss der Container neu gebaut werden:

```
docker compose -f docker-compose.yml -f docker-compose.mock.yml build
docker compose -f docker-compose.yml -f docker-compose.mock.yml up
```

Danach im Browser **Strg+Shift+R** drücken, damit auch der Browser-Cache geleert wird.

**Stoppen:**

```
docker compose down
```

---

## Betrieb auf dem Raspberry Pi (Real-Modus)

**Voraussetzungen auf dem Pi:**
- Docker installiert (`curl -fsSL https://get.docker.com | sh`)
- BME280-Sensor an I2C angeschlossen (Standard: Adresse 0x77, Port 1)
- Relais an GPIO-Pin 17 angeschlossen

**1. Projekt auf den Pi kopieren**

```
scp -r . pi@<IP-ADRESSE>:/home/pi/lueftung
```

Oder per Git:

```
git clone <repo-url> /home/pi/lueftung
cd /home/pi/lueftung
```

**2. messwerte.csv anlegen**

```
echo "zeitstempel,temperatur,temperatur_fahrenheit,taupunkt,luftfeuchte,luftdruck,luefter_aktiv" > messwerte.csv
```

**3. Container bauen und starten**

```
docker compose up --build
```

Kein `-f docker-compose.mock.yml` — dadurch gilt automatisch `SENSOR_MODUS: real`.

**4. Dashboard öffnen**

```
http://<PI-IP-ADRESSE>:8000
```

**Mit automatischem Neustart nach Reboot:**

`restart: unless-stopped` ist bereits in der docker-compose.yml eingetragen.
Der Container startet also automatisch neu wenn der Pi neu bootet,
solange Docker als Dienst läuft:

```
sudo systemctl enable docker
```

---

## Modi im Überblick

| Befehl | Sensor | Lüfter | Verwendung |
|---|---|---|---|
| `docker compose up` | real | real | Raspberry Pi mit Hardware |
| `docker compose -f docker-compose.yml -f docker-compose.mock.yml up` | mock | mock | PC zum Testen |

---

## Lüfterlogik

| Temperatur | Aktion |
|---|---|
| ≥ Einschalttemperatur (Standard: 25 °C) | Lüfter geht **AN** |
| < Einschalttemperatur − 3 °C (Standard: 22 °C) | Lüfter geht **AUS** |
| Dazwischen | Lüfter behält aktuellen Zustand (Hysterese) |

Die Einschalttemperatur kann im Dashboard unter **Steuerung** jederzeit geändert werden.
Die Ausschalttemperatur ist immer 3 °C darunter.

---

## Konfiguration

Feste Werte in `config.py`:

| Variable | Standard | Bedeutung |
|---|---|---|
| `TEMP_SCHWELLE` | 25.0 | Einschalttemperatur beim Start |
| `MESSINTERVALL_SEKUNDEN` | 1 | Wie oft der Sensor ausgelesen wird |
| `LUEFTER_PIN` | 17 | GPIO-Pin für das Relais |
| `I2C_ADDRESS` | 0x77 | I2C-Adresse des BME280 |
| `CSV_DATEI` | messwerte.csv | Pfad zur Messwertdatei |
