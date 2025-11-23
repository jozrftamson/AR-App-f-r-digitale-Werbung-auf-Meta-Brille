# AR Ad Glasses

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Language](https://img.shields.io/badge/language-TypeScript-3178c6.svg)
![Language](https://img.shields.io/badge/language-JavaScript-f7df1e.svg?logo=javascript&logoColor=000000)
![Top language](https://img.shields.io/github/languages/top/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille)

[![Discord](https://img.shields.io/discord/000000000000000000?label=Discord&logo=discord&style=flat-square)](https://discord.gg/your-invite-code)
[![GitHub stars](https://img.shields.io/github/stars/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille?style=flat-square)](https://github.com/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille/stargazers)
![License](https://img.shields.io/github/license/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille?style=flat-square)
![Downloads](https://img.shields.io/github/downloads/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille/total?style=flat-square)

<sub>Community- & Download-Links aktualisieren, sobald Discord-Server, Einladung, YouTube-Video und Release-Zähler final sind.</sub>

## Demo Video

[![Watch the video](https://img.youtube.com/vi/ABC123XYZ/maxresdefault.jpg)](https://www.youtube.com/watch?v=ABC123XYZ)

[YouTube-Kanal @aradvertisingmarketing](https://www.youtube.com/@aradvertisingmarketing)

Komplette Projektgrundlage für eine AR-Plattform („AR Ad Glasses“), die ortsbasierte Werbeflächen auf der Meta Quest 3 bzw. Meta Smart Glasses sichtbar macht. Das Repository enthält Konzepte, Unity-Prototyp, Express-Backend sowie PostgreSQL-Schema und Roadmap.

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