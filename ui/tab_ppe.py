"""Tab 1: site safety and PPE audit."""

import json

import streamlit as st

from config.prompts import PPE_PROMPT
from config.settings import PPE_REQUIRED_KEYS, SEVERITY_LEVELS
from core.demo_data import DEMO_PPE
from core.images import ImageLoadError, load_image
from core.llm_client import GeminiClient
from ui.components import as_list, demo_banner, esc, metric_card, severity_badge, status_pill, alert

STATE_KEY = "ppe_result"
_ICONS = {"Compliant": "✅", "Non-Compliant": "❌"}


def render(llm: GeminiClient) -> None:
    st.subheader("Site Safety & PPE Audit")
    st.caption("Checks helmets, high-visibility vests, steel-toe boots and harnesses against OSHA and IS 456 practice.")

    upload = st.file_uploader("Upload a site photo", type=["jpg", "jpeg", "png"], key="ppe_upload")
    if upload is None:
        st.info("Upload a JPG or PNG site photo to begin.")
        st.session_state.pop(STATE_KEY, None)
        return

    try:
        image = load_image(upload)
    except ImageLoadError as exc:
        st.error(str(exc))
        return

    st.image(image, caption="Uploaded site photo", use_container_width=True)

    if st.button("Run PPE audit", type="primary", key="ppe_run"):
        with st.spinner("Analysing PPE compliance and site hazards..."):
            result = llm.analyse_image_json(PPE_PROMPT, image, DEMO_PPE, PPE_REQUIRED_KEYS)
        st.session_state[STATE_KEY] = (upload.name, result)

    stored = st.session_state.get(STATE_KEY)
    if not stored or stored[0] != upload.name:
        return
    result = stored[1]

    if result.error:
        st.warning(result.error)
    demo_banner(result.is_demo)
    _render_result(result.data)


def _render_result(data: dict) -> None:
    score = int(data.get("safety_score", 0) or 0)
    score = min(max(score, 0), 100)
    hazards = [h for h in data.get("hazards", []) if isinstance(h, dict)]

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Safety score", f"{score}/100")
    with c2:
        metric_card("Workers detected", data.get("workers_detected", "—"))
    with c3:
        metric_card("Hazards found", len(hazards))

    st.markdown(
        f"**Overall status:** {status_pill(str(data.get('overall_status', 'Unknown')))}",
        unsafe_allow_html=True,
    )
    st.progress(score / 100)

    st.markdown("#### PPE checklist")
    ppe = data.get("ppe_detection", {}) if isinstance(data.get("ppe_detection"), dict) else {}
    if ppe:
        cols = st.columns(len(ppe))
        for col, (item, state) in zip(cols, ppe.items()):
            with col:
                icon = _ICONS.get(state, "➖")
                st.markdown(f"{icon} **{item.replace('_', ' ').title()}**  \n{esc(state)}")

    st.markdown("#### Identified hazards")
    if not hazards:
        st.success("No hazards identified in this image.")
    order = {level: i for i, level in enumerate(SEVERITY_LEVELS)}
    for hz in sorted(hazards, key=lambda h: order.get(h.get("severity"), len(order))):
        st.markdown(
            f'<div class="alert">{severity_badge(hz.get("severity", "Low"))}'
            f'<strong>{esc(hz.get("description", ""))}</strong><br>'
            f'<em>Remedy:</em> {esc(hz.get("corrective_remedy", ""))}<br>'
            f'<small>Reference: {esc(hz.get("standard_reference", "—"))}</small></div>',
            unsafe_allow_html=True,
        )

    st.download_button(
        "⬇️ Download JSON report",
        data=json.dumps(data, indent=2),
        file_name="ppe_audit_report.json",
        mime="application/json",
    )
