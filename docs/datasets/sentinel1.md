# Sentinel-1

Source of SAR imagery for oil spill detection.

- **Product** — Sentinel-1 GRD (Ground Range Detected), IW mode, VV or VH polarisation.
- **Acquisition** — Copernicus Open Access Hub; Copernicus Data Space Ecosystem (CDSE) post-2023.
- **Format** — GeoTIFF (after GRD-to-TC conversion) or SAFE.
- **Typical scene size** — ~170 km × 170 km per IW swath.
- **Use in OORCA** — input to `engine/sar/*`.

See `docs/algorithms/sar-detection.md` for processing details.