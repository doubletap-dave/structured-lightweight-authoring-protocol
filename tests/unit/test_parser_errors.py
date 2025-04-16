"""Tests for the Nomenic Core parser error handling."""

import pytest

from nomenic.errors import ParserError
from nomenic.lexer import tokenize
from nomenic.parser import Parser, parse


def test_parser_error_recording():
    """Test that the parser records errors when it encounters problems."""
    # Source with various errors
    source = """
header: # Missing header text
list:
- # Missing list item text
text:
>>> # Missing closing <<<
code:
# No code content
    """

    tokens = tokenize(source)
    parser = Parser(tokens)
    # Parse should still complete, recording errors but not raising them
    parser.parse()  # Execute parse to collect errors, but we don't need the document

    # Debug prints
    print(f"\nTotal errors recorded: {len(parser.errors)}")
    for i, (msg, token) in enumerate(parser.errors):
        print(f"Error {i+1}: {msg} at line {token.line}, column {token.column}")

    # Verify errors were recorded
    assert len(parser.errors) > 0, "No errors were recorded!"
    # At least these errors should be recorded
    error_messages = [msg for msg, _ in parser.errors]
    for msg in error_messages:
        print(f"Message: {msg}")

    expected_errors = ["header", "list item", "multi-line text block", "code block"]
    for expected in expected_errors:
        has_error = any(expected in msg.lower() for msg in error_messages)
        assert has_error, (
            f"Expected error containing '{expected}' not found in messages: "
            f"{error_messages}"
        )


def test_parser_error_reporting():
    """Test that the parser can be made to raise errors immediately."""
    # Source with a specific error
    source = """
header: # Missing header text
"""

    tokens = tokenize(source)
    parser = Parser(tokens)

    # Directly call _report_error which should raise a ParserError
    with pytest.raises(ParserError, match="header"):
        parser._report_error("Expected text after header:", parser._peek())


def test_parser_recovers_from_errors():
    """Test that the parser can recover from errors using synchronization."""
    # Source with an error in the first block but valid content after
    source = """
header: # Missing header text
text: This is valid text content that should be parsed correctly.
"""

    tokens = tokenize(source)
    document = parse(tokens)

    # Despite the error in the header, the parser should recover and parse the text
    assert len(document.children) > 0

    # Check that we got the text node
    text_nodes = [
        node for node in document.children if node.__class__.__name__ == "TextNode"
    ]
    assert len(text_nodes) > 0
    assert any("valid text content" in node.text for node in text_nodes)


def test_multiline_text_block_error_handling():
    """Test error handling for unterminated multi-line text blocks."""
    # Source with unterminated multi-line text block
    source = """
text:
>>>
This is some text that should be parsed.
But the closing <<< is missing.
"""

    tokens = tokenize(source)
    parser = Parser(tokens)
    document = parser.parse()

    # The text content should still be parsed despite the missing <<<
    assert len(document.children) > 0

    # The error should be recorded
    assert len(parser.errors) > 0
    assert any("unterminated" in msg.lower() for msg, _ in parser.errors)

    # And we should have the content in a TextNode
    text_nodes = [
        node for node in document.children if node.__class__.__name__ == "TextNode"
    ]
    assert len(text_nodes) > 0
    assert any("should be parsed" in node.text for node in text_nodes)
