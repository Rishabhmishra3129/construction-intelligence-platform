import pytest

from core.cost_engine import compute_economics
from core.formatting import fmt_inr

RCC = "RCC Framed Residential"
T1 = "Tier 1 (Metro)"


def test_budget_capex_and_valuation_for_rcc_metro():
    econ = compute_economics(2000, RCC, T1, 40)
    assert econ.total_budget == pytest.approx(2000 * 2800)
    assert econ.capex_incurred == pytest.approx(2000 * 2800 * 0.40)
    assert econ.asset_value == pytest.approx(2000 * 9500 * 0.40)


def test_material_quantities():
    econ = compute_economics(2000, RCC, T1, 40)
    assert econ.steel_tonnes == pytest.approx(8.0)
    assert econ.cement_bags == pytest.approx(840.0)


def test_structure_factor_applied():
    villa = compute_economics(1000, "Independent Villa", T1, 0)
    assert villa.total_budget == pytest.approx(1000 * 2800 * 1.30)


def test_milestones_reflect_completion():
    econ = compute_economics(2000, RCC, T1, 40)
    done = {m.name: m.done for m in econ.milestones}
    assert done == {"Foundation": True, "Superstructure": False,
                    "Finishing & MEP": False, "Handover": False}


@pytest.mark.parametrize("sqft", [100, 600_000])
def test_area_out_of_range_rejected(sqft):
    with pytest.raises(ValueError):
        compute_economics(sqft, RCC, T1, 10)


def test_unknown_structure_rejected():
    with pytest.raises(ValueError):
        compute_economics(1000, "Igloo", T1, 10)


def test_unknown_tier_rejected():
    with pytest.raises(ValueError):
        compute_economics(1000, RCC, "Tier 9", 10)


def test_completion_bounds_enforced():
    with pytest.raises(ValueError):
        compute_economics(1000, RCC, T1, 101)


@pytest.mark.parametrize(
    "amount, expected",
    [
        (5000, "₹5,000"),
        (2_240_000, "₹22.40 L"),
        (15_000_000, "₹1.50 Cr"),
    ],
)
def test_fmt_inr_uses_indian_units(amount, expected):
    assert fmt_inr(amount) == expected
