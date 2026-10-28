"""Tab 3: planning, cost estimation, and real-estate valuation."""

import streamlit as st

from config.settings import (
    PROJECT_SQFT_MAX,
    PROJECT_SQFT_MIN,
    STRUCTURE_CONFIG,
    TIER_RATES,
)
from core.cost_engine import compute_economics
from core.formatting import fmt_inr
from core.llm_client import GeminiClient
from core.render_prompt import build_render_prompt, build_render_url
from ui.components import demo_banner, metric_card

RENDER_KEY = "render_url"


def render(_llm: GeminiClient) -> None:
    st.subheader("Project Planning & Real Estate Valuation")
    st.caption("Conceptual estimates in INR. Rates are planning assumptions, not quotations.")

    c1, c2 = st.columns(2)
    with c1:
        structure = st.selectbox("Structure type", list(STRUCTURE_CONFIG.keys()))
        sqft = st.number_input(
            "Built-up area (sq ft)",
            min_value=PROJECT_SQFT_MIN,
            max_value=PROJECT_SQFT_MAX,
            value=2000,
            step=100,
        )
    with c2:
        tier = st.selectbox("Location tier", list(TIER_RATES.keys()))
        pct = st.slider("Completion percentage", 0, 100, 40)

    try:
        econ = compute_economics(sqft, structure, tier, pct)
    except ValueError as exc:
        st.error(str(exc))
        return

    st.markdown("#### Financial summary")
    m1, m2, m3 = st.columns(3)
    with m1:
        metric_card("Total project budget", fmt_inr(econ.total_budget))
    with m2:
        metric_card("Capex incurred", fmt_inr(econ.capex_incurred))
    with m3:
        metric_card("Current asset valuation", fmt_inr(econ.asset_value))

    st.markdown("#### Material requirements")
    m4, m5 = st.columns(2)
    with m4:
        metric_card("Steel required", f"{econ.steel_tonnes:,.2f} tonnes")
    with m5:
        metric_card("Cement required", f"{econ.cement_bags:,.0f} bags (50 kg)")

    st.markdown("#### Milestone progress")
    st.progress(pct / 100)
    for milestone in econ.milestones:
        mark = "✅" if milestone.done else "⬜"
        st.markdown(f"{mark} {milestone.name} ({milestone.threshold}%)")

    st.markdown("#### Conceptual 3D rendering")
    if st.button("Generate concept rendering", key="render_btn"):
        prompt = build_render_prompt(structure, sqft, tier)
        st.session_state[RENDER_KEY] = build_render_url(prompt)

    if st.session_state.get(RENDER_KEY):
        st.image(
            st.session_state[RENDER_KEY],
            caption="Concept rendering (Pollinations AI)",
            use_container_width=True,
        )
        st.caption("Illustrative only. Not an engineering or architectural drawing.")
