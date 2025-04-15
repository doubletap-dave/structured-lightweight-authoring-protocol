#!/usr/bin/env python3
"""Diagnostic script to check parser error recording."""

from src.nomenic.lexer import tokenize
from src.nomenic.parser import Parser


def main():
    """Run diagnostic tests on parser error handling."""
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
    parser.parse()  # Execute the parse but we don't need the document

    print(f"\nTotal errors recorded: {len(parser.errors)}")
    for i, (msg, token) in enumerate(parser.errors):
        print(f"Error {i+1}: {msg} at line {token.line}, column {token.column}")

    # Check for expected error types
    error_messages = [msg.lower() for msg, _ in parser.errors]
    expected_errors = ["header", "list item", "multi-line", "code block"]

    print("\nExpected errors check:")
    for expected in expected_errors:
        found = any(expected in msg for msg in error_messages)
        print(f"- {expected}: {'Found' if found else 'Not found'}")


if __name__ == "__main__":
    main()
