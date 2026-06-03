# KI-Nutzung im Projekt – Lüftersteuerung Serverraum

**Projekt:** LF7 – LS2 Lüftersteuerung mit Raspberry Pi  
**Team:** Artur Leer  
**Stand:** 02.06.2026

---

## Eingesetzte KI

Wir haben Claude Sonnet von Anthropic genutzt, eingebunden in VS Code über die Erweiterung Claude Code.

---

## Warum?

Das Projekt hat Technologien kombiniert, die wir vorher nicht kannten: Flask, Docker, Threading zwischen Messprozess und Webserver, sowie SVG-Animationen und Canvas-Diagramme im Browser. Für einzelne Probleme wäre Recherche noch machbar gewesen, aber alles zusammen in einem Projekt war der Hauptgrund für den KI-Einsatz.

---

## Wie?

Wir haben Code nie einfach kopiert. Das Vorgehen war immer: Problem beschreiben, Antwort verstehen, testen, bei Fehlern die Fehlermeldung mitschicken und nachfragen was sie bedeutet. Die meisten Konzepte haben wir dadurch tatsächlich verstanden.

Konkrete Themen bei denen die KI geholfen hat:

**Threading:** Wie man Messwerte zwischen zwei Threads sicher teilt, ohne dass es zu gleichzeitigen Schreibzugriffen kommt. Daraus ist `app_state.py` mit `threading.Lock` entstanden.

**Hysterese:** Wir haben gefragt ob es ein bekanntes Muster gibt damit der Lüfter nicht jede Sekunde an- und ausschaltet. Die KI hat das Konzept aus der Regelungstechnik erklärt, wir haben es dann selbst implementiert.

**SVG-Animation:** Die Lüfterblätter haben sich beim Drehen verschoben. Die Ursache war eine falsche CSS-Eigenschaft (`transform-box: fill-box` statt `view-box`), die wir ohne die Erklärung nicht gefunden hätten.

**Browser-Cache:** Das Dashboard hat veraltete Werte angezeigt obwohl der Server neue geliefert hat. Wir haben zuerst im Python-Code gesucht, die KI hat dann auf das Browser-Caching hingewiesen.

---

## Wo die KI nicht geholfen hat

Einige Probleme mussten wir selbst debuggen, bevor die KI überhaupt helfen konnte. Zum Beispiel dass Docker unsere `messwerte.csv` als Verzeichnis angelegt hatte, das haben wir erst über `docker logs` herausgefunden. Das hat gezeigt: je unklarer das Problem beschrieben ist, desto weniger nützlich ist die Antwort.
