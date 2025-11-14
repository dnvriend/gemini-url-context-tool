"""CLI entry point for gemini-url-context-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from gemini_url_context_tool.commands import query


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """A CLI for querying Gemini with URL context.

    Query Gemini with URLs embedded in your prompts. The model automatically
    extracts and retrieves content from those URLs for analysis.

    \b
    Examples:

    \b
    # Query with URLs in prompt
    gemini-url-context-tool query "Compare https://example.com/page1 and https://example.com/page2"

    \b
    # Read from stdin
    echo "Analyze https://example.com/doc.pdf" | gemini-url-context-tool query --stdin

    \b
    # Get plain text output
    gemini-url-context-tool query "Summarize https://example.com" --text

    \b
    For detailed help on any command:
        gemini-url-context-tool query --help
    """
    pass


# Register commands
main.add_command(query)


if __name__ == "__main__":
    main()
