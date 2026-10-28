"""Tab 2: crack diagnostics and structural integrity."""

import json

import streamlit as st

from config.prompts import CRACK_PROMPT
from config.settings import CRACK_REQUIRED_KEYS
from core.demo_data import DEMO_CRACK
from core.images import ImageLoadError, load_image
from core.llm_client import GeminiClient
from ui.components import alert, as_list, demo_banner, esc, metric_card

STATE_KEY = "crack_result"


def render(llm: GeminiClient) -> None:
    st.subheader("Crack Diagnostics & Structural Integrity")
    st.caption("Classifies the defect, estimates crack width, and recommends engineering repairs.")

    upload = st.file_uploader(
        "Upload a concrete or wall surface photo", type=["jpg", "jpeg", "png"], key="crack_upload"
    )
    if upload is None:
        st.info("Upload a photo of the affected surface to begin.")
        st.session_state.pop(STATE_KEY, None)
        return

    try:
        image = load_image(upload)
    except ImageLoadError as exc:
        st.error(str(exc))
        return

    st.image(image, caption="Uploaded surface", use_container_width=True)

    if st.button("Analyse defect", type="primary", key="crack_run"):
        with st.spinner("Classifying defect and estimating crack width..."):
            result = llm.analyse_image_json(CRACK_PROMPT, image, DEMO_CRACK, CRACK_REQUIRED_KEYS)
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
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Defect type", data.get("defect_type", "—"))
    with c2:
        metric_card("Crack width", f"{data.get('estimated_crack_width_mm', '—')} mm")
    with c3:
        metric_card("Severity", f"{data.get('severity_score', '—')}/100")
    with c4:
        metric_card("Urgency", data.get("urgency", "—"))

    if data.get("urgency") in ("Urgent", "Immediate"):
        alert("Urgent defect: restrict loading and occupation until a structural engineer has inspected it.")
    elif data.get("engineer_review_required"):
        alert("A licensed structural engineer should review this defect before further loading.", kind="warn")

    st.markdown(f"**Model confidence:** {esc(data.get('confidence', '—'))}")

    left, right = st.columns(2)
    with left:
        st.markdown("#### Observations")
        for item in as_list(data.get("observations")):
            st.markdown(f"- {esc(item)}")
        st.markdown("#### Root causes")
        for item in as_list(data.get("root_causes")):
            st.markdown(f"- {esc(item)}")
    with right:
        st.markdown("#### Recommended engineering repairs")
        for item in as_list(data.get("recommended_repairs")):
            st.markdown(f"- {esc(item)}")

    st.download_button(
        "⬇️ Download diagnostic report",
        data=json.dumps(data, indent=2),
        file_name="crack_diagnostic_report.json",
        mime="application/json",
    )
