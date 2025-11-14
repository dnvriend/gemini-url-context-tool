"""Utility functions for gemini-url-context-tool.

This module provides shared utilities for output formatting, input validation,
and stdin handling.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import sys
from typing import Any

from gemini_url_context_tool.core.client import QueryResult


def read_stdin() -> str:
    """Read prompt from stdin.

    Returns:
        The prompt text from stdin

    Raises:
        ValueError: If stdin is empty or only whitespace

    Examples:
        >>> prompt = read_stdin()
        >>> print(f"Got prompt: {prompt}")
    """
    if sys.stdin.isatty():
        raise ValueError(
            "No input from stdin.\n"
            "Pipe input to the command:\n"
            "  echo 'your prompt' | gemini-url-context-tool query --stdin\n"
            "Or provide prompt as argument:\n"
            "  gemini-url-context-tool query 'your prompt'"
        )

    prompt = sys.stdin.read()

    if not prompt or not prompt.strip():
        raise ValueError(
            "Stdin input is empty.\n"
            "Provide non-empty input:\n"
            "  echo 'your prompt' | gemini-url-context-tool query --stdin"
        )

    return prompt.strip()


def format_output(
    result: QueryResult,
    text_only: bool = False,
    verbose: bool = False,
    search_enabled: bool = True,
) -> str:
    """Format query result for output.

    Args:
        result: The QueryResult to format
        text_only: If True, return only response_text as plain text
        verbose: If True, include all metadata in JSON output
        search_enabled: Whether Google Search was enabled (affects metadata)

    Returns:
        Formatted output string (JSON or plain text)

    Examples:
        >>> result = QueryResult(response_text="Hello")
        >>> output = format_output(result, text_only=True)
        >>> print(output)
        Hello

        >>> output = format_output(result, text_only=False)
        >>> print(output)
        {"response_text": "Hello", ...}
    """
    if text_only:
        return result.response_text

    # Build JSON output
    output: dict[str, Any] = {
        "response_text": result.response_text,
    }

    # Always include URL context metadata if available
    if result.url_context_metadata:
        output["url_context_metadata"] = [
            {
                "retrieved_url": url_meta.retrieved_url,
                "url_retrieval_status": url_meta.url_retrieval_status,
            }
            for url_meta in result.url_context_metadata
        ]

    # Include grounding metadata if verbose and search was enabled
    if verbose and search_enabled and result.grounding_metadata:
        output["grounding_metadata"] = result.grounding_metadata

    return json.dumps(output, indent=2)


def validate_prompt(prompt: str | None) -> str:
    """Validate that prompt is non-empty.

    Args:
        prompt: The prompt to validate

    Returns:
        The validated prompt (stripped of whitespace)

    Raises:
        ValueError: If prompt is None, empty, or only whitespace

    Examples:
        >>> prompt = validate_prompt("  hello  ")
        >>> print(prompt)
        hello

        >>> validate_prompt("")
        ValueError: Prompt cannot be empty
    """
    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty.\n"
            "Provide a prompt:\n"
            "  gemini-url-context-tool query 'your prompt here'\n"
            "Or read from stdin:\n"
            "  echo 'your prompt' | gemini-url-context-tool query --stdin"
        )

    return prompt.strip()
