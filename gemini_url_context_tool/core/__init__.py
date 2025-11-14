"""Core library functions for Gemini URL context queries.

This module contains the core business logic independent of CLI.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from gemini_url_context_tool.core.client import (
    GeminiClient,
    QueryResult,
    UrlMetadata,
    query_with_url_context,
)

__all__ = [
    "GeminiClient",
    "QueryResult",
    "UrlMetadata",
    "query_with_url_context",
]
