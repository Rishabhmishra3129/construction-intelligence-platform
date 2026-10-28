"""Turn raw model text into validated Python dictionaries."""

import json
import re
from typing import Any, Dict, Iterable

_FENCE_RE = re.compile(r"```(?:json)?", re.IGNORECASE)


class ParsingError(ValueError):
    """The model output could not be used as structured data."""


def parse_json_response(text: str) -> Dict[str, Any]:
    """Extract the first JSON object from model output, tolerating markdown fences and prose."""
    if not text or not text.strip():
        raise ParsingError("The model returned an empty response.")

    cleaned = _FENCE_RE.sub("", text).strip()
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end <= start:
        raise ParsingError("The model response did not contain a JSON object.")

    try:
        data = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError as exc:
        raise ParsingError(f"Invalid JSON from the model: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ParsingError("The model returned JSON, but not an object.")
    return data


def require_keys(data: Dict[str, Any], keys: Iterable[str], label: str) -> Dict[str, Any]:
    """Raise ParsingError if any required top-level field is absent."""
    missing = [key for key in keys if key not in data]
    if missing:
        raise ParsingError(f"{label} response is missing fields: {', '.join(missing)}.")
    return data
