# Roadmap & Phasenplan

## Phase 0 – Projektsetup (1 Woche)
- Repos & Branch-Strategie, CI/CD Skeleton, Infrastrukturzugänge (Cloud, S3, DB). 
- Basic IaC (Terraform oder Pulumi) für Datenbank + Storage.
- Sicherheitsrichtlinien, Coding Guidelines, Definition of Done.

## Phase 1 – Backend & Datenbasis (2–3 Wochen)
- Implementiere Auth (JWT, Rollen), CRUD-Endpunkte laut Schema, Medien-Upload (presigned URLs).
- Postgres + PostGIS aufsetzen, Migration (`db/schema.sql`) ausrollen, Seed-Daten für Testgebiet.
- Unit-/Integrationstests (Supertest/Jest), Linters, API-Doku (OpenAPI).

**Meilenstein:** API liefert stabile Antworten für Dashboard + AR-Client; Admin kann Standorte freigeben.

## Phase 2 – Advertiser Dashboard (2–3 Wochen)
- Frontend (React/Next.js) mit Login, Standortkarte, Ad-Space-Editor, Kampagnenwizard, Vorschau.
- Moderationstools für Admin (Approval, Reports, Abuse-Flagging).
- Analytics-Widgets (Impressions/Tag, Interaktionen) auf Basis aggregierter Tabellen.

**Meilenstein:** Erster Pilotkunde kann eigenständig Standort + Kampagne anlegen und live schalten.

## Phase 3 – AR-Client MVP (3–4 Wochen)
- Unity-Prototyp (Quest 3) mit Opt-in-Flow, Plane Detection, Banner-Rendering, Interaktionen.
- Integration des `/ads/nearby`-Endpoints, Caching, Telemetrie (Impressions/Interactions).
- Sicherheitsfeatures: Distanz-Limits, Helligkeitsregeln, Logging.

**Meilenstein:** Walkthrough im Testgebiet (eine Stadt, z. B. Dresden Altstadt) zeigt 1–2 Formate stabil.

## Phase 4 – Spatial Anchors & QA (2–4 Wochen)
- Optionaler Cloud-Anchor-Service (Azure/Niantic/Meta) für persistente Platzierung.
- Field Tests mit realen Gebäuden, Usability Feedback, Performance-Tuning.
- Datenschutz-Check (Opt-out, Data Retention, Consent-Audit), Pen-Test-Light.

**Meilenstein:** Beta-Release mit ausgewählten Partnern, Feedback in Backlog.

## Phase 5 – Launch-Vorbereitung (2–3 Wochen)
- Marketing- & Support-Material, Onboarding-Kits für Advertiser.
- Observability: Logs, Metrics, Alerting, On-Call-Prozesse.
- Vertragliche Themen (Nutzungsbedingungen, Werberichtlinien, DSGVO-Dokumentation).

**Meilenstein:** "Go/No-Go" Meeting, Launch-Date fixiert.

## Phase 6 – Post-Launch Iterationen (laufend)
- Erweiterte Formate (Video, 3D), Payments, Programmatic APIs.
- Erweiterung auf weitere Städte, Automatisierung für Spatial Anchors, A/B-Tests.
- Datengestützte Optimierungen (Relevanz-ML, Heatmaps) unter Beachtung der Privatsphäre.

## Testgebiet & MVP Fokus
- Pilotstadt: Dresden (Altmarkt, Prager Straße) – begrenztes Areal für valide Feldtests.
- Werbeformate: statisches Bild + Text-Overlay, optional 3D Billboard.
- KPIs: Anzahl freigeschalteter Flächen, tägliche Impressions, Nutzer-Opt-in-Rate, Report-Quote.
