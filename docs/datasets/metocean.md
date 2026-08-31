# Metocean

Surface winds and currents used as forcing for drift simulation.

- **Sources** — ECMWF ERA5 (hindcast), GFS / ECMWF / CMEMS (forecast), HYCOM / GLORYS currents.
- **Variables** — 10-m U/V wind, surface currents, sea surface temperature, air temperature, mixed layer depth.
- **Use in OORCA** — driving OpenDrift in `engine/drift/*`.