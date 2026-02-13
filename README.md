# Checktica Python SDK

[![PyPI version](https://badge.fury.io/py/checktica.svg)](https://badge.fury.io/py/checktica)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Coverage](https://raw.githubusercontent.com/checktica/checktica-python/gh-pages/coverage.svg?raw=true)](https://github.com/checktica/checktica-python/actions/workflows/main.yml)

Open Source Python SDK for Checktica - detect AI-generated text with high accuracy.

## Features

- 🎯 **99%+ accuracy** in detecting AI-generated content
- 🚀 **Multiple detection methods** from fastest to most accurate
- 📦 **Simple API** - just one function to call
- 🔄 **Automatic retries** with smart error handling
- 📝 **No length limits** on text analysis
- 🆓 **Free API** access

## Installation

Install Checktica using uv:

```bash
uv add checktica
```

## Quick Start

### Step 1: Import the SDK

```python
from checktica import detect
```

### Step 2: Check Your Text

```python
text = """
    AI detectors help distinguish between human and AI-generated writing.
    Checktica offers high accuracy, a free Python SDK, and no text length limits.
"""

result = detect(text)
```

### Step 3: Interpret Results

```python
if result.is_llm_generated:
    print(f"AI-generated (confidence: {result.confidence:.2%})")
    print(f"Remarks: {result.remarks}")
else:
    print(f"Human-written (confidence: {result.confidence:.2%})")
```

## Detection Methods

Checktica provides five detection methods with different speed/accuracy tradeoffs:

| Method | Speed | Accuracy | Best For |
|--------|-------|----------|----------|
| `most_accurate` | Slowest | Highest | Critical decisions, academic integrity |
| `more_accurate` | Slow | Very High | Important content verification |
| `balanced` | Medium | High | General purpose use |
| `fast` | Fast | Good | Real-time filtering |
| `fastest` | Fastest | Acceptable | Bulk processing |

### Choosing a Detection Method

```python
# Use the most accurate method (default, recommended)
result = detect(text, detection_method="most_accurate")

# Use faster method for bulk processing
result = detect(text, detection_method="fastest")

# Balanced approach for most cases
result = detect(text, detection_method="balanced")
```

## Understanding Results

The `detect()` function returns a `DetectionResult` object with three fields:

```python
result = detect(text)

# Is the text AI-generated?
print(result.is_llm_generated)  # True or False

# Confidence score (0.0 to 1.0)
print(result.confidence)  # e.g., 0.95 means 95% confident

# Additional context about the detection
print(result.remarks)  # e.g., "None."
```

## More Examples

Check out the [`examples/`](examples/) directory for complete working examples:

- [`hello_world.py`](examples/hello_world.py) - Basic usage
- [`product_reviews.py`](examples/product_reviews.py) - Analyzing product reviews
- [`student_essay_scanner.py`](examples/student_essay_scanner.py) - Educational use case

## Development Setup

Want to contribute? Here's how to set up your development environment:

### Step 1: Clone the Repository

```bash
git clone https://github.com/checktica/checktica-python.git
cd checktica-python
```

### Step 2: Install Dependencies

This project uses [uv](https://docs.astral.sh/uv/) for dependency management:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### Step 3: Run Tests

```bash
# Run all tests with coverage
uv run pytest

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Step 4: Code Quality

We use Ruff for linting and formatting:

```bash
# Format code
uv run ruff format .

# Check for issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .
```

### Step 5: Pre-commit Hooks

Set up pre-commit hooks to automatically check code quality:

```bash
uv run pre-commit install
```

## Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository.
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`).
3. **Make** your changes.
4. **Test** your changes (`uv run pytest tests/`).
5. **Commit** your changes (`git commit -m 'feat: Add amazing feature'`).
6. **Push** to the branch (`git push origin feature/amazing-feature`).
7. **Open** a Pull Request.

Please ensure:
- All tests pass (`uv run pytest`).
- Code is formatted (`uv run ruff format .`).
- Linting passes (`uv run ruff check .`).
- Coverage remains at 100%.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: contact@checktica.com
- 🌐 Website: https://checktica.com
- 📚 Documentation: https://api.checktica.com/v1/docs
- 🐛 Issues: https://github.com/checktica/checktica-python/issues

## Acknowledgments

Built with ❤️ by the Checktica team.



