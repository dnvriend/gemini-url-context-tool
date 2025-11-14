# gemini-url-context-tool - Developer Guide

## Overview

`gemini-url-context-tool` is a production-ready CLI and library for querying Google's Gemini models with URL context. Built with modern Python tooling (uv, mise, click, Python 3.14+), it provides a CLI-first architecture designed for humans, AI agents, and automation.

## Architecture

### Project Structure

```
gemini-url-context-tool/
├── gemini_url_context_tool/
│   ├── __init__.py              # Public API exports for library usage
│   ├── cli.py                   # CLI entry point with Click group
│   ├── core/                    # Core library functions (importable)
│   │   ├── __init__.py
│   │   └── client.py            # Gemini client management, query logic
│   ├── commands/                # CLI command implementations
│   │   ├── __init__.py
│   │   └── query_commands.py   # CLI wrapper with Click decorators
│   └── utils.py                 # Shared utilities (formatting, validation)
├── tests/
│   ├── __init__.py
│   └── test_utils.py            # Unit tests
├── pyproject.toml               # Project configuration
├── Makefile                     # Development commands
├── README.md                    # User documentation
├── CLAUDE.md                    # This file
├── LICENSE                      # MIT License
├── .mise.toml                   # mise configuration
└── .gitignore
```

### Key Design Principles

1. **Separation of Concerns**
   - `core/` contains business logic independent of CLI
   - `commands/` contains Click command wrappers
   - Core functions raise exceptions, CLI handles formatting and exit codes

2. **Exception-Based Error Handling**
   - Core functions raise specific exceptions (MissingApiKeyError, QueryError, ValueError)
   - CLI catches exceptions and formats rich error messages with command examples
   - Enables both CLI and library usage with consistent behavior

3. **Composable Output**
   - JSON to stdout for machine consumption
   - Logs and errors to stderr for human monitoring
   - Enables easy piping and integration with other tools

4. **Agent-Friendly Design**
   - Rich error messages with working command examples
   - Input validation with suggested fixes
   - Structured output for ReAct loop compatibility
   - Comprehensive `--help` with examples

## Development Commands

### Quick Start

```bash
# Install dependencies
make install

# Run full quality checks
make check

# Full pipeline (format, check, build, install)
make pipeline
```

### Quality Checks

```bash
make format      # Auto-format with ruff
make lint        # Lint with ruff (100 char line length)
make typecheck   # Type check with mypy (strict mode)
make test        # Run pytest suite
make check       # Run lint + typecheck + test
```

### Build & Install

```bash
make build            # Build package with uv
make install-global   # Install globally with uv tool (from wheel)
make pipeline         # Full workflow: format, check, build, install-global
```

### Local Development

```bash
make run ARGS="query 'https://example.com'"  # Run locally without install
```

## Code Standards

- **Python 3.14+** with modern syntax (dict/list over Dict/List)
- **Type hints** for all functions (strict mypy)
- **Docstrings** for all public functions with Args, Returns, Raises sections
- **Module docstrings** acknowledging AI-generated code
- **Line length**: 100 characters
- **Exception handling**: Raise exceptions in core, catch at CLI boundary
- **Click decorators**: @click.command, @click.argument, @click.option

## CLI Commands

### Main Command Group

```bash
gemini-url-context-tool --help     # Show main help
gemini-url-context-tool --version  # Show version (0.1.0)
```

### Query Command

```bash
gemini-url-context-tool query PROMPT [OPTIONS]
```

**Arguments:**
- `PROMPT` - Query prompt (optional if --stdin used)

**Options:**
- `--stdin, -s` - Read prompt from stdin
- `--no-search-tool` - Disable Google Search (URL context only)
- `--verbose, -v` - Include detailed metadata
- `--text, -t` - Output plain text instead of JSON
- `--help, -h` - Show command help with examples

**Examples:**

```bash
# Basic query
gemini-url-context-tool query "Analyze https://example.com"

# Read from stdin
echo "Analyze https://example.com" | gemini-url-context-tool query --stdin

# Disable search, get plain text
gemini-url-context-tool query "Extract pricing from https://example.com" \
  --no-search-tool \
  --text

# Verbose output with metadata
gemini-url-context-tool query "Summarize https://example.com" --verbose
```

## Library Usage

### Public API

Exported from `gemini_url_context_tool`:

- `query_with_url_context()` - Convenience function for queries
- `GeminiClient` - Client class for multiple queries
- `QueryResult` - Result dataclass with response_text, url_context_metadata, grounding_metadata
- `UrlMetadata` - Dataclass for URL retrieval info
- `GeminiClientError` - Base exception
- `MissingApiKeyError` - API key not set
- `QueryError` - Query failed

### Import Examples

```python
from gemini_url_context_tool import query_with_url_context

# Simple query
result = query_with_url_context("Analyze https://example.com")
print(result.response_text)
```

```python
from gemini_url_context_tool import GeminiClient

# Use client for multiple queries
client = GeminiClient()
result1 = client.query("Analyze https://example.com/page1")
result2 = client.query("Analyze https://example.com/page2")
```

```python
from gemini_url_context_tool import (
    query_with_url_context,
    MissingApiKeyError,
    QueryError,
)

# Error handling
try:
    result = query_with_url_context("Analyze https://example.com")
except MissingApiKeyError:
    print("Set GEMINI_API_KEY environment variable")
except QueryError as e:
    print(f"Query failed: {e}")
```

## Testing

```bash
# Run all tests
make test

# Run with verbose output
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_utils.py::test_validate_prompt_success

# Run with coverage
uv run pytest tests/ --cov=gemini_url_context_tool
```

## Important Notes

### Dependencies

- **click>=8.1.7** - CLI framework
- **google-genai>=1.0.0** - Google Gemini API client
- **ruff>=0.8.0** - Linting and formatting (dev)
- **mypy>=1.7.0** - Type checking (dev)
- **pytest>=7.4.0** - Testing framework (dev)
- **types-requests>=2.31.0** - Type stubs for requests (dev)

### Environment Variables

- `GEMINI_API_KEY` - **Required**. API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Authentication

The tool reads `GEMINI_API_KEY` from environment variables. For secure storage on macOS:

```bash
# Store in Keychain
security add-generic-password -a "production" -s "GEMINI_API_KEY" -w "your-key"

# Retrieve
export GEMINI_API_KEY=$(security find-generic-password -a "production" -s "GEMINI_API_KEY" -w)
```

### Client Implementation

- **Model**: Always uses `gemini-2.5-flash`
- **Tools**: URL context tool (always enabled) + Google Search tool (optional)
- **Error Handling**: Exceptions raised at core level, caught at CLI boundary
- **Metadata Extraction**: URL context metadata always included, grounding metadata only with --verbose

### Stdin Handling

The `--stdin` flag enables reading prompts from stdin for pipeline integration:

```bash
# Direct piping
echo "Analyze https://example.com" | gemini-url-context-tool query --stdin

# From file
cat prompt.txt | gemini-url-context-tool query --stdin

# Combined with other tools
curl -s https://example.com | jq '.urls[]' | xargs -I {} \
  gemini-url-context-tool query "Analyze {}"
```

**Validation:**
- Checks if stdin is a TTY (raises error if interactive terminal)
- Validates non-empty input
- Provides clear error messages with alternative commands

### Output Formats

**JSON (default):**
```json
{
  "response_text": "...",
  "url_context_metadata": [...],
  "grounding_metadata": {...}  // Only with --verbose
}
```

**Text (--text):**
```
Response text only, no JSON structure.
```

### Version Synchronization

**CRITICAL**: Keep version consistent across three locations:
- `pyproject.toml`: `[project] version = "0.1.0"`
- `cli.py`: `@click.version_option(version="0.1.0")`
- `__init__.py`: `__version__ = "0.1.0"`

Failure to sync versions will cause confusion for users.

## Known Issues & Future Fixes

### SDK Type Annotations Issue

**Problem**: The `google-genai` SDK has loose type annotations for the `tools` parameter in `GenerateContentConfig`. Mypy expects `list[Tool | Callable[..., Any] | Any | Any] | None` but providing a properly typed `list[types.Tool]` causes type errors.

**Location**: `gemini_url_context_tool/core/client.py:108-120`

**Current Workaround**:
```python
# Using list[Any] to satisfy SDK's loose typing
from typing import Any as AnyType

tools: list[AnyType] = [types.Tool(url_context=types.UrlContext())]

# Include Google Search tool unless disabled
if enable_search:
    tools = [
        types.Tool(url_context=types.UrlContext()),
        types.Tool(google_search=types.GoogleSearch()),
    ]

config = types.GenerateContentConfig(tools=tools)
```

**Proper Implementation (when SDK fixes types)**:
```python
# When SDK type annotations are tightened
from collections.abc import Sequence

tools: Sequence[types.Tool] = [types.Tool(url_context=types.UrlContext())]

if enable_search:
    tools = [
        types.Tool(url_context=types.UrlContext()),
        types.Tool(google_search=types.GoogleSearch()),
    ]

config = types.GenerateContentConfig(tools=tools)
```

**Steps to Fix When Resolved**:
1. Monitor `google-genai` SDK releases for type annotation improvements
2. Update `core/client.py` to use `Sequence[types.Tool]`
3. Remove `from typing import Any as AnyType` import
4. Run `make typecheck` to verify
5. Update this section in CLAUDE.md

### Response Text Extraction

**Note**: The SDK's response structure may return `None` for `part.text`. The code handles this:

```python
response_text = "".join(
    str(part.text)
    for part in candidate.content.parts
    if hasattr(part, "text") and part.text is not None
)
```

This ensures type safety and prevents `None` from entering the response string.

## Installation Methods

### Global Installation (Recommended)

```bash
cd /path/to/gemini-url-context-tool
make pipeline
```

This runs the full quality pipeline and installs globally from the wheel file.

### Development Installation

```bash
cd /path/to/gemini-url-context-tool
uv sync
uv run gemini-url-context-tool query "test prompt"
```

### Manual Global Install

```bash
cd /path/to/gemini-url-context-tool
uv tool install .
```

**Note**: Installing from `.` may use uv's cache. Use `make install-global` to install from the wheel file to avoid stale cache issues.

## Troubleshooting

### Type Errors

```bash
# Auto-fix common issues (Dict → dict, List → list)
uv run ruff check --fix .
```

### Import Errors in Tests

Ensure tests import from the package:
```python
from gemini_url_context_tool.core.client import QueryResult
from gemini_url_context_tool.utils import format_output
```

### Stale Cache After Changes

```bash
# Clean and rebuild
make clean
make build
make install-global
```

### Version Mismatch

Check all three locations:
```bash
grep -n "version" pyproject.toml
grep -n "version_option" gemini_url_context_tool/cli.py
grep -n "__version__" gemini_url_context_tool/__init__.py
```

## Resources

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [URL Context Feature](https://ai.google.dev/gemini-api/docs/url-context)
- [Google Search Grounding](https://ai.google.dev/gemini-api/docs/grounding)
- [Click Documentation](https://click.palletsprojects.com/)
- [uv Documentation](https://github.com/astral-sh/uv)
