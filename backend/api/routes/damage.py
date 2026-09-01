"""Damage assessment endpoints for Phase 1."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from backend.api.schemas.damage import DamageAssessmentRead
from backend.services.damage_service import DamageService

router = APIRouter(prefix="/api/damage", tags=["damage"])


def get_damage_service() -> DamageService:
    return DamageService()


@router.post("/assess", response_model=DamageAssessmentRead)
async def assess_damage(
    simulation_run_id: str,
    service: DamageService = Depends(get_damage_service),
) -> DamageAssessmentRead:
    """Calculate damage assessment for a simulation run."""
    result = await service.assess_damage(simulation_run_id)
    if not result:
        raise HTTPException(status_code=404, detail="Simulation run not found or not completed")
    return result


@router.get("/assessments/{assessment_id}", response_model=DamageAssessmentRead)
async def get_assessment(
    assessment_id: str,
    service: DamageService = Depends(get_damage_service),
) -> DamageAssessmentRead:
    """Get damage assessment by ID."""
    assessment = await service.get_assessment(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment