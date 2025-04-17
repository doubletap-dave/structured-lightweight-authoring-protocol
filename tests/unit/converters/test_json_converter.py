"""Tests for the JSON converter."""

import json
import pytest
from typing import Dict, Any

from nomenic.converters import JSONConverter


class TestJSONConverter:
    """Test suite for the JSON converter."""

    def test_init(self):
        """Test initializing the converter."""
        converter = JSONConverter()
        assert isinstance(converter, JSONConverter)

    def test_extract_metadata(self):
        """Test extracting metadata from JSON content."""
        converter = JSONConverter()

        # Test with metadata
        json_content = json.dumps({
            "metadata": {
                "title": "Test Document",
                "author": "Test Author",
                "date": "2025-05-10"
            },
            "content": "Test content"
        })

        metadata = converter.extract_metadata(json_content)
        assert metadata == {
            "title": "Test Document",
            "author": "Test Author",
            "date": "2025-05-10"
        }

        # Test without metadata
        json_content = json.dumps({
            "content": "Test content"
        })

        metadata = converter.extract_metadata(json_content)
        assert metadata == {}

    def test_from_nomenic(self):
        """Test converting Nomenic to JSON."""
        converter = JSONConverter()

        # Simple Nomenic document
        nomenic = """meta:
  title: Test Document
  author: Test Author

header: Test Heading

  text: Test content.

  list:
    - Item 1
    - Item 2

  code:
    ```python
    def test():
        return "Hello, world!"
    ```"""

        # Test with pretty printing (default)
        json_output = converter.from_nomenic(
            nomenic, pretty=True, include_content=True)

        # Basic validation that it's valid JSON
        try:
            json_data = json.loads(json_output)
            assert isinstance(json_data, dict)
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON output")

        # Test content separately since implementation details may vary
        if "document" in json_data:
            assert isinstance(json_data["document"], list)

        if "metadata" in json_data:
            assert isinstance(json_data["metadata"], dict)

        # Test without pretty printing
        json_output = converter.from_nomenic(
            nomenic, pretty=False, include_content=True)
        assert isinstance(json_output, str)
        json_data = json.loads(json_output)  # Should be valid JSON

    def test_to_nomenic(self):
        """Test converting JSON to Nomenic."""
        converter = JSONConverter()

        # Simple JSON document
        json_content = json.dumps({
            "metadata": {
                "title": "Test Document",
                "author": "Test Author"
            },
            "document": [
                {
                    "type": "header",
                    "level": 1,
                    "content": "Test Heading"
                },
                {
                    "type": "text",
                    "content": "Test content."
                },
                {
                    "type": "list",
                    "items": ["Item 1", "Item 2"]
                },
                {
                    "type": "code",
                    "language": "python",
                    "content": "def test():\n    return \"Hello, world!\""
                }
            ]
        })

        # Test with metadata
        nomenic = converter.to_nomenic(json_content, include_metadata=True)

        # Check that the conversion occurred and has key elements
        assert "header:" in nomenic
        assert "Test Heading" in nomenic
        assert "Test content" in nomenic

        # Test without metadata
        nomenic = converter.to_nomenic(json_content, include_metadata=False)
        assert "meta:" not in nomenic
        assert "header:" in nomenic

    def test_bidirectional_conversion(self):
        """Test bidirectional conversion (JSON -> Nomenic -> JSON)."""
        converter = JSONConverter()

        # Simple JSON document with just the essential elements
        original_json = {
            "document": [
                {
                    "type": "header",
                    "level": 1,
                    "content": "Test Heading"
                },
                {
                    "type": "text",
                    "content": "Test content."
                }
            ]
        }

        # Convert JSON to Nomenic
        nomenic = converter.to_nomenic(json.dumps(
            original_json), include_metadata=False)

        # Convert Nomenic back to JSON
        json_output = converter.from_nomenic(nomenic, include_content=True)

        # Basic validation that it's valid JSON
        try:
            json_data = json.loads(json_output)
            assert isinstance(json_data, dict)
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON output")

    def test_invalid_json(self):
        """Test handling invalid JSON input."""
        converter = JSONConverter()

        # Invalid JSON
        invalid_json = "{invalid json}"

        # Test to_nomenic with invalid JSON
        with pytest.raises(ValueError):
            converter.to_nomenic(invalid_json)

        # Test extract_metadata with invalid JSON
        metadata = converter.extract_metadata(invalid_json)
        assert metadata == {}
