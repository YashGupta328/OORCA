# AIS (Automatic Identification System)

Vessel tracking messages.

- **Sources** — MarineTraffic API, AIS Hub, raw terrestrial/satellite AIS feeds.
- **Message types** — Position reports (Class A/B), static and voyage data.
- **Fields used** — MMSI, timestamp, lat/lon, SOG, COG, heading, nav status, vessel name/type, IMO, length, beam, draft.
- **Use in OORCA** — input to `engine/ais/*` and `engine/attribution/*`.