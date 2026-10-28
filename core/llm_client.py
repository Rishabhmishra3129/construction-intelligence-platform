"""Gemini wrapper with graceful demonstration-mode fallback.

Uses the google-genai SDK (the successor to google-generativeai). This module
has no Streamlit dependency, so it can be unit tested directly.
"""

import copy
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from config.prompts import CHAT_SYSTEM_PROMPT
from config.settings import CHAT_HISTORY_TURNS, MODEL_NAME
from core.parsing import parse_json_response, require_keys

try:
    from google import genai
    from google.genai import types

    GENAI_AVAILABLE = True
except ImportError:  # the app still runs in demonstration mode
    genai = None
    types = None
    GENAI_AVAILABLE = False

logger = logging.getLogger(__name__)


class LLMError(RuntimeError):
    """A live model call failed."""


@dataclass(frozen=True)
class AnalysisResult:
    data: Dict[str, Any]
    is_demo: bool
    error: Optional[str] = None


def build_chat_prompt(history: Sequence[Dict[str, str]], weather: str) -> str:
    recent = list(history)[-CHAT_HISTORY_TURNS:]
    transcript = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in recent)
    return (
        f"{CHAT_SYSTEM_PROMPT}\nCurrent site weather: {weather}.\n\n"
        f"Conversation so far:\n{transcript}\n\nAssistant:"
    )


class GeminiClient:
    def __init__(self, api_key: str, model_name: str = MODEL_NAME, client: Any = None) -> None:
        """
        api_key: user-supplied key. Empty means demonstration mode.
        client:  optional pre-built client (used by tests to inject a fake).
        """
        self.api_key = (api_key or "").strip()
        self.model_name = model_name
        self.init_error: Optional[str] = None
        self._client = client

        if self._client is None and self.api_key and GENAI_AVAILABLE:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception as exc:
                logger.exception("Gemini initialisation failed")
                self.init_error = str(exc)

    @property
    def ready(self) -> bool:
        """True when a live model client is configured."""
        return self._client is not None

    @property
    def mode_label(self) -> str:
        return "Live (Gemini connected)" if self.ready else "Demonstration mode"

    def _generate(self, contents: Any, config: Any = None) -> str:
        response = self._client.models.generate_content(
            model=self.model_name, contents=contents, config=config
        )
        return (response.text or "").strip()

    def analyse_image_json(
        self,
        prompt: str,
        image: Any,
        demo_payload: Dict[str, Any],
        required_keys: Sequence[str],
    ) -> AnalysisResult:
        """Send an image and prompt to the model and return validated JSON.

        Any failure falls back to the demo payload and reports the reason.
        """
        if not self.ready:
            return AnalysisResult(copy.deepcopy(demo_payload), is_demo=True)

        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json", temperature=0.2
            ) if types else None
            text = self._generate([prompt, image], config)
            data = require_keys(parse_json_response(text), required_keys, "Model")
            return AnalysisResult(data, is_demo=False)
        except Exception as exc:
            logger.exception("Vision analysis failed")
            return AnalysisResult(
                copy.deepcopy(demo_payload),
                is_demo=True,
                error=f"Live analysis failed ({exc}). Showing demonstration output.",
            )

    def chat(self, history: List[Dict[str, str]], weather: str) -> Optional[str]:
        """Return the model's reply, or None when running in demonstration mode.

        Raises LLMError if a live call fails.
        """
        if not self.ready:
            return None
        try:
            config = types.GenerateContentConfig(temperature=0.4) if types else None
            text = self._generate(build_chat_prompt(history, weather), config)
        except Exception as exc:
            logger.exception("Chat request failed")
            raise LLMError(str(exc)) from exc

        if not text:
            raise LLMError("the model returned an empty reply")
        return text
