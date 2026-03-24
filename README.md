# Dockerisierte DDD-Lösung für die Fahrzeug-API

Diese Referenzlösung kapselt die gegebene Fahrzeug-API in einer **DDD-orientierten FastAPI-Anwendung** mit Weboberfläche.

## Architektur

```text
app/
  domain/
    entities/              # fachliche Objekte und Value Objects
    services/              # fachliche Ports und Planungslogik
  application/
    dto/                   # Request-Modelle
    use_cases/             # Anwendungsfälle
  infrastructure/
    gateways/              # HTTP-Anbindung an die Fremd-API
  presentation/
    api/                   # REST-Endpunkte für UI/Clients
    web/                   # HTML/CSS/JS-Oberfläche
```

## Umgesetzte Funktionen

### 1. Schrittbewegung per Buttons
Die Fremd-API dokumentiert keine direkte Bewegung in diskreten Schritten. Deshalb werden die Richtungsbuttons so abgebildet:

- **Vorne** → `steer=0`, `throttle=+X`, warten, dann `throttle=0`
- **Hinten** → `steer=0`, `throttle=-X`, warten, dann `throttle=0`
- **Links** → `steer=-35`, `throttle=+X/2`, warten, dann Stop + Lenkung 0
- **Rechts** → `steer=+35`, `throttle=+X/2`, warten, dann Stop + Lenkung 0

Diese Schritte sind **zeitbasiert** und damit eine Approximation.

### 2. Weitere mit der dokumentierten API mögliche Ansteuerungen
Aus der Doku lassen sich aktuell folgende zusätzlichen Möglichkeiten ableiten, die in der Oberfläche ebenfalls umgesetzt sind:

- Status abfragen
- Lidar-Daten lesen
- Reset auslösen
- Lenkung mit beliebigem Prozentwert setzen
- Throttle mit beliebigem Prozentwert setzen
- Sofort stoppen über `throttle = 0`
- Kartonposition lesen
- Karton entlang X verschieben

## Oberfläche

Die Weboberfläche enthält:

- Direction Pad für definierte Schrittbewegungen
- Slider für **Steering** und **Throttle**
- **Stop**-Button
- Panels für **Status**, **Lidar** und **Reset**
- Formular für **Objektposition lesen** und **Objekt bewegen**
- Analyse-Panel für die unterstützten Capabilities
- <img width="1908" height="1058" alt="image" src="https://github.com/user-attachments/assets/a8afe739-b0e3-4eeb-92d2-24fb9e813391" />


## Start

### Mit Docker Compose

```bash
docker compose up --build
```

Danach ist die Anwendung unter `http://localhost:8080` erreichbar.

### Mit Docker direkt

```bash
docker build -t vehicle-control .
docker run --rm -p 8080:8080 \
  -e VEHICLE_API_BASE_URL="https://www.interagierende-systeme.de:8000" \
  vehicle-control
```

## REST-Fassade der Lösung

- `GET /api/status`
- `GET /api/lidar`
- `POST /api/reset`
- `POST /api/steer` mit `{ "value": 10 }`
- `POST /api/throttle` mit `{ "value": 10 }`
- `POST /api/move/forward` mit `{ "step_percent": 18, "duration_ms": 450 }`
- `POST /api/move/backward` mit `{ "step_percent": 18, "duration_ms": 450 }`
- `POST /api/move/left` mit `{ "step_percent": 18, "duration_ms": 450 }`
- `POST /api/move/right` mit `{ "step_percent": 18, "duration_ms": 450 }`
- `GET /api/object/{object_id}`
- `POST /api/object/move` mit `{ "objectId": 4, "x": 1 }`
- `GET /api/capabilities`

## Hinweise

- Weil die Fremd-API keine Distanz- oder Winkelrückmeldung pro Fahrbefehl dokumentiert, sind Bewegungssteps nicht metrisch exakt.
- Für reproduzierbarere Schritte könnten später Status- oder Lidar-basierte Regelkreise ergänzt werden.
- Die HTTP-Anbindung ist bewusst hinter einem Port/Gateway gekapselt, damit ein Mock oder eine andere Fahrzeug-API leicht austauschbar bleibt.
