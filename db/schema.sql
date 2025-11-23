-- PostgreSQL schema for AR advertising platform.
-- Run: psql -f schema.sql (requires superuser for CREATE EXTENSION).

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TYPE user_role AS ENUM ('user','advertiser','admin');
CREATE TYPE location_status AS ENUM ('draft','pending','approved','rejected');
CREATE TYPE adspace_geometry AS ENUM ('wall','window','floor','custom');
CREATE TYPE adspace_status AS ENUM ('draft','pending','active','disabled');
CREATE TYPE campaign_status AS ENUM ('draft','scheduled','running','paused','finished');
CREATE TYPE media_type AS ENUM ('image','video','model','text');
CREATE TYPE interaction_type AS ENUM ('open','save','mute','report');
CREATE TYPE report_status AS ENUM ('new','in_review','resolved','dismissed');
CREATE TYPE campaign_model AS ENUM ('flat','cpm');

CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  email varchar(255) UNIQUE NOT NULL,
  password_hash varchar(255) NOT NULL,
  display_name varchar(120),
  role user_role NOT NULL DEFAULT 'user',
  consent_location_ads boolean DEFAULT false,
  preferences jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE locations (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  owner_id uuid REFERENCES users(id) ON DELETE SET NULL,
  name text NOT NULL,
  address text,
  latitude numeric(9,6) NOT NULL,
  longitude numeric(9,6) NOT NULL,
  geom geography(Point,4326) GENERATED ALWAYS AS (
    ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography
  ) STORED,
  geofence_radius_m int NOT NULL DEFAULT 40,
  photos jsonb NOT NULL DEFAULT '[]'::jsonb,
  status location_status NOT NULL DEFAULT 'draft',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX locations_geom_idx ON locations USING GIST (geom);

CREATE TABLE ad_spaces (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  location_id uuid REFERENCES locations(id) ON DELETE CASCADE,
  label varchar(80) NOT NULL,
  geometry_type adspace_geometry NOT NULL,
  anchor_ref jsonb,
  surface_normal jsonb,
  dimensions jsonb,
  status adspace_status NOT NULL DEFAULT 'draft',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE campaigns (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  advertiser_id uuid REFERENCES users(id) ON DELETE SET NULL,
  name text NOT NULL,
  start_at timestamptz NOT NULL,
  end_at timestamptz NOT NULL,
  budget numeric,
  pricing_model campaign_model NOT NULL DEFAULT 'flat',
  target_categories text[] NOT NULL DEFAULT ARRAY[]::text[],
  status campaign_status NOT NULL DEFAULT 'draft',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX campaigns_status_idx ON campaigns (status);

CREATE TABLE ads (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id uuid REFERENCES campaigns(id) ON DELETE CASCADE,
  ad_space_id uuid REFERENCES ad_spaces(id) ON DELETE SET NULL,
  media_type media_type NOT NULL,
  media_url text NOT NULL,
  thumbnail_url text,
  title varchar(120),
  body text,
  cta_url text,
  display_rules jsonb NOT NULL DEFAULT '{}'::jsonb,
  preferred_size_meters numeric DEFAULT 1.2,
  enabled boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE impressions_daily (
  id bigserial PRIMARY KEY,
  ad_id uuid REFERENCES ads(id) ON DELETE CASCADE,
  location_id uuid REFERENCES locations(id) ON DELETE CASCADE,
  day date NOT NULL,
  impressions int NOT NULL DEFAULT 0,
  unique_viewers int NOT NULL DEFAULT 0,
  avg_dwell_time_seconds numeric,
  CONSTRAINT impressions_daily_unique UNIQUE (ad_id, day)
);

CREATE TABLE interactions (
  id bigserial PRIMARY KEY,
  ad_id uuid REFERENCES ads(id) ON DELETE CASCADE,
  user_id uuid REFERENCES users(id) ON DELETE SET NULL,
  event_type interaction_type NOT NULL,
  metadata jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE reports (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  reporter_id uuid REFERENCES users(id) ON DELETE SET NULL,
  ad_id uuid REFERENCES ads(id) ON DELETE CASCADE,
  message text,
  status report_status NOT NULL DEFAULT 'new',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

-- Simple view to join ads with locations for convenient API querying.
CREATE OR REPLACE VIEW ad_with_location AS
SELECT
  ads.id AS ad_id,
  ads.title,
  ads.media_url,
  ads.preferred_size_meters,
  ads.enabled,
  ad_spaces.id AS ad_space_id,
  ad_spaces.label,
  ad_spaces.geometry_type,
  ad_spaces.anchor_ref,
  locations.id AS location_id,
  locations.latitude,
  locations.longitude,
  locations.geom
FROM ads
JOIN ad_spaces ON ad_spaces.id = ads.ad_space_id
JOIN locations ON locations.id = ad_spaces.location_id;
