# gemini-url-context-tool

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![AI Generated](https://img.shields.io/badge/AI-Generated-blueviolet.svg)](https://www.anthropic.com/claude)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)

A production-ready CLI and library for querying Google's Gemini models with URL context, enabling the model to access and analyze content from URLs provided in your prompts.

## Table of Contents

- [About](#about)
  - [What is Gemini URL Context?](#what-is-gemini-url-context)
  - [Why CLI-First?](#why-cli-first)
- [Use Cases](#use-cases)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI Usage](#cli-usage)
  - [Library Usage](#library-usage)
- [Output Formats](#output-formats)
- [Development](#development)
- [Testing](#testing)
- [Resources](#resources)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## About

### What is Gemini URL Context?

[Gemini URL Context](https://ai.google.dev/gemini-api/docs/url-context) is a feature of Google's Gemini API that allows the model to automatically extract URLs from your prompts and retrieve their content for analysis. This enables:

- **Automatic Content Retrieval**: The model extracts URLs from your prompt and fetches their content
- **Multi-Source Analysis**: Process up to 20 URLs per request
- **Diverse Content Types**: Supports HTML, PDFs, images, JSON, XML, and more
- **Combined Capabilities**: Works alongside Google Search for comprehensive information retrieval

For official documentation, pricing, and API details, see the [Gemini API Documentation](https://ai.google.dev/gemini-api/docs).

### Why CLI-First?

This tool embraces a **CLI-first architecture** designed for humans, AI agents, and automation:

**🤖 Agent-Friendly Design**
- **ReAct Loop Compatible**: Structured commands and error messages enable AI agents (like Claude Code) to reason and act effectively in iterative loops
- **Rich Error Messages**: Errors include context and working command examples, allowing agents to self-correct
- **Validation Gates**: Input validation with suggested fixes prevents common mistakes

**🔗 Composable Architecture**
- **JSON to stdout, logs to stderr**: Clean separation enables easy piping and integration
- **stdin Support**: Read prompts from pipelines for seamless automation
- **Multiple Output Formats**: JSON for machines, plain text for humans

**🧩 Reusable Building Blocks**
- **CLI Commands**: Use as building blocks for Claude Code skills, MCP servers, shell scripts, or custom workflows
- **Importable Library**: Use programmatically in Python applications
- **Production Quality**: Type-safe (strict mypy), tested (pytest), and documented

**🎯 Dual-Mode Operation**
- **CLI Tool**: Complete command-line interface with comprehensive help
- **Python Library**: Import and use in your applications with clean exception handling

## Use Cases

📚 **Document Analysis**
- Extract specific information from multiple documents, reports, or PDFs
- Compare versions of documents to identify changes
- Summarize long-form content from web pages or articles

💻 **Technical Documentation**
- Analyze GitHub repositories and code
- Generate setup instructions from README files
- Extract API documentation and examples

🔍 **Content Research**
- Compare products, services, or pricing across multiple URLs
- Gather information from multiple sources for research
- Fact-check claims by analyzing source URLs

🎯 **AI Agent Integration**
- Use in Claude Code skills for automated workflows
- Build MCP servers for AI assistants
- Create automation pipelines with structured output

## Features

- ✅ **URL Context Queries**: Query Gemini with URLs embedded in prompts
- ✅ **Google Search Integration**: Combine URL context with Google Search (optional)
- ✅ **stdin Support**: Read prompts from stdin for pipeline integration
- ✅ **Multiple Output Formats**: JSON (default) or plain text
- ✅ **Verbose Metadata**: Include URL retrieval status and grounding metadata
- ✅ **Rich Error Messages**: Actionable errors with command examples
- ✅ **Type-Safe**: Strict mypy type checking throughout
- ✅ **Fully Tested**: Comprehensive pytest test suite
- ✅ **CLI and Library**: Use as CLI tool or import in Python
- ✅ **Agent-Friendly**: Designed for AI agent integration (ReAct loops)

## Installation

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Google Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Install Globally with uv

```bash
# Clone the repository
git clone https://github.com/dnvriend/gemini-url-context-tool.git
cd gemini-url-context-tool

# Install dependencies and build
make pipeline

# The tool is now available globally
gemini-url-context-tool --version
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/dnvriend/gemini-url-context-tool.git
cd gemini-url-context-tool

# Install globally with uv
uv tool install .
```

### Verify Installation

```bash
gemini-url-context-tool --version
gemini-url-context-tool --help
```

## Configuration

### Environment Variables

The tool requires a Gemini API key. Set it as an environment variable:

```bash
export GEMINI_API_KEY='your-api-key-here'
```

### Get an API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create or select a project
3. Generate an API key
4. Store it securely (e.g., in macOS Keychain)

### Secure Storage (macOS)

Store your API key in macOS Keychain:

```bash
# Store key
security add-generic-password -a "production" -s "GEMINI_API_KEY" -w "your-api-key-here"

# Retrieve and export
export GEMINI_API_KEY=$(security find-generic-password -a "production" -s "GEMINI_API_KEY" -w)
```

## Usage

### CLI Usage

The CLI provides a single `query` command with options for customizing behavior.

#### Basic Query

```bash
gemini-url-context-tool query "Summarize the key points from https://example.com/article"
```

#### Compare Multiple URLs

```bash
gemini-url-context-tool query "Compare the pricing and features from https://example.com/product1 and https://example.com/product2"
```

#### Read from stdin

```bash
echo "Analyze https://example.com/doc.pdf" | gemini-url-context-tool query --stdin
```

#### Disable Google Search (URL Context Only)

```bash
gemini-url-context-tool query "Extract pricing from https://example.com/pricing" --no-search-tool
```

#### Get Verbose Output with Metadata

```bash
gemini-url-context-tool query "Summarize https://example.com" --verbose
```

#### Output Plain Text Instead of JSON

```bash
gemini-url-context-tool query "What are the main features at https://example.com" --text
```

#### Combine Options

```bash
gemini-url-context-tool query "Analyze https://example.com/report.pdf" \
  --no-search-tool \
  --verbose \
  --text
```

#### Pipeline Integration

```bash
# Generate prompt dynamically
echo "Compare $(cat urls.txt | head -2)" | gemini-url-context-tool query --stdin

# Extract response text with jq
gemini-url-context-tool query "Summarize https://example.com" | jq -r '.response_text'

# Check URL retrieval status
gemini-url-context-tool query "Analyze https://example.com" | jq '.url_context_metadata'
```

### Library Usage

Use `gemini-url-context-tool` as a library in your Python applications.

#### Basic Usage

```python
from gemini_url_context_tool import query_with_url_context

# Simple query
result = query_with_url_context("Analyze https://example.com")
print(result.response_text)
```

#### With Options

```python
from gemini_url_context_tool import query_with_url_context

# Query with verbose metadata and search disabled
result = query_with_url_context(
    prompt="Compare https://example.com/page1 and https://example.com/page2",
    enable_search=False,
    verbose=True,
)

print(result.response_text)
print(result.url_context_metadata)
```

#### Using the Client

```python
from gemini_url_context_tool import GeminiClient

# Create client
client = GeminiClient()  # Uses GEMINI_API_KEY env var

# Query
result = client.query(
    prompt="Summarize https://example.com/article",
    enable_search=True,
    verbose=False,
)

print(result.response_text)
```

#### Error Handling

```python
from gemini_url_context_tool import (
    query_with_url_context,
    MissingApiKeyError,
    QueryError,
)

try:
    result = query_with_url_context("Analyze https://example.com")
    print(result.response_text)
except MissingApiKeyError as e:
    print(f"API key not set: {e}")
except QueryError as e:
    print(f"Query failed: {e}")
except ValueError as e:
    print(f"Invalid input: {e}")
```

#### Access URL Metadata

```python
from gemini_url_context_tool import query_with_url_context

result = query_with_url_context("Analyze https://example.com", verbose=True)

# Check URL retrieval status
if result.url_context_metadata:
    for url_meta in result.url_context_metadata:
        print(f"URL: {url_meta.retrieved_url}")
        print(f"Status: {url_meta.url_retrieval_status}")

# Access grounding metadata (if Google Search was enabled)
if result.grounding_metadata:
    print(f"Search queries: {result.grounding_metadata.get('web_search_queries', [])}")
```

## Output Formats

### JSON Output (Default)

```json
{
  "response_text": "The article discusses...",
  "url_context_metadata": [
    {
      "retrieved_url": "https://example.com/article",
      "url_retrieval_status": "URL_RETRIEVAL_STATUS_SUCCESS"
    }
  ]
}
```

### JSON with Verbose Metadata

```json
{
  "response_text": "The article discusses...",
  "url_context_metadata": [
    {
      "retrieved_url": "https://example.com/article",
      "url_retrieval_status": "URL_RETRIEVAL_STATUS_SUCCESS"
    }
  ],
  "grounding_metadata": {
    "web_search_queries": ["topic research"],
    "grounding_chunks": [
      {
        "uri": "https://search-result.com",
        "title": "Search Result Title"
      }
    ],
    "grounding_supports": [...]
  }
}
```

### Plain Text Output (--text)

```
The article discusses three main topics: technology trends,
market analysis, and future predictions. Key findings include...
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dnvriend/gemini-url-context-tool.git
cd gemini-url-context-tool

# Install dependencies
make install

# Show available commands
make help
```

### Available Make Commands

```bash
make install          # Install dependencies
make format           # Format code with ruff
make lint             # Run linting with ruff
make typecheck        # Run type checking with mypy
make test             # Run tests with pytest
make check            # Run all checks (lint, typecheck, test)
make pipeline         # Full pipeline (format, lint, typecheck, test, build, install-global)
make build            # Build package
make run ARGS="..."   # Run gemini-url-context-tool locally
make clean            # Remove build artifacts
```

### Project Structure

```
gemini-url-context-tool/
├── gemini_url_context_tool/
│   ├── __init__.py              # Public API exports
│   ├── cli.py                   # CLI entry point
│   ├── core/                    # Core library functions
│   │   ├── __init__.py
│   │   └── client.py            # Gemini client and query logic
│   ├── commands/                # CLI command implementations
│   │   ├── __init__.py
│   │   └── query_commands.py   # Query command wrapper
│   └── utils.py                 # Shared utilities
├── tests/                       # Test suite
│   ├── __init__.py
│   └── test_utils.py
├── pyproject.toml               # Project configuration
├── Makefile                     # Development commands
├── README.md                    # This file
├── LICENSE                      # MIT License
└── CLAUDE.md                    # Developer documentation
```

## Testing

Run the test suite:

```bash
# Run all tests
make test

# Run tests with verbose output
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_utils.py

# Run with coverage
uv run pytest tests/ --cov=gemini_url_context_tool
```

## Resources

### Official Documentation

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [URL Context Feature Guide](https://ai.google.dev/gemini-api/docs/url-context)
- [Google Search Grounding](https://ai.google.dev/gemini-api/docs/grounding)
- [Pricing Information](https://ai.google.dev/gemini-api/docs/pricing)

### Related Tools

- [Google GenAI Python SDK](https://github.com/google/generative-ai-python)
- [Google AI Studio](https://aistudio.google.com/)

## Known Issues

### SDK Type Annotations

The `google-genai` SDK has loose type annotations for the `tools` parameter in `GenerateContentConfig`. This tool works around this by using `list[Any]` for the tools list, which satisfies both mypy and the SDK's runtime requirements.

**Code Location**: `gemini_url_context_tool/core/client.py:108-120`

**Workaround**:
```python
# Using list[Any] to satisfy SDK's loose typing
from typing import Any as AnyType
tools: list[AnyType] = [types.Tool(url_context=types.UrlContext())]
```

This will be improved when the SDK's type annotations are tightened.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the full pipeline (`make pipeline`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for public functions
- Format code with `ruff`
- Pass all linting and type checks
- Ensure all tests pass

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Dennis Vriend**

- GitHub: [@dnvriend](https://github.com/dnvriend)

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI framework
- Powered by [Google Gemini API](https://ai.google.dev/gemini-api)
- Developed with [uv](https://github.com/astral-sh/uv) for fast Python tooling
- Generated with assistance from [Claude Code](https://www.anthropic.com/claude/code)

---

**Built with AI**

This project was developed with assistance from [Claude Code](https://www.anthropic.com/claude/code), an AI-powered development tool by [Anthropic](https://www.anthropic.com/). The code has been reviewed, tested, and validated by a human.

Made with ❤️ using Python 3.14
