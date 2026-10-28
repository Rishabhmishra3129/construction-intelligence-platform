import pytest
from core.demo_data import DEMO_PPE
from core.llm_client import GeminiClient, build_chat_prompt
from config.settings import PPE_REQUIRED_KEYS


def test_no_key_means_demonstration_mode():
    llm = GeminiClient("")
    assert not llm.ready
    assert llm.mode_label == "Demonstration mode"


def test_demo_analysis_returns_copy_not_shared_state():
    llm = GeminiClient("")
    result = llm.analyse_image_json("prompt", object(), DEMO_PPE, PPE_REQUIRED_KEYS)
    assert result.is_demo
    assert result.error is None
    result.data["safety_score"] = 0
    assert DEMO_PPE["safety_score"] == 62  # the shared demo payload is untouched


def test_offline_chat_returns_none():
    assert GeminiClient("").chat([{"role": "user", "content": "hi"}], "Normal") is None


def test_chat_prompt_includes_weather_and_recent_turns_only():
    history = [{"role": "user", "content": f"msg {i}"} for i in range(30)]
    prompt = build_chat_prompt(history, "Heavy Rain")
    assert "Heavy Rain" in prompt
    assert "msg 29" in prompt
    assert "msg 0\n" not in prompt


class _FakeResponse:
    def __init__(self, text):
        self.text = text


class _FakeModels:
    def __init__(self, reply=None, error=None):
        self.reply, self.error, self.calls = reply, error, []

    def generate_content(self, model, contents, config=None):
        self.calls.append({"model": model, "contents": contents, "config": config})
        if self.error:
            raise self.error
        return _FakeResponse(self.reply)


class _FakeClient:
    def __init__(self, reply=None, error=None):
        self.models = _FakeModels(reply, error)


def test_live_analysis_parses_model_json():
    fake = _FakeClient(reply='```json\n{"safety_score": 90, "overall_status": "Compliant", '
                             '"ppe_detection": {}, "hazards": []}\n```')
    llm = GeminiClient("key", client=fake)
    assert llm.ready and llm.mode_label.startswith("Live")
    result = llm.analyse_image_json("p", object(), DEMO_PPE, PPE_REQUIRED_KEYS)
    assert not result.is_demo and result.error is None
    assert result.data["safety_score"] == 90
    assert fake.models.calls[0]["model"] == llm.model_name


def test_live_analysis_falls_back_on_bad_json():
    llm = GeminiClient("key", client=_FakeClient(reply="sorry, no json"))
    result = llm.analyse_image_json("p", object(), DEMO_PPE, PPE_REQUIRED_KEYS)
    assert result.is_demo
    assert "Live analysis failed" in result.error


def test_live_analysis_falls_back_on_missing_fields():
    llm = GeminiClient("key", client=_FakeClient(reply='{"safety_score": 10}'))
    result = llm.analyse_image_json("p", object(), DEMO_PPE, PPE_REQUIRED_KEYS)
    assert result.is_demo and "missing fields" in result.error


def test_live_chat_returns_reply():
    llm = GeminiClient("key", client=_FakeClient(reply="Keep it moist for 7 days."))
    assert llm.chat([{"role": "user", "content": "curing?"}], "Extreme Heat") == "Keep it moist for 7 days."


def test_live_chat_error_raises_llm_error():
    from core.llm_client import LLMError
    llm = GeminiClient("key", client=_FakeClient(error=RuntimeError("quota exceeded")))
    with pytest.raises(LLMError, match="quota"):
        llm.chat([{"role": "user", "content": "hi"}], "Normal")
