"""Query command implementation for CLI.

This module provides the CLI wrapper for querying Gemini with URL context.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from gemini_url_context_tool.core.client import (
    GeminiClientError,
    MissingApiKeyError,
    QueryError,
)
from gemini_url_context_tool.core.client import query_with_url_context as core_query
from gemini_url_context_tool.utils import format_output, read_stdin


@click.command()
@click.argument("prompt", required=False)
@click.option(
    "--stdin",
    "-s",
    is_flag=True,
    help="Read prompt from stdin for pipeline integration",
)
@click.option(
    "--no-search-tool",
    is_flag=True,
    default=False,
    help="Disable Google Search tool (URL context only)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Include detailed metadata (url_context_metadata and grounding_metadata)",
)
@click.option(
    "--text",
    "-t",
    is_flag=True,
    help="Output plain text instead of JSON",
)
def query(
    prompt: str | None,
    stdin: bool,
    no_search_tool: bool,
    verbose: bool,
    text: bool,
) -> None:
    """Query Gemini with URL context tool.

    URLs can be included directly in the prompt text. The model will automatically
    extract and retrieve content from those URLs.

    \b
    Examples:

    \b
    # Basic query with URLs in prompt
    gemini-url-context-tool query "Compare recipes from https://example.com/recipe1 and https://example.com/recipe2"

    \b
    # Read prompt from stdin (pipeline integration)
    echo "Analyze https://example.com/article.pdf" | gemini-url-context-tool query --stdin

    \b
    # Disable Google Search (URL context only)
    gemini-url-context-tool query "Extract pricing from https://example.com/pricing" \\
        --no-search-tool

    \b
    # Get verbose output with metadata
    gemini-url-context-tool query "Summarize https://example.com/doc" --verbose

    \b
    # Output plain text instead of JSON
    gemini-url-context-tool query "What are the key points in https://example.com/article" --text

    \b
    # Combine multiple options
    gemini-url-context-tool query "Analyze https://example.com" \\
        --no-search-tool \\
        --verbose \\
        --text

    \b
    Output Format (default JSON):
        {
          "response_text": "The model's response...",
          "url_context_metadata": [
            {
              "retrieved_url": "https://example.com",
              "url_retrieval_status": "URL_RETRIEVAL_STATUS_SUCCESS"
            }
          ],
          "grounding_metadata": {...}  // Only with --verbose and search enabled
        }

    \b
    Output Format (with --text):
        Plain text response only, no JSON structure.
    """
    # Validate prompt source
    if stdin and prompt:
        click.echo(
            "Error: Cannot specify both PROMPT argument and --stdin flag.\n"
            "Choose one:\n"
            "  gemini-url-context-tool query 'your prompt'\n"
            "  echo 'your prompt' | gemini-url-context-tool query --stdin",
            err=True,
        )
        sys.exit(1)

    # Get prompt from stdin or argument
    if stdin:
        try:
            prompt = read_stdin()
        except ValueError as e:
            click.echo(f"Error: {str(e)}", err=True)
            sys.exit(1)
    elif not prompt:
        click.echo(
            "Error: PROMPT argument is required.\n"
            "Provide a prompt:\n"
            "  gemini-url-context-tool query 'your prompt here'\n"
            "Or read from stdin:\n"
            "  echo 'your prompt' | gemini-url-context-tool query --stdin\n"
            "For help:\n"
            "  gemini-url-context-tool query --help",
            err=True,
        )
        sys.exit(1)

    # Log verbose info
    if verbose:
        model = "gemini-2.5-flash"
        click.echo(
            f"[INFO] Querying with model '{model}' and URL context tool",
            err=True,
        )
        if not no_search_tool:
            click.echo("[INFO] Google Search tool enabled", err=True)
        else:
            click.echo("[INFO] Google Search tool disabled", err=True)

    # Execute query
    try:
        result = core_query(
            prompt=prompt,
            enable_search=not no_search_tool,
            verbose=verbose,
        )

        if verbose:
            click.echo("[INFO] Query completed successfully", err=True)

        # Format and output result
        output = format_output(
            result=result,
            text_only=text,
            verbose=verbose,
            search_enabled=not no_search_tool,
        )
        click.echo(output)

    except MissingApiKeyError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except QueryError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except GeminiClientError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(
            f"Error: Unexpected error: {str(e)}\n"
            "This may be a bug. Please report at:\n"
            "  https://github.com/dnvriend/gemini-url-context-tool/issues",
            err=True,
        )
        sys.exit(1)
