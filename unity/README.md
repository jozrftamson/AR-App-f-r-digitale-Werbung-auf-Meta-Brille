# Unity AR Client Snippet

Dieses Verzeichnis enthält ein prototypisches Skript (`AdBannerManager.cs`) für die Meta Quest 3 bzw. Meta Smart Glasses. Es demonstriert:

- Abruf ortsbasierter Werbedaten via REST (`/ads/nearby`).
- Nutzung von AR Foundation (Plane Detection + Anchors) zur Platzierung von Bannern auf vertikalen Flächen.
- Dynamisches Laden von Medien (Bilder) und Anheften als World-Space Canvas.

## Voraussetzungen
- Unity 2022.3 LTS oder neuer.
- Pakete: `AR Foundation`, `ARCore XR Plugin` (für Editor Tests) + `Oculus XR Plugin` bzw. `OpenXR` für Quest/Brille.
- Szenenobjekte: `ARSession`, `ARSessionOrigin` mit `ARCamera`, `ARPlaneManager`, `ARAnchorManager` und ein Banner-Prefab (Canvas + `RawImage` + `TMP_Text`).

## Verwendung
1. Füge `AdBannerManager` auf dasselbe GameObject wie Plane- und Anchor-Manager.
2. Verknüpfe das Banner Prefab im Inspector.
3. Setze `adsApiEndpoint` auf dein Backend (z. B. `https://api.example.com/ads/nearby`). Endpoint erwartet Query-Parameter `lat`, `lng`, `radius` und liefert JSON:
   ```json
   [
     { "id": "a1", "title": "Coffee Deal", "media_url": "https://cdn.example.com/coffee.jpg", "preferredSizeMeters": 1.5 }
   ]
   ```
4. Stelle sicher, dass Location Services aktiviert sind (Projekt Settings → XR Plug-in Management → Permissions > Fine Location).
5. Auf dem Device bauen, Opt-in Flow ausführen, Blicke/Gesten testen.

## Sicherheit & UX Hinweise
- Skaliere Banner über `preferredSizeMeters`, um Mindestlesbarkeit bei 2–5 m Entfernung zu gewährleisten.
- Ergänze Colliders/Distance Checks, sodass Banner keine kritischen Bereiche (Zebrastreifen, Verkehrsschilder) verdecken.
- Für persistente Platzierungen verwende zusätzlich Cloud Spatial Anchors (Azure/Meta) und erweitere `anchor_ref` im Payload.
