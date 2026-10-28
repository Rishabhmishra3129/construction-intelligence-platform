"""Deterministic project economics. Pure functions with no UI dependencies."""

from dataclasses import dataclass
from typing import Tuple

from config.settings import (
    CEMENT_BAGS_PER_SQFT,
    MILESTONES,
    PROJECT_SQFT_MAX,
    PROJECT_SQFT_MIN,
    STRUCTURE_CONFIG,
    TIER_RATES,
)


@dataclass(frozen=True)
class MilestoneStatus:
    name: str
    threshold: int
    done: bool


@dataclass(frozen=True)
class ProjectEconomics:
    built_up_sqft: float
    structure: str
    tier: str
    completion_pct: int
    total_budget: float
    capex_incurred: float
    asset_value: float
    steel_tonnes: float
    cement_bags: float
    milestones: Tuple[MilestoneStatus, ...]


def compute_economics(
    built_up_sqft: float, structure: str, tier: str, completion_pct: int
) -> ProjectEconomics:
    """Compute budget, capex, valuation, and material needs in INR.

    Raises ValueError for out-of-range or unknown inputs.
    """
    if not PROJECT_SQFT_MIN <= built_up_sqft <= PROJECT_SQFT_MAX:
        raise ValueError(
            f"Built-up area must be between {PROJECT_SQFT_MIN:,} and {PROJECT_SQFT_MAX:,} sq ft."
        )
    if structure not in STRUCTURE_CONFIG:
        raise ValueError(f"Unknown structure type: {structure}")
    if tier not in TIER_RATES:
        raise ValueError(f"Unknown location tier: {tier}")
    if not 0 <= completion_pct <= 100:
        raise ValueError("Completion percentage must be between 0 and 100.")

    rates = TIER_RATES[tier]
    config = STRUCTURE_CONFIG[structure]
    fraction = completion_pct / 100

    total_budget = built_up_sqft * rates["build_inr_per_sqft"] * config["cost_factor"]
    milestones = tuple(
        MilestoneStatus(name, threshold, completion_pct >= threshold)
        for name, threshold in MILESTONES
    )

    return ProjectEconomics(
        built_up_sqft=built_up_sqft,
        structure=structure,
        tier=tier,
        completion_pct=completion_pct,
        total_budget=total_budget,
        capex_incurred=total_budget * fraction,
        asset_value=built_up_sqft * rates["market_inr_per_sqft"] * fraction,
        steel_tonnes=built_up_sqft * config["steel_kg_sqft"] / 1000,
        cement_bags=built_up_sqft * CEMENT_BAGS_PER_SQFT,
        milestones=milestones,
    )
