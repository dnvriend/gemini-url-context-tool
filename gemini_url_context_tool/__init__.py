"""gemini-url-context-tool: A CLI for querying Gemini with URL context.

This package provides both a CLI tool and a library for querying Google's Gemini
models with URL context, allowing the model to access and analyze content from
URLs provided in prompts.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from gemini_url_context_tool.core.client import (
    GeminiClient,
    GeminiClientError,
    MissingApiKeyError,
    QueryError,
    QueryResult,
    UrlMetadata,
    query_with_url_context,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "GeminiClient",
    "GeminiClientError",
    "MissingApiKeyError",
    "QueryError",
    "QueryResult",
    "UrlMetadata",
    "query_with_url_context",
]
