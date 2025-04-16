#!/usr/bin/env python3
"""Simple script to debug the failing test."""

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


def main():
    """Run the failing test directly."""
    print("Starting test")
    result = debug(SAMPLE_CONTENT, mode="tokens", output_format="json")
    print(f"Result type: {type(result)}")
    print(f"Result contents: {result}")

    # Check assertions
    assert isinstance(result, dict), f"Result is not a dict: {type(result)}"
    assert "results" in result, f"'results' not in result: {list(result.keys())}"
    print("All assertions passed!")


if __name__ == "__main__":
    main()
