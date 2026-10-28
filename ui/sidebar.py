"""Sidebar: API key entry, mode indicator, navigation, and architecture notes."""

import streamlit as st

from config.settings import MODEL_NAME
from core.llm_client import GENAI_AVAILABLE


def _secret_key() -> str:
    try:
        return str(st.secrets.get("GEMINI_API_KEY", "") or "")
    except Exception:  # no secrets.toml present is normal in local development
        return ""


def render_sidebar() -> str:
    """Render the sidebar and return the API key entered (or empty string)."""
    st.sidebar.header("⚙️ Configuration")

    if "api_key" not in st.session_state:
        st.session_state["api_key"] = _secret_key()

    st.sidebar.text_input(
        "Google Gemini API key",
        type="password",
        key="api_key",
        help="Held in this browser session only. Leave blank for demonstration mode.",
    )
    key = st.session_state.get("api_key", "").strip()

    if key and GENAI_AVAILABLE:
        st.sidebar.success(f"Live mode: {MODEL_NAME}")
    elif key:
        st.sidebar.error("Install google-generativeai to enable live mode.")
    else:
        st.sidebar.warning("Demonstration mode: no API key")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🧭 Navigation")
    st.sidebar.markdown(
        "- **Tab 1:** Site safety and PPE audit\n"
        "- **Tab 2:** Crack diagnostics\n"
        "- **Tab 3:** Planning and valuation\n"
        "- **Tab 4:** Daily site assistant"
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("🏛️ Architecture")
    st.sidebar.markdown(
        "Streamlit UI → Gemini multimodal model → strict JSON contracts "
        "→ deterministic cost engine (INR). Pollinations AI renders concepts. "
        "No external database."
    )
    return key
