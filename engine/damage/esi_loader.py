"""ESI (Environmental Sensitivity Index) feature loader for Phase 1.

Loads mock ESI data for the Indian coastal environment (Mumbai/Arabian Sea region).
In production, this would load from a PostGIS database or GeoJSON files.
"""

from __future__ import annotations

from typing import Any


ESI_FEATURES: list[dict[str, Any]] = [
    {
        "id": "esi-mangrove-001",
        "resource_type": "mangrove",
        "resource_name": "Thane Creek Mangroves",
        "sensitivity_score": 95,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.95, 19.15],
                [73.05, 19.15],
                [73.05, 19.25],
                [72.95, 19.25],
                [72.95, 19.15],
            ]],
        },
        "metadata": {
            "area_km2": 12.5,
            "dominant_species": "Avicennia marina",
            "conservation_status": "Protected",
        },
    },
    {
        "id": "esi-mangrove-002",
        "resource_type": "mangrove",
        "resource_name": "Vasai Creek Mangroves",
        "sensitivity_score": 90,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.80, 19.30],
                [72.90, 19.30],
                [72.90, 19.40],
                [72.80, 19.40],
                [72.80, 19.30],
            ]],
        },
        "metadata": {
            "area_km2": 8.3,
            "dominant_species": "Rhizophora mucronata",
            "conservation_status": "Reserved Forest",
        },
    },
    {
        "id": "esi-coral-001",
        "resource_type": "coral_reef",
        "resource_name": "Angria Bank Coral Reef",
        "sensitivity_score": 98,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [73.10, 16.80],
                [73.30, 16.80],
                [73.30, 17.00],
                [73.10, 17.00],
                [73.10, 16.80],
            ]],
        },
        "metadata": {
            "area_km2": 45.2,
            "depth_range_m": "10-25",
            "conservation_status": "Marine Protected Area",
        },
    },
    {
        "id": "esi-seagrass-001",
        "resource_type": "seagrass",
        "resource_name": "Malvan Seagrass Meadows",
        "sensitivity_score": 85,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [73.40, 16.10],
                [73.55, 16.10],
                [73.55, 16.25],
                [73.40, 16.25],
                [73.40, 16.10],
            ]],
        },
        "metadata": {
            "area_km2": 22.7,
            "dominant_species": "Halophila ovalis",
            "conservation_status": "Ecologically Sensitive Area",
        },
    },
    {
        "id": "esi-fish-001",
        "resource_type": "fish_habitat",
        "resource_name": "Mumbai Offshore Fisheries Zone",
        "sensitivity_score": 75,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.70, 18.80],
                [73.00, 18.80],
                [73.00, 19.20],
                [72.70, 19.20],
                [72.70, 18.80],
            ]],
        },
        "metadata": {
            "area_km2": 185.4,
            "key_species": ["Bombay duck", "Pomfret", "Mackerel", "Shrimp"],
            "fishing_intensity": "High",
        },
    },
    {
        "id": "esi-fish-002",
        "resource_type": "fish_habitat",
        "resource_name": "Alibaug Coastal Fisheries",
        "sensitivity_score": 70,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.85, 18.50],
                [73.00, 18.50],
                [73.00, 18.80],
                [72.85, 18.80],
                [72.85, 18.50],
            ]],
        },
        "metadata": {
            "area_km2": 92.1,
            "key_species": ["Sardine", "Anchovy", "Crab"],
            "fishing_intensity": "Medium",
        },
    },
    {
        "id": "esi-turtle-001",
        "resource_type": "sea_turtle_habitat",
        "resource_name": "Velas Turtle Nesting Beach",
        "sensitivity_score": 92,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [73.05, 17.85],
                [73.10, 17.85],
                [73.10, 17.95],
                [73.05, 17.95],
                [73.05, 17.85],
            ]],
        },
        "metadata": {
            "area_km2": 2.1,
            "species": "Olive Ridley",
            "nesting_season": "Nov-Mar",
            "conservation_status": "Critically Important",
        },
    },
    {
        "id": "esi-dolphin-001",
        "resource_type": "dolphin_habitat",
        "resource_name": "Sindhudurg Dolphin Sanctuary",
        "sensitivity_score": 88,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [73.30, 15.90],
                [73.50, 15.90],
                [73.50, 16.10],
                [73.30, 16.10],
                [73.30, 15.90],
            ]],
        },
        "metadata": {
            "area_km2": 58.3,
            "species": "Indian Ocean Humpback Dolphin",
            "conservation_status": "Sanctuary",
        },
    },
    {
        "id": "esi-protected-001",
        "resource_type": "protected_area",
        "resource_name": "Sanjay Gandhi National Park (Coastal Zone)",
        "sensitivity_score": 80,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.85, 19.15],
                [72.95, 19.15],
                [72.95, 19.25],
                [72.85, 19.25],
                [72.85, 19.15],
            ]],
        },
        "metadata": {
            "area_km2": 15.6,
            "designation": "National Park",
            "iucn_category": "II",
        },
    },
    {
        "id": "esi-protected-002",
        "resource_type": "protected_area",
        "resource_name": "Mahim Creek Bird Sanctuary",
        "sensitivity_score": 82,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.83, 19.03],
                [72.87, 19.03],
                [72.87, 19.07],
                [72.83, 19.07],
                [72.83, 19.03],
            ]],
        },
        "metadata": {
            "area_km2": 1.8,
            "key_species": ["Flamingo", "Heron", "Sandpiper"],
            "designation": "Bird Sanctuary",
        },
    },
    {
        "id": "esi-saltmarsh-001",
        "resource_type": "saltmarsh",
        "resource_name": "Uran Saltmarshes",
        "sensitivity_score": 78,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.92, 18.95],
                [73.00, 18.95],
                [73.00, 19.05],
                [72.92, 19.05],
                [72.92, 18.95],
            ]],
        },
        "metadata": {
            "area_km2": 6.4,
            "dominant_species": "Suaeda fruticosa",
            "conservation_status": "Wetland",
        },
    },
]


def load_esi_features() -> list[dict[str, Any]]:
    """Load all ESI features for the region.

    Returns:
        List of ESI feature dictionaries with geometry and metadata.
    """
    return ESI_FEATURES


def get_esi_feature(feature_id: str) -> dict[str, Any] | None:
    """Get a specific ESI feature by ID."""
    for feature in ESI_FEATURES:
        if feature["id"] == feature_id:
            return feature
    return None


def get_features_by_type(resource_type: str) -> list[dict[str, Any]]:
    """Get all ESI features of a specific type."""
    return [f for f in ESI_FEATURES if f["resource_type"] == resource_type]


class ESIResource:
    """Typed ESI resource for damage calculations."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data["id"]
        self.resource_type = data["resource_type"]
        self.resource_name = data["resource_name"]
        self.sensitivity_score = data["sensitivity_score"]
        self.geometry = data["geometry"]
        self.metadata = data.get("metadata", {})