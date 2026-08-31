"""Semantic segmentation for SAR dark spots."""

from __future__ import annotations


def segment(scene: "object") -> "object":
    """Run a U-Net / DeepLab model on the preprocessed scene."""
    raise NotImplementedError