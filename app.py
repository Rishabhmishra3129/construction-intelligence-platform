"""Application entry point.

Run locally with:  streamlit run app.py
"""

import logging

import streamlit as st

from config.settings import APP_ICON, APP_TITLE
from core.llm_client import GeminiClient
from ui import tab_assistant, tab_crack, tab_planning, tab_ppe
from ui.components import esc
from ui.sidebar import render_sidebar
from ui.styles import CSS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero"><h1>{APP_ICON} {esc(APP_TITLE)}</h1>'
        "<p>Multimodal AI for site safety, structural diagnostics, project economics, "
        "and daily operations.</p></div>",
        unsafe_allow_html=True,
    )

    api_key = render_sidebar()
    llm = GeminiClient(api_key)
    if llm.init_error:
        st.sidebar.error(f"Gemini could not be initialised: {llm.init_error}")

    tabs = st.tabs(["🦺 Site Safety & PPE", "🧱 Crack Diagnostics", "📐 Planning & Valuation", "🌦️ Daily Site Assistant"])
    with tabs[0]:
        tab_ppe.render(llm)
    with tabs[1]:
        tab_crack.render(llm)
    with tabs[2]:
        tab_planning.render(llm)
    with tabs[3]:
        tab_assistant.render(llm)


if __name__ == "__main__":
    try:
        main()
    except Exception:  # last-resort guard so users never see a raw traceback
        logging.exception("Unhandled application error")
        st.error("Something went wrong while rendering the page. Please refresh and try again.")
