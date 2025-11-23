const express = require('express');
const cors = require('cors');
const { v4: uuid } = require('uuid');

const app = express();
app.use(cors());
app.use(express.json());

// --- Demo data (would live in PostgreSQL in production) ---
const users = [
  { id: 'user-consumer', role: 'user', displayName: 'Quest Tester' },
  { id: 'adv-001', role: 'advertiser', displayName: 'Cafe Aurora' }
];

const locations = [
  {
    id: 'loc-001',
    ownerId: 'adv-001',
    name: 'Cafe Aurora – Innenstadt',
    address: 'Hauptstraße 12, Dresden',
    latitude: 51.0504,
    longitude: 13.7373,
    geofenceRadiusM: 60,
    status: 'approved'
  }
];

const adSpaces = [
  {
    id: 'space-001',
    locationId: 'loc-001',
    label: 'Fassade Front',
    geometryType: 'wall',
    anchorRef: { type: 'plane_hint', normal: [0, 0, 1] },
    status: 'active'
  }
];

const campaigns = [
  {
    id: 'camp-001',
    advertiserId: 'adv-001',
    name: 'Frühstückswochen',
    startAt: '2025-11-01T06:00:00Z',
    endAt: '2025-12-01T18:00:00Z',
    targetCategories: ['food'],
    status: 'running'
  }
];

const ads = [
  {
    id: 'ad-001',
    campaignId: 'camp-001',
    adSpaceId: 'space-001',
    mediaUrl: 'https://cdn.example.com/coffee.jpg',
    mediaType: 'image',
    title: '2x1 Cappuccino',
    description: 'Zwischen 8–10 Uhr, nur heute!',
    preferredSizeMeters: 1.5,
    enabled: true
  }
];

// --- Helpers ---
const requireFields = (obj, fields) =>
  fields.filter((field) => obj[field] === undefined || obj[field] === null);

const toNumber = (value, fallback) => {
  const parsed = parseFloat(value);
  return Number.isFinite(parsed) ? parsed : fallback;
};

const haversine = (lat1, lon1, lat2, lon2) => {
  const R = 6371e3; // meters
  const toRad = (deg) => (deg * Math.PI) / 180;
  const φ1 = toRad(lat1);
  const φ2 = toRad(lat2);
  const Δφ = toRad(lat2 - lat1);
  const Δλ = toRad(lon2 - lon1);
  const a =
    Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
    Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};

// --- Routes ---
app.get('/health', (req, res) => res.json({ status: 'ok' }));

app.get('/locations', (req, res) => {
  res.json(locations);
});

app.post('/locations', (req, res) => {
  const missing = requireFields(req.body, ['ownerId', 'name', 'latitude', 'longitude']);
  if (missing.length) {
    return res.status(400).json({ error: 'Missing fields', fields: missing });
  }
  const location = {
    id: uuid(),
    ownerId: req.body.ownerId,
    name: req.body.name,
    address: req.body.address || '',
    latitude: Number(req.body.latitude),
    longitude: Number(req.body.longitude),
    geofenceRadiusM: Number(req.body.geofenceRadiusM || 50),
    status: 'pending'
  };
  locations.push(location);
  res.status(201).json(location);
});

app.get('/ad-spaces', (req, res) => {
  res.json(adSpaces);
});

app.post('/ad-spaces', (req, res) => {
  const missing = requireFields(req.body, ['locationId', 'label', 'geometryType']);
  if (missing.length) {
    return res.status(400).json({ error: 'Missing fields', fields: missing });
  }
  const space = {
    id: uuid(),
    locationId: req.body.locationId,
    label: req.body.label,
    geometryType: req.body.geometryType,
    anchorRef: req.body.anchorRef || null,
    status: 'pending'
  };
  adSpaces.push(space);
  res.status(201).json(space);
});

app.get('/campaigns', (req, res) => {
  res.json(campaigns);
});

app.post('/campaigns', (req, res) => {
  const missing = requireFields(req.body, ['advertiserId', 'name', 'startAt', 'endAt']);
  if (missing.length) {
    return res.status(400).json({ error: 'Missing fields', fields: missing });
  }
  const camp = {
    id: uuid(),
    advertiserId: req.body.advertiserId,
    name: req.body.name,
    startAt: req.body.startAt,
    endAt: req.body.endAt,
    targetCategories: req.body.targetCategories || [],
    status: 'draft'
  };
  campaigns.push(camp);
  res.status(201).json(camp);
});

app.get('/ads', (req, res) => {
  res.json(ads);
});

app.post('/ads', (req, res) => {
  const missing = requireFields(req.body, ['campaignId', 'adSpaceId', 'title', 'mediaUrl']);
  if (missing.length) {
    return res.status(400).json({ error: 'Missing fields', fields: missing });
  }
  const ad = {
    id: uuid(),
    campaignId: req.body.campaignId,
    adSpaceId: req.body.adSpaceId,
    mediaUrl: req.body.mediaUrl,
    mediaType: req.body.mediaType || 'image',
    title: req.body.title,
    description: req.body.description || '',
    preferredSizeMeters: Number(req.body.preferredSizeMeters || 1.2),
    enabled: true
  };
  ads.push(ad);
  res.status(201).json(ad);
});

app.get('/ads/nearby', (req, res) => {
  const lat = toNumber(req.query.lat, locations[0].latitude);
  const lng = toNumber(req.query.lng, locations[0].longitude);
  const radius = toNumber(req.query.radius, 200);

  const activeAds = ads.filter((ad) => {
    const campaign = campaigns.find((c) => c.id === ad.campaignId && c.status === 'running');
    const space = adSpaces.find((s) => s.id === ad.adSpaceId);
    const location = locations.find((l) => l.id === space?.locationId && l.status === 'approved');
    if (!campaign || !space || !location || !ad.enabled) {
      return false;
    }
    const distance = haversine(lat, lng, location.latitude, location.longitude);
    return distance <= radius;
  });

  const payload = activeAds.map((ad) => {
    const space = adSpaces.find((s) => s.id === ad.adSpaceId);
    const location = locations.find((l) => l.id === space.locationId);
    return {
      id: ad.id,
      title: ad.title,
      media_url: ad.mediaUrl,
      preferredSizeMeters: ad.preferredSizeMeters,
      location: {
        latitude: location.latitude,
        longitude: location.longitude
      },
      adSpace: {
        id: space.id,
        label: space.label,
        geometryType: space.geometryType,
        anchorRef: space.anchorRef
      }
    };
  });

  res.json(payload);
});

if (require.main === module) {
  const port = process.env.PORT || 3000;
  app.listen(port, () => console.log(`API listening on http://localhost:${port}`));
}

module.exports = app;
