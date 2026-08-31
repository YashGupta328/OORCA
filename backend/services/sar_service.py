"""SAR detection orchestration service."""

from __future__ import annotations


class SarService:
    """High-level wrapper around the SAR detection engine."""

    def detect_scene(self, scene_path: str) -> list[dict]:
        from engine.sar.preprocessing import preprocess
        from engine.sar.segmentation import segment
        from engine.sar.detection import detect_candidates
        from engine.sar.classification import classify
        from engine.sar.postprocessing import postprocess

        pre = preprocess(scene_path)
        prob_map = segment(pre)
        candidates = detect_candidates(prob_map)
        classified = classify(candidates)
        return postprocess(classified)