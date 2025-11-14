"""Gemini API client and query functions.

This module provides the core functionality for querying Gemini with URL context.
All functions raise exceptions rather than sys.exit() to remain CLI-independent.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os
from dataclasses import dataclass
from typing import Any

from google import genai
from google.genai import types


class GeminiClientError(Exception):
    """Base exception for Gemini client errors."""

    pass


class MissingApiKeyError(GeminiClientError):
    """Raised when GEMINI_API_KEY environment variable is not set."""

    pass


class QueryError(GeminiClientError):
    """Raised when a query to Gemini fails."""

    pass


@dataclass
class UrlMetadata:
    """Metadata about a URL retrieved during query."""

    retrieved_url: str
    url_retrieval_status: str


@dataclass
class QueryResult:
    """Result of a Gemini query with URL context."""

    response_text: str
    url_context_metadata: list[UrlMetadata] | None = None
    grounding_metadata: dict[str, Any] | None = None


class GeminiClient:
    """Client for interacting with the Gemini API."""

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize Gemini client.

        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY env var.

        Raises:
            MissingApiKeyError: If api_key is None and GEMINI_API_KEY is not set.
        """
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise MissingApiKeyError(
                "GEMINI_API_KEY environment variable is required.\n"
                "Set it with: export GEMINI_API_KEY='your-api-key'\n"
                "Get an API key from: https://aistudio.google.com/app/apikey"
            )

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def query(
        self,
        prompt: str,
        enable_search: bool = True,
        verbose: bool = False,
    ) -> QueryResult:
        """Query Gemini with URL context.

        Args:
            prompt: Query prompt that can include URLs
            enable_search: Whether to enable Google Search tool (default: True)
            verbose: Whether to include detailed metadata in result (default: False)

        Returns:
            QueryResult with response text and optional metadata

        Raises:
            QueryError: If the query fails
            ValueError: If prompt is empty
        """
        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty.\n"
                "Provide a prompt as argument:\n"
                "  gemini-url-context-tool query 'your prompt here'\n"
                "Or read from stdin:\n"
                "  echo 'your prompt' | gemini-url-context-tool query --stdin"
            )

        # Build tools list - using list[Any] to satisfy SDK's loose typing
        from typing import Any as AnyType

        tools: list[AnyType] = [types.Tool(url_context=types.UrlContext())]

        # Include Google Search tool unless disabled
        if enable_search:
            tools = [
                types.Tool(url_context=types.UrlContext()),
                types.Tool(google_search=types.GoogleSearch()),
            ]

        config = types.GenerateContentConfig(tools=tools)

        try:
            # Generate content
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
        except Exception as e:
            raise QueryError(
                f"Query failed: {str(e)}\n"
                "Check your API key and network connection.\n"
                "Verify API key is set: echo $GEMINI_API_KEY"
            ) from e

        # Extract response text
        response_text = ""
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                response_text = "".join(
                    str(part.text)
                    for part in candidate.content.parts
                    if hasattr(part, "text") and part.text is not None
                )

        # Extract URL context metadata
        url_metadata_list: list[UrlMetadata] | None = None
        if (
            response.candidates
            and len(response.candidates) > 0
            and hasattr(response.candidates[0], "url_context_metadata")
        ):
            url_context_metadata = response.candidates[0].url_context_metadata
            if url_context_metadata and hasattr(url_context_metadata, "url_metadata"):
                url_meta_attr = url_context_metadata.url_metadata
                if url_meta_attr:
                    url_metadata_list = [
                        UrlMetadata(
                            retrieved_url=getattr(url_meta, "retrieved_url", ""),
                            url_retrieval_status=getattr(
                                url_meta, "url_retrieval_status", "UNKNOWN"
                            ),
                        )
                        for url_meta in url_meta_attr
                    ]

        # Extract grounding metadata (if verbose and search enabled)
        grounding_dict: dict[str, Any] | None = None
        if verbose and enable_search:
            if (
                response.candidates
                and len(response.candidates) > 0
                and hasattr(response.candidates[0], "grounding_metadata")
            ):
                grounding_metadata = response.candidates[0].grounding_metadata
                grounding_dict = {}

                # Extract web search queries
                web_search_queries = getattr(grounding_metadata, "web_search_queries", [])
                if web_search_queries:
                    grounding_dict["web_search_queries"] = web_search_queries

                # Extract grounding chunks
                chunks = getattr(grounding_metadata, "grounding_chunks", [])
                if chunks:
                    chunks_list = []
                    for chunk in chunks:
                        chunk_dict: dict[str, Any] = {}
                        if hasattr(chunk, "web") and chunk.web:
                            chunk_dict["uri"] = getattr(chunk.web, "uri", None)
                            chunk_dict["title"] = getattr(chunk.web, "title", None)
                        elif hasattr(chunk, "uri"):
                            chunk_dict["uri"] = chunk.uri
                            chunk_dict["title"] = getattr(chunk, "title", None)
                        chunks_list.append(chunk_dict)
                    if chunks_list:
                        grounding_dict["grounding_chunks"] = chunks_list

                # Extract grounding supports
                supports = getattr(grounding_metadata, "grounding_supports", [])
                if supports:
                    supports_list = []
                    for support in supports:
                        segment = getattr(support, "segment", None)
                        chunk_indices = getattr(support, "grounding_chunk_indices", [])

                        if segment:
                            supports_list.append(
                                {
                                    "segment": {
                                        "start_index": getattr(segment, "start_index", None),
                                        "end_index": getattr(segment, "end_index", None),
                                        "text": getattr(segment, "text", ""),
                                    },
                                    "grounding_chunk_indices": chunk_indices,
                                }
                            )

                    if supports_list:
                        grounding_dict["grounding_supports"] = supports_list

                if not grounding_dict:
                    grounding_dict = None

        return QueryResult(
            response_text=response_text,
            url_context_metadata=url_metadata_list,
            grounding_metadata=grounding_dict,
        )


def query_with_url_context(
    prompt: str,
    api_key: str | None = None,
    enable_search: bool = True,
    verbose: bool = False,
) -> QueryResult:
    """Convenience function to query Gemini with URL context.

    Args:
        prompt: Query prompt that can include URLs
        api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
        enable_search: Whether to enable Google Search tool (default: True)
        verbose: Whether to include detailed metadata (default: False)

    Returns:
        QueryResult with response text and optional metadata

    Raises:
        MissingApiKeyError: If api_key is None and GEMINI_API_KEY not set
        QueryError: If the query fails
        ValueError: If prompt is empty

    Examples:
        >>> result = query_with_url_context("Analyze https://example.com")
        >>> print(result.response_text)

        >>> result = query_with_url_context(
        ...     "Compare URLs",
        ...     enable_search=False,
        ...     verbose=True
        ... )
    """
    client = GeminiClient(api_key=api_key)
    return client.query(prompt=prompt, enable_search=enable_search, verbose=verbose)
