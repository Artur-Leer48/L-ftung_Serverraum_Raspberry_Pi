# Abnahme-Checkliste – Lüftersteuerung Serverraum

**Projekt:** LF7 – LS2 Lüftersteuerung mit Raspberry Pi  
**Auftragnehmer:** Artur Leer, Claudia Dang, Danil Fartanov, Endrit Salihi
**Datum der Prüfung:** _______________

Diese Checkliste ist vor der Abgabe vollständig durchzugehen. Jeder Punkt muss geprüft und abgehakt sein.

---

## Phase 1 – PC-Test (Mock-Modus)

Container starten mit:
```
docker compose -f docker-compose.yml -f docker-compose.mock.yml up --build
```

### Konsole

- [ ] `docker logs -f <container>` zeigt alle 1 s neue Messwerte
- [ ] Temperatur erscheint mit 2 Nachkommastellen (z.B. `21.45 °C`)
- [ ] Temperatur in Fahrenheit wird ausgegeben
- [ ] Taupunkt wird ausgegeben
- [ ] Luftfeuchte erscheint ohne Nachkommastellen, abgeschnitten (z.B. `48 %`)
- [ ] Luftdruck erscheint ohne Nachkommastellen, abgeschnitten (z.B. `1013 hPa`)
- [ ] Lüfterstatus wird ausgegeben (`AN` / `AUS`)

### CSV

- [ ] `messwerte.csv` existiert nach dem Start
- [ ] Erste Zeile enthält die Spaltennamen
- [ ] Trennzeichen ist Semikolon
- [ ] Jede Sekunde kommt eine neue Zeile dazu
- [ ] Zeitstempel ist vorhanden

### Dashboard – Grundfunktion

- [ ] `http://localhost:8000` öffnet das Dashboard ohne Fehler
- [ ] Temperatur, Fahrenheit, Taupunkt, Luftfeuchte, Luftdruck werden angezeigt
- [ ] Werte aktualisieren sich automatisch ohne Reload
- [ ] Lüfterstatus (AN/AUS) wird korrekt angezeigt
- [ ] Lüfter-Animation dreht sich wenn Lüfter AN, steht still wenn AUS

### Dashboard – Schwellwert

- [ ] Slider und Eingabefeld sind vorhanden und synchronisiert
- [ ] "Übernehmen"-Button ist deaktiviert solange kein Wert geändert wurde
- [ ] Nach Änderung wird der Button aktiv
- [ ] Nach Klick auf "Übernehmen" schaltet der Lüfter sofort entsprechend
- [ ] Button wird nach dem Speichern wieder deaktiviert

### Hysterese-Test

- [ ] Schwellwert auf einen Wert setzen, der gerade über der aktuellen Temperatur liegt → Lüfter geht AN
- [ ] Schwellwert so setzen, dass die Temperatur im Bereich zwischen Schwelle und Schwelle−3 °C liegt → Lüfter bleibt im aktuellen Zustand
- [ ] Schwellwert mehr als 3 °C unter die aktuelle Temperatur setzen → Lüfter geht AUS

### Monitoring-Tab

- [ ] Tab "Monitoring" öffnet sich per Klick
- [ ] Temperaturverlauf wird als Chart dargestellt
- [ ] Chart füllt sich mit Datenpunkten während der Container läuft

---

## Phase 2 – Hardware-Test (Raspberry Pi)

Container starten mit:
```
docker compose up --build
```

- [ ] Container startet ohne Fehler
- [ ] BME280-Sensor liefert echte Werte (keine simulierten)
- [ ] Werte im Dashboard plausibel (Raumtemperatur ~18–30 °C)
- [ ] Relais schaltet hörbar wenn Schwellwert unter aktuelle Temperatur gesetzt wird
- [ ] Dashboard unter `http://<Pi-IP>:8000` erreichbar
- [ ] Nach Neustart des Pi startet der Container automatisch (`docker ps` prüfen)

---

## Phase 3 – Code-Review

- [ ] Keine unerlaubten Fremdbibliotheken in `main.py` und `sensor.py` (erlaubt: `time`, `math`, `csv`, `gpiozero` für GPIO)
- [ ] Code ist in sinnvolle Module aufgeteilt (`sensor.py`, `app_state.py`, `calculations.py`, `csv_logger.py`, `webserver.py`)
- [ ] `SETUP.md` erklärt den Start vollständig
- [ ] `KI_DOKUMENTATION.md` ist vorhanden und ausgefüllt

---

## Ergebnis

Alle Punkte abgehakt: **Ja / Nein**

Offene Punkte vor Abgabe:

| # | Beschreibung | Erledigt |
|---|-------------|----------|
|   |             |          |
