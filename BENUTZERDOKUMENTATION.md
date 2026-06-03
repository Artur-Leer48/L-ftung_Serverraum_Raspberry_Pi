# Benutzerdokumentation – Lüftersteuerung Serverraum

**Projekt:** LF7 – LS2 Lüftersteuerung mit Raspberry Pi  
**Version:** 1.0  
**Stand:** 02.06.2026  
**Erstellt von:** Artur Leer, Claudia Dang, Danil Fartanov, Endrit Salihi

---

## 1. Über das System

Die Lüftersteuerung überwacht automatisch die Temperatur, Luftfeuchte und den Luftdruck im Serverraum. Ein angeschlossener Lüfter wird abhängig von der gemessenen Temperatur automatisch ein- und ausgeschaltet. Über ein webbasiertes Dashboard kann der aktuelle Zustand eingesehen und die Einschalttemperatur angepasst werden.

---

## 2. Voraussetzungen

**Für den Betrieb auf dem Raspberry Pi:**

- Raspberry Pi mit installiertem Docker
- BME280-Sensor, angeschlossen über I²C (Adresse 0x77, Port 1)
- Relais an GPIO-Pin 17
- Lüfter am Relais angeschlossen
- Netzwerkverbindung (für den Zugriff auf das Dashboard)

**Für den Test auf einem PC:**

- Docker Desktop installiert
- Kein Sensor oder Relais erforderlich — der Mock-Modus simuliert alle Werte

---

## 3. System starten

### Auf dem Raspberry Pi

```
docker compose up
```

Das System startet automatisch neu, wenn der Pi neu gebootet wird.

### Auf dem PC (Testmodus)

```
docker compose -f docker-compose.yml -f docker-compose.mock.yml up --build
```

Im Testmodus werden simulierte Temperaturwerte zwischen 20 und 32 °C verwendet. Der Lüfter wird nicht physisch angesteuert, der Zustand wird aber im Dashboard korrekt angezeigt.

---

## 4. Dashboard aufrufen

Sobald das System läuft, kann das Dashboard im Browser geöffnet werden:

| Gerät | Adresse |
|---|---|
| Raspberry Pi | `http://<IP-Adresse des Pi>:8000` |
| PC (Testmodus) | `http://localhost:8000` |

Die IP-Adresse des Pi lässt sich mit `hostname -I` auf dem Pi ermitteln.

---

## 5. Dashboard – Übersicht

Das Dashboard zeigt auf der linken Seite eine Navigation mit zwei Bereichen: Übersicht und Monitoring.

### 5.1 Übersicht

Der Hauptbereich zeigt die aktuellen Messwerte des Sensors in Echtzeit. Alle Werte aktualisieren sich automatisch jede Sekunde.

| Anzeige | Beschreibung |
|---|---|
| Temperatur | Aktuelle Raumtemperatur in °C und °F |
| Taupunkt | Temperatur, bei der Kondensation einsetzt |
| Luftfeuchte | Relative Luftfeuchtigkeit in % |
| Luftdruck | Aktueller Luftdruck in hPa |
| Lüfter | Zeigt AN oder AUS mit animiertem Lüftersymbol |

### 5.2 Einschalttemperatur anpassen

Im unteren Bereich der Übersicht befindet sich ein Regler zur Einstellung der Einschalttemperatur.

1. Slider verschieben oder Wert direkt ins Eingabefeld tippen
2. Der "Übernehmen"-Button wird aktiv sobald der Wert geändert wurde
3. Auf "Übernehmen" klicken — der Lüfter reagiert sofort

**Hinweis zur Ausschalttemperatur:** Der Lüfter schaltet sich erst aus, wenn die Temperatur 3 °C unterhalb der eingestellten Einschalttemperatur liegt. Das verhindert, dass der Lüfter bei Temperaturen nahe der Schwelle ständig an- und ausschaltet.

Beispiel bei einer Einschalttemperatur von 25 °C:

| Temperatur | Lüfter |
|---|---|
| ≥ 25 °C | geht AN |
| 22–24,9 °C | bleibt im aktuellen Zustand |
| < 22 °C | geht AUS |

### 5.3 Monitoring

Der Monitoring-Tab zeigt den zeitlichen Verlauf der Messwerte als Diagramme. Die letzten 120 Sekunden werden dargestellt. Die Ansicht aktualisiert sich automatisch solange der Tab geöffnet ist.

---

## 6. Messdaten als CSV

Alle Messwerte werden automatisch in der Datei `messwerte.csv` gespeichert. Die Datei liegt im Projektordner und kann jederzeit mit Excel oder einem Texteditor geöffnet werden.

Aufbau der Datei:

```
zeitstempel;temperatur;temperatur_fahrenheit;taupunkt;luftfeuchte;luftdruck;luefter_aktiv
2026-06-02 10:00:01;23.45;74.21;12.30;48;1013;False
2026-06-02 10:00:02;23.46;74.23;12.31;48;1013;False
```

---

## 7. System stoppen

```
docker compose down
```

---

## 8. Fehlerbehebung

**Dashboard zeigt keine aktuellen Werte**

Browser-Cache leeren mit Strg+Shift+R. Falls das nicht hilft, Container neu starten.

**Dashboard nicht erreichbar**

Prüfen ob der Container läuft: `docker ps`. Falls kein Container gelistet wird, System neu starten.

**Lüfter schaltet nicht**

Sicherstellen dass das Relais korrekt an GPIO-Pin 17 angeschlossen ist. Im Dashboard prüfen ob der Lüfterstatus auf AN steht — falls ja, liegt das Problem an der Hardware, nicht am System.

**Messwerte wirken unrealistisch**

Prüfen ob der BME280-Sensor korrekt an I²C angeschlossen ist. Der Sensor muss an Adresse 0x77 erreichbar sein. Mit `i2cdetect -y 1` auf dem Pi lässt sich das prüfen.

---

## 9. Technische Daten

| Parameter | Wert |
|---|---|
| Messintervall | 1 Sekunde |
| Standard-Einschalttemperatur | 25,0 °C |
| Hysterese | 3 °C |
| GPIO-Pin (Relais) | 17 |
| I²C-Adresse (BME280) | 0x77 |
| Dashboard-Port | 8000 |
| Messdatei | messwerte.csv |
