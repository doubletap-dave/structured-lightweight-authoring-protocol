"""Tests for the debug module core functionality."""

import pytest

from src.nomenic.debug import debug

# Sample content for testing
SAMPLE_CONTENT = """
header: Test Document
text: This is a sample document with @b(bold) text.
list:
  - First item
  - Second item
code:
  print("Hello, world!")
"""


def test_debug_tokens_basic():
    """Test basic token debugging functionality."""
    # Test with default options
    result = debug(SAMPLE_CONTENT, mode="tokens")

    # Check that we have tokens
    assert isinstance(result, list)
    assert len(result) > 0

    # Check token structure
    token = result[0]
    assert "type" in token
    assert "value" in token
    assert "line" in token
    assert "column" in token


def test_debug_tokens_filter():
    """Test token debugging with type filtering."""
    # Filter to header tokens only
    result = debug(SAMPLE_CONTENT, mode="tokens", token_type="HEADER")

    # Check that all tokens are headers
    assert all(token["type"] == "HEADER" for token in result)


def test_debug_errors():
    """Test error debugging functionality."""
    # Create content with errors
    error_content = """
header: # Missing header text
list:
- # Missing list item text
    """

    # Test error debugging
    result = debug(error_content, mode="errors")

    # Check error structure
    assert isinstance(result, dict)
    assert "total_errors" in result
    assert result["total_errors"] > 0
    assert "errors" in result

    # Check first error
    error = result["errors"][0]
    assert "message" in error
    assert "line" in error
    assert "column" in error


def test_debug_styles():
    """Test style debugging functionality."""
    # Create content with styles
    style_content = """
text: This text has @b(bold) and @i(italic) styles.
    """

    # Test style debugging
    result = debug(style_content, mode="styles")

    # Check style structure
    assert isinstance(result, dict)
    assert "total_styles" in result
    assert "styles" in result

    # Check matches
    assert "matches" in result
    assert "bold" in result["matches"]
    assert "italic" in result["matches"]


def test_debug_invalid_mode():
    """Test invalid debug mode."""
    with pytest.raises(ValueError) as excinfo:
        debug(SAMPLE_CONTENT, mode="invalid")

    assert "Unknown debug mode" in str(excinfo.value)


def test_debug_output_json():
    """Test JSON output format."""
    # Get JSON format
    print("Starting test_debug_output_json")
    result = debug(SAMPLE_CONTENT, mode="tokens", output_format="json")
    print(f"Result type: {type(result)}")
    print(f"Result contents: {result}")

    # Check JSON structure
    assert isinstance(result, dict)
    assert "results" in result
    print("Test passed")
