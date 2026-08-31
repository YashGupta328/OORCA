"""SAR preprocessing: calibration, speckle filtering, land masking."""

from __future__ import annotations


def preprocess(scene_path: str) -> "object":
    """Return a preprocessed SAR scene object.

    Concrete implementation should:
    - apply orbit correction
    - calibrate to sigma0
    - apply a Lee / Gamma-MAP speckle filter
    - mask land using a coastline dataset
    """
    raise NotImplementedError