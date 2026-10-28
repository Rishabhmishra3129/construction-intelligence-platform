"""Tab 4: weather-aware protocols and the multi-turn site engineering assistant."""

import streamlit as st

from config.settings import CHAT_HISTORY_TURNS, WEATHER_OPTIONS
from core.demo_data import offline_chat_reply
from core.llm_client import GeminiClient, LLMError
from core.weather import WEATHER_PROTOCOLS
from ui.components import alert

CHAT_KEY = "chat_history"


def render(llm: GeminiClient) -> None:
    st.subheader("Daily Site Assistant & Weather-Aware Advisory")

    weather = st.selectbox("Today's site weather", WEATHER_OPTIONS)
    st.markdown("#### Protocol alerts")
    for item in WEATHER_PROTOCOLS[weather]:
        alert(item.message, kind="danger" if item.level == "danger" else "info")

    st.markdown("---")
    st.markdown("#### Construction engineering assistant")
    st.button(
        "Clear conversation",
        key="clear_chat",
        on_click=lambda: st.session_state.pop(CHAT_KEY, None),
    )

    history = st.session_state.setdefault(CHAT_KEY, [])
    for message in history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask about curing, shoring, mix design, or safety...")
    if not question:
        return

    history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    reply = _reply(llm, history, question, weather)
    history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)


def _reply(llm: GeminiClient, history, question: str, weather: str) -> str:
    try:
        live = llm.chat(history[-CHAT_HISTORY_TURNS:], weather)
    except LLMError as exc:
        return f"The live model is unavailable right now ({exc}). Please try again shortly."
    return live if live is not None else offline_chat_reply(question, weather)
