"""Tests for utility functions.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import pytest

from gemini_url_context_tool.core.client import QueryResult, UrlMetadata
from gemini_url_context_tool.utils import format_output, validate_prompt


def test_validate_prompt_success() -> None:
    """Test that validate_prompt returns stripped prompt."""
    assert validate_prompt("  hello  ") == "hello"
    assert validate_prompt("test prompt") == "test prompt"


def test_validate_prompt_empty() -> None:
    """Test that validate_prompt raises ValueError for empty input."""
    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        validate_prompt("")

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        validate_prompt("   ")

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        validate_prompt(None)


def test_format_output_text_only() -> None:
    """Test format_output with text_only=True."""
    result = QueryResult(response_text="Hello World")
    output = format_output(result, text_only=True)
    assert output == "Hello World"


def test_format_output_json_basic() -> None:
    """Test format_output with basic JSON output."""
    result = QueryResult(response_text="Test response")
    output = format_output(result, text_only=False)

    # Should be valid JSON
    import json

    data = json.loads(output)
    assert data["response_text"] == "Test response"
    assert "url_context_metadata" not in data


def test_format_output_json_with_url_metadata() -> None:
    """Test format_output with URL metadata."""
    url_meta = UrlMetadata(
        retrieved_url="https://example.com",
        url_retrieval_status="URL_RETRIEVAL_STATUS_SUCCESS",
    )
    result = QueryResult(
        response_text="Test",
        url_context_metadata=[url_meta],
    )
    output = format_output(result, text_only=False)

    import json

    data = json.loads(output)
    assert data["response_text"] == "Test"
    assert "url_context_metadata" in data
    assert len(data["url_context_metadata"]) == 1
    assert data["url_context_metadata"][0]["retrieved_url"] == "https://example.com"


def test_format_output_json_with_grounding_metadata() -> None:
    """Test format_output with grounding metadata in verbose mode."""
    grounding_data = {
        "web_search_queries": ["test query"],
        "grounding_chunks": [{"uri": "https://example.com", "title": "Example"}],
    }
    result = QueryResult(
        response_text="Test",
        grounding_metadata=grounding_data,
    )
    output = format_output(result, text_only=False, verbose=True, search_enabled=True)

    import json

    data = json.loads(output)
    assert "grounding_metadata" in data
    assert data["grounding_metadata"]["web_search_queries"] == ["test query"]


def test_format_output_no_grounding_when_search_disabled() -> None:
    """Test that grounding metadata is not included when search is disabled."""
    grounding_data = {"web_search_queries": ["test"]}
    result = QueryResult(
        response_text="Test",
        grounding_metadata=grounding_data,
    )
    output = format_output(result, text_only=False, verbose=True, search_enabled=False)

    import json

    data = json.loads(output)
    assert "grounding_metadata" not in data
