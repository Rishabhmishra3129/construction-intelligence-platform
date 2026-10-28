"""Sample outputs for demonstration mode, plus an offline chatbot fallback."""

from typing import Any, Dict

DEMO_PPE: Dict[str, Any] = {
    "safety_score": 62,
    "overall_status": "Partially Compliant",
    "workers_detected": 4,
    "ppe_detection": {
        "helmet": "Compliant",
        "high_vis_vest": "Non-Compliant",
        "steel_toe_boots": "Compliant",
        "safety_harness": "Non-Compliant",
    },
    "hazards": [
        {
            "description": "Worker at roof edge without fall-arrest harness or guardrail.",
            "severity": "Critical",
            "corrective_remedy": "Stop work at the edge, install guardrails, and issue a harness with a certified anchor point.",
            "standard_reference": "OSHA 1926.501 / IS 3764",
        },
        {
            "description": "Exposed reinforcement bars at ground level without caps.",
            "severity": "High",
            "corrective_remedy": "Fit protective rebar caps and mark the zone with barricade tape.",
            "standard_reference": "OSHA 1926.701(a)",
        },
        {
            "description": "Scattered tools and debris on the access path.",
            "severity": "Low",
            "corrective_remedy": "Assign housekeeping duty and clear the walkway each shift.",
            "standard_reference": "OSHA 1926.25",
        },
    ],
}

DEMO_CRACK: Dict[str, Any] = {
    "defect_type": "Structural Shear",
    "estimated_crack_width_mm": 1.8,
    "severity_score": 68,
    "confidence": "Medium",
    "observations": [
        "Diagonal crack initiating near a window opening corner.",
        "Crack width appears to vary along its length.",
    ],
    "root_causes": [
        "Shear stress concentration at an unreinforced opening corner.",
        "Possible differential loading from an adjacent structure.",
    ],
    "recommended_repairs": [
        "Epoxy injection of the crack after surface preparation.",
        "Structural re-grouting and installation of diagonal GFRP strips.",
        "Monitor crack width with a crack gauge for three months.",
    ],
    "urgency": "Planned",
    "engineer_review_required": True,
}


def offline_chat_reply(question: str, weather: str) -> str:
    """Canned IS 456-based answers used when no live model is available."""
    q = question.lower()
    if "cur" in q:
        return (
            "**Concrete curing (IS 456):** keep the surface continuously moist for at least 7 days, "
            "or 10 days for mixes with mineral admixtures or in dry, hot conditions. "
            "Use wet hessian, ponding, or a curing compound."
        )
    if "shor" in q or "formwork" in q:
        return (
            "**Formwork and shoring:** do not strip shuttering until the concrete reaches adequate strength "
            "(typically 14 days for slabs with props retained, per IS 456). "
            "Inspect props for plumbness, bracing, and base plates before every pour."
        )
    if "mix" in q or "grade" in q:
        return (
            "**Mix design:** M20 suits general residential RCC, M25 most framed structures, "
            "and M30 and above for heavily loaded or exposed members. Confirm with trial batches and cube tests."
        )
    if "safe" in q or "ppe" in q:
        return (
            "**Site safety:** enforce helmets, high-visibility vests, and steel-toe boots at all times. "
            "Use fall-arrest harnesses above 2 m, and hold a toolbox talk at the start of each shift."
        )
    return (
        f"With today's weather set to **{weather}**, follow the protocol alerts above. "
        "Ask about curing, shoring, mix design, or site safety for detailed guidance. "
        "Add a Gemini API key in the sidebar for open-ended answers."
    )
