# AR Ad Glasses

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Language](https://img.shields.io/badge/language-TypeScript-3178c6.svg)
![Language](https://img.shields.io/badge/language-JavaScript-f7df1e.svg?logo=javascript&logoColor=000000)
![Top language](https://img.shields.io/github/languages/top/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille)
![License](https://img.shields.io/github/license/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille?style=flat-square)
![Downloads](https://img.shields.io/github/downloads/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille/total?style=flat-square)
[![CodSpeed](https://img.shields.io/endpoint?url=https://codspeed.io/badge.json)](https://codspeed.io/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille?utm_source=badge)

[![Discord](https://img.shields.io/discord/000000000000000000?label=Discord&logo=discord&style=flat-square)](https://discord.gg/your-invite-code)
[![GitHub stars](https://img.shields.io/github/stars/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille?style=flat-square)](https://github.com/jozrftamson/AR-App-f-r-digitale-Werbung-auf-Meta-Brille/stargazers)

> **AR Ad Glasses** macht Städte zu dynamischen Media-Spaces: Echtzeit-Logo-Erkennung, ortsbasierte Werbeplätze und AR-Overlays für Meta Quest 3 & Smart Glasses.

---

## Highlights
- 🌍 **End-to-End Plattform**: FastAPI Vision-Service, Node.js Location-API, Unity AR-Client & PostgreSQL/PostGIS-Schema.
- 👓 **AR-Overlay Workflow**: Kamera-Stream → Logo/Brand Detection → Tracking → On-Device Banner-Platzierung.
- ⚙️ **Erweiterbar**: Modularer Aufbau für echte Modelle (ONNX/Cloud), GPS-Daten, Kampagnen und Analytics.
- 🧪 **Getestet & dokumentiert**: Pytest-Suite, Setup-Guides und Roadmap für den produktiven Ausbau.

---

## Demo

<video src="demo/demo.mp4" controls width="640">
  Dein Browser unterstützt das Video-Tag nicht.
</video>

– oder auf YouTube ansehen: [AR ads – Deine Stadt als Media-Space](https://www.youtube.com/shorts/yDkVgCdM0X4)  
– Kanal: [@aradvertisingmarketing](https://www.youtube.com/@aradvertisingmarketing)

---

## Architektur auf einen Blick
| Layer | Technologie | Zweck |
| --- | --- | --- |
| Vision Service | Python 3.12, FastAPI, OpenCV | Analyse einzelner Frames/Videos, Tracking & Bounding Boxes |
| Spatial/Ads API | Node.js + Express | REST-Endpunkte für Locations, Kampagnen, Anzeigen |
| Datenhaltung | PostgreSQL + PostGIS | Geodaten, Kampagnen, Impressionen, Reports |
| AR Client | Unity 2022 LTS, AR Foundation, OpenXR | Rendering der Werbeflächen auf Quest/Smart Glasses |
| Prototyp Web | HTML/JS (getUserMedia) | Browser-Demo mit Kamera-Overlay |
| Java Tracker | Maven + OpenCV | Referenz-Implementation für klassische Logo-Detection |

---

## Verzeichnisüberblick
```
backend/          Express-Mini-API (Locations, Ads, Campaigns)
db/               PostgreSQL/PostGIS-Schema & Views
python-backend/   FastAPI Vision-Service inkl. Tests
prototype/backend Flask/FastAPI-Sketch für frühe Iterationen
prototype/web/    Browser-Demo mit Kamera-Overlay
src/main/java/    Logo-Tracker (Java, OpenCV)
unity/            Unity-Skripte & Anleitung
ROADMAP.md        Phasenplanung & Milestones
```

---

## Quick Start

### 1. Python Vision-Service
```bash
cd python-backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```
- **Endpoints**: `/health`, `POST /analyze-frame`, `POST /analyze-video`
- **Model Swap**: Passe `detector.py::detect_logos` an (ONNX, Cloud-API etc.).

### 2. Node.js Ads-API
```bash
cd backend
npm install
npm start
```
- Läuft auf `http://localhost:3000` mit Routen wie `/locations`, `/ad-spaces`, `/ads/nearby`.

### 3. Web-Prototype
```bash
cd prototype/web
# Öffne index.html (z.B. via VS Code Live Server)
```
- Nutzt `getUserMedia` + Canvas, ruft das jeweilige Backend an und zeigt AR-Overlays.

---

## Java Logo Tracker (Referenz)
Dieses Beispiel demonstriert die Logo-/Farberkennung mit OpenCV-Trackern.

**Build & Run**
```bash
mvn clean package
java -jar target/logo-tracker-0.1.0.jar 0          # Webcam
java -jar target/logo-tracker-0.1.0.jar video.mp4  # Datei
```

**OpenCV Hinweise**
- Abhängigkeit: `org.bytedeco:opencv-platform` (plattformspezifische Binaries).
- Eigene Modelle: DNN via `Dnn.readNetFromONNX`, Preprocessing & `net.forward()` in `detection.LogoDetector` implementieren.
- Empfohlene Modelle: YOLOv8, Faster R-CNN, RetinaNet oder Cloud-Dienste (AutoML, Rekognition, Custom Vision).

---

## Datenbank & Unity
- `db/schema.sql`: Vollständiges PostgreSQL/PostGIS-Schema (Users, Locations, AdSpaces, Campaigns, Ads, Impressions, Interactions, Reports).  
  **Setup**: `psql "$DATABASE_URL" -f schema.sql` (erfordert `uuid-ossp`, `postgis`).
- `unity/AdBannerManager.cs`: Bindet REST-Endpunkte und platziert Banner über Plane Detection.  
  **Voraussetzungen**: Unity 2022.3 LTS, AR Foundation, OpenXR/Oculus Plugin, Location Services aktiviert.

---

## Tests
```bash
cd python-backend
source .venv/bin/activate
pytest
```
- Testen `/health` und `/analyze-frame` mit synthetischen Frames & Monkeypatching.
- Weitere Szenarien (z. B. `/analyze-video`) lassen sich leicht ergänzen.

---

## Roadmap & Nächste Schritte
- Roadmap (Phasen 0–6) in `ROADMAP.md` dokumentiert.
- Empfohlene Erweiterungen:
  1. Vision-Service an echte GPU-Modelle koppeln (ONNX/TensorRT oder Remote-Inferenz).
  2. Node-Backend mit PostgreSQL/PostGIS verbinden + Auth einführen.
  3. Unity-Client mit Spatial Anchors, Safety-Checks und Analytics ausstatten.
  4. Continuous Deployment (GitHub Actions + Container Registry) vorbereiten.

---

## Support & Community
- **Discord**: Platzhalter-Link ersetzen, sobald Community-Server live ist.
- **Issues / Ideen**: Bitte GitHub Issues nutzen.
- **Contributions**: PRs willkommen – haltet euch an die Coding-Guidelines und fügt Tests & Docs hinzu.

> Fragen oder Feature-Wünsche? Öffne ein Issue oder melde dich im Discord – wir freuen uns auf dein Feedback!
