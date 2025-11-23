# Backend Mini-API (Node.js + Express)

Dieses Beispiel spiegelt die wichtigsten REST-Endpunkte des AR-Werbeprojekts wider. Es nutzt nur In-Memory-Daten, damit du die Request/Response-Struktur schnell nachvollziehen kannst.

## Setup & Start

```bash
cd backend
npm install
npm start
```

Der Server lauscht standardmäßig auf `http://localhost:3000` und stellt folgende Routen bereit:

| Methode | Pfad            | Beschreibung |
|---------|-----------------|--------------|
| GET     | `/health`       | Lebenszeichen |
| GET/POST| `/locations`    | Standorte listen/anlegen |
| GET/POST| `/ad-spaces`    | Werbeflächen listen/anlegen |
| GET/POST| `/campaigns`    | Kampagnen listen/anlegen |
| GET/POST| `/ads`          | Werbemittel listen/anlegen |
| GET     | `/ads/nearby`   | Ads für AR-Client filtern (lat/lng/radius) |

## Beispielanfragen

### 1. Standort anlegen
```bash
curl -X POST http://localhost:3000/locations \
  -H 'Content-Type: application/json' \
  -d '{
    "ownerId": "adv-001",
    "name": "Pop-up Store",
    "address": "Altmarkt 3",
    "latitude": 51.049,
    "longitude": 13.738,
    "geofenceRadiusM": 40
  }'
```
Antwort (`201`):
```json
{
  "id": "4f3a...",
  "ownerId": "adv-001",
  "name": "Pop-up Store",
  "latitude": 51.049,
  "longitude": 13.738,
  "geofenceRadiusM": 40,
  "status": "pending"
}
```

### 2. Werbefläche hinzufügen
```bash
curl -X POST http://localhost:3000/ad-spaces \
  -H 'Content-Type: application/json' \
  -d '{
    "locationId": "loc-001",
    "label": "Schaufenster links",
    "geometryType": "window",
    "anchorRef": { "type": "spatial_anchor", "provider": "azure", "anchorId": "abc-123" }
  }'
```

### 3. Kampagne erstellen
```bash
curl -X POST http://localhost:3000/campaigns \
  -H 'Content-Type: application/json' \
  -d '{
    "advertiserId": "adv-001",
    "name": "Winter Deals",
    "startAt": "2025-12-01T06:00:00Z",
    "endAt": "2026-01-10T22:00:00Z",
    "targetCategories": ["shopping", "food"]
  }'
```

### 4. Ad anlegen
```bash
curl -X POST http://localhost:3000/ads \
  -H 'Content-Type: application/json' \
  -d '{
    "campaignId": "camp-001",
    "adSpaceId": "space-001",
    "title": "20% auf Kuchen",
    "mediaUrl": "https://cdn.example.com/cake.jpg",
    "preferredSizeMeters": 1.0
  }'
```

### 5. Nearby Ads für AR-Client
```bash
curl "http://localhost:3000/ads/nearby?lat=51.0501&lng=13.7378&radius=150"
```
Antwort (`200`):
```json
[
  {
    "id": "ad-001",
    "title": "2x1 Cappuccino",
    "media_url": "https://cdn.example.com/coffee.jpg",
    "preferredSizeMeters": 1.5,
    "location": {
      "latitude": 51.0504,
      "longitude": 13.7373
    },
    "adSpace": {
      "id": "space-001",
      "label": "Fassade Front",
      "geometryType": "wall",
      "anchorRef": { "type": "plane_hint", "normal": [0, 0, 1] }
    }
  }
]
```

> **Hinweis:** In der echten Plattform würden Validierung, Authentifizierung, PostgreSQL (z. B. via Prisma/TypeORM) und Storage-Anbindung ergänzt. Dieses Beispiel fokussiert sich auf die Schnittstellenstruktur, sodass der Unity-Client direkt damit testen kann.
