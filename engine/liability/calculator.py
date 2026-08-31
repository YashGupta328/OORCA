"""Top-level liability calculator orchestrating all components."""

from __future__ import annotations


def calculate(incident: dict, iterations: int = 1000) -> dict:
    """Compute total liability with components and sensitivity analysis."""
    from engine.liability.volume import estimate_volume
    from engine.liability.cleanup import estimate_cleanup
    from engine.liability.restoration import estimate_restoration
    from engine.liability.fisheries import estimate_fisheries
    from engine.liability.tourism import estimate_tourism
    from engine.liability.ecological import estimate_ecological
    from engine.liability.discounting import discount
    from engine.liability.monte_carlo import simulate

    volume = estimate_volume(incident)
    cleanup = estimate_cleanup(incident, volume)
    restoration = estimate_restoration(incident)
    fisheries = estimate_fisheries(incident)
    tourism = estimate_tourism(incident)
    ecological = estimate_ecological(incident)
    discounted = discount({
        "cleanup": cleanup,
        "restoration": restoration,
        "fisheries": fisheries,
        "tourism": tourism,
        "ecological": ecological,
    })
    return simulate(discounted, iterations=iterations)