"""Tests for debug token_utils module."""

import pytest

from src.nomenic.debug.token_utils import analyze_tokens, check_token_patterns

# Sample content for testing
SAMPLE_CONTENT = """
header: Test Document
text: This is a sample document.
list:
  - First item
  - Second item
code:
  print("Hello, world!")
"""


def test_analyze_tokens():
    """Test token analysis functionality."""
    # Test with default options
    tokens = analyze_tokens(SAMPLE_CONTENT)

    # Check that we have tokens
    assert isinstance(tokens, list)
    assert len(tokens) > 0

    # Check token structure
    assert all("type" in token for token in tokens)
    assert all("value" in token for token in tokens)
    assert all("line" in token for token in tokens)
    assert all("column" in token for token in tokens)


def test_analyze_tokens_filter():
    """Test token analysis with filtering."""
    # Filter to HEADER tokens
    tokens = analyze_tokens(SAMPLE_CONTENT, token_type="HEADER")

    # Check that we have tokens and they're all headers
    assert len(tokens) > 0
    assert all(token["type"] == "HEADER" for token in tokens)

    # Filter to LIST tokens
    list_tokens = analyze_tokens(SAMPLE_CONTENT, token_type="LIST")
    assert len(list_tokens) > 0
    assert all(token["type"] == "LIST" for token in list_tokens)


def test_analyze_tokens_detailed():
    """Test token analysis with detailed output."""
    # Get detailed analysis
    tokens = analyze_tokens(SAMPLE_CONTENT, detailed=True)

    # Check that context is included
    assert "context" in tokens[0]
    assert isinstance(tokens[0]["context"], list)
    assert "context_line_start" in tokens[0]


def test_analyze_tokens_invalid_type():
    """Test token analysis with invalid token type."""
    with pytest.raises(ValueError) as excinfo:
        analyze_tokens(SAMPLE_CONTENT, token_type="NONEXISTENT")

    assert "Invalid token type" in str(excinfo.value)


def test_check_token_patterns():
    """Test token pattern checking."""
    # Test pattern checking
    result = check_token_patterns(SAMPLE_CONTENT)

    # Check structure
    assert isinstance(result, dict)
    assert len(result) > 0

    # Check line entry
    first_line_key = list(result.keys())[0]
    line_info = result[first_line_key]
    assert "content" in line_info
    assert "matches" in line_info
    assert isinstance(line_info["matches"], dict)


def test_check_token_patterns_specific_line():
    """Test token pattern checking for a specific line."""
    # Check for line 2 (header line in the sample)
    result = check_token_patterns(SAMPLE_CONTENT, line_number=2)

    # Should only have one entry
    assert len(result) == 1
    assert "line_2" in result

    # Line 2 should match header pattern
    header_line = result["line_2"]
    assert header_line["matches"]["block_token_flexible"]


def test_check_token_patterns_invalid_line():
    """Test token pattern checking with invalid line number."""
    with pytest.raises(ValueError) as excinfo:
        check_token_patterns(SAMPLE_CONTENT, line_number=1000)

    assert "out of range" in str(excinfo.value)
