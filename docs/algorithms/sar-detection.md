# SAR Oil Detection

The SAR pipeline transforms Sentinel-1 GRD products into labelled oil spill candidates.

## Stages

1. **Preprocessing** (`engine/sar/preprocessing.py`)
   - Orbit correction, calibration, speckle filtering, land masking.
2. **Segmentation** (`engine/sar/segmentation.py`)
   - U-Net / DeepLab model produces a dark-spot probability map.
3. **Detection** (`engine/sar/detection.py`)
   - Connected-components + thresholding converts the probability map into polygon candidates.
4. **Classification** (`engine/sar/classification.py`)
   - Candidate features (texture, contrast to neighbours, wind context) feed a binary classifier to discriminate oil from look-alikes (biogenic films, low-wind areas, ships).
5. **Postprocessing** (`engine/sar/postprocessing.py`)
   - Geometry validation, minimum-area filter, confidence scoring.

## Outputs

Per detection: timestamp, polygon geometry, area (km²), confidence, classifier score, scene metadata.

See `docs/datasets/sentinel1.md` for input data conventions.