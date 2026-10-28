"""Reusable HTML and Streamlit widgets. All model-supplied text is HTML-escaped."""

import html
from typing import Any, List

import streamlit as st

from config.settings import SEVERITY_LEVELS


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def as_list(value: Any) -> List[str]:
    """Normalise a model field that should be a list of strings."""
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [str(value)] if value else []


def metric_card(label: str, value: Any) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="label">{esc(label)}</div>'
        f'<div class="value">{esc(value)}</div></div>',
        unsafe_allow_html=True,
    )


def status_pill(status: str) -> str:
    s = status.lower()
    if s.startswith("compliant"):
        css = "pill-safe"
    elif "partial" in s:
        css = "pill-warn"
    else:
        css = "pill-danger"
    return f'<span class="pill {css}">{esc(status)}</span>'


def severity_badge(severity: str) -> str:
    level = severity if severity in SEVERITY_LEVELS else "Low"
    return f'<span class="sev sev-{level}">{level}</span>'


def alert(message: str, kind: str = "danger") -> None:
    css = {"info": "alert alert-info", "warn": "alert alert-warn"}.get(kind, "alert")
    st.markdown(f'<div class="{css}">{esc(message)}</div>', unsafe_allow_html=True)


def demo_banner(is_demo: bool) -> None:
    if is_demo:
        st.info(
            "Demonstration mode: showing sample output. "
            "Add a Gemini API key in the sidebar for live analysis."
        )
