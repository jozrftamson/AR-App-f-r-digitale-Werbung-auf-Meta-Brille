# AR-App für digitale Werbung auf Meta-Brillen

Komplette Projektgrundlage für eine AR-Plattform, die ortsbasierte Werbeflächen auf der Meta Quest 3 bzw. Meta Smart Glasses sichtbar macht. Das Repository enthält Konzepte, Unity-Prototyp, Express-Backend sowie PostgreSQL-Schema und Roadmap.

## Verzeichnisüberblick

```
backend/   – Express-Mini-API mit Beispielendpunkten
db/        – PostgreSQL/PostGIS-Schema inkl. Views
unity/     – Unity-Skript + Anleitung für AR-Client-Prototyp
ROADMAP.md – Phasenplan & Meilensteine
```

## Schnellstart Backend

```bash
cd backend
npm install
npm start
```

Der Server lauscht auf `http://localhost:3000` und stellt u. a. `/locations`, `/ad-spaces`, `/ads`, `/campaigns` sowie `/ads/nearby` bereit. Das README im Unterordner beschreibt alle Beispielanfragen.

## Unity-Prototyp verwenden
1. Öffne ein Unity 2022.3 LTS Projekt mit AR Foundation + OpenXR/Oculus Plugin.
2. Lege eine Szene mit `ARSession`, `ARSessionOrigin`, `ARPlaneManager`, `ARAnchorManager` und deinem Banner-Prefab an.
3. Platziere `AdBannerManager.cs` aus `unity/` auf das Manager-Objekt und setze `adsApiEndpoint` auf dein Backend.
4. Baue auf Quest/Smart Glasses, aktiviere Location Services und teste Plane Detection + Banner-Platzierung.

## Datenbank-Schema anwenden

```bash
cd db
psql "$DATABASE_URL" -f schema.sql
```

Erfordert `uuid-ossp` und `postgis`. Das Schema spiegelt alle zuvor beschriebenen Datenmodelle (Users, Locations, AdSpaces, Campaigns, Ads, Impressions, Interactions, Reports).

## Roadmap & nächste Schritte
- `ROADMAP.md` enthält Phasen 0–6 (Setup, Backend, Dashboard, AR-Client, Spatial Anchors, Launch).
- Für einen produktiven Ausbau: Backend an echte DB anbinden, Auth einbauen, Unity-App mit Spatial Anchors und Safety-Checks erweitern.