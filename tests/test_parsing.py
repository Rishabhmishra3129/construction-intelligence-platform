import pytest

from core.parsing import ParsingError, parse_json_response, require_keys


def test_parses_plain_json():
    assert parse_json_response('{"a": 1}') == {"a": 1}


def test_strips_markdown_fences_and_prose():
    text = 'Here you go:\n```json\n{"safety_score": 70}\n```\nDone.'
    assert parse_json_response(text) == {"safety_score": 70}


def test_empty_response_raises():
    with pytest.raises(ParsingError):
        parse_json_response("   ")


def test_no_object_raises():
    with pytest.raises(ParsingError):
        parse_json_response("no json here")


def test_invalid_json_raises():
    with pytest.raises(ParsingError):
        parse_json_response('{"a": }')


def test_non_object_json_raises():
    with pytest.raises(ParsingError):
        parse_json_response("[1, 2]")


def test_require_keys_reports_missing_fields():
    with pytest.raises(ParsingError, match="hazards"):
        require_keys({"safety_score": 1}, ("safety_score", "hazards"), "PPE")
