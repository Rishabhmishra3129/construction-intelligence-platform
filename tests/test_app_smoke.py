"""Runs the full Streamlit script headlessly to catch wiring errors across all tabs."""

from pathlib import Path

import pytest

apptest = pytest.importorskip("streamlit.testing.v1")

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def _run():
    return apptest.AppTest.from_file(APP, default_timeout=30).run()


def test_app_renders_without_exceptions_in_demo_mode():
    at = _run()
    assert not at.exception
    assert len(at.tabs) == 4


def test_planning_tab_shows_financial_metrics():
    at = _run()
    assert not at.exception
    assert any("Total project budget" in m.value for m in at.markdown)
