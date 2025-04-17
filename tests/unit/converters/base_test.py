"""Tests for the base FormatConverter class."""

import pytest
from typing import Dict, Any

from nomenic.converters.base import FormatConverter


class SimpleConverter(FormatConverter):
    """Simple concrete implementation of FormatConverter for testing."""

    def to_nomenic(self, source: str, **options) -> str:
        """Convert from source format to Nomenic."""
        return f"header: {source}"

    def from_nomenic(self, nomenic: str, **options) -> str:
        """Convert from Nomenic to target format."""
        # Extract header content if present
        if "header:" in nomenic:
            content = nomenic.split("header:", 1)[1].strip()
            return content
        return nomenic


class TestFormatConverter:
    """Test suite for the base FormatConverter class."""

    def test_abstract_methods(self):
        """Test that FormatConverter is an abstract base class."""
        with pytest.raises(TypeError):
            FormatConverter()  # Should raise TypeError as it's abstract

    def test_detect_format(self):
        """Test format detection from content."""
        class TestConverter(FormatConverter):
            def to_nomenic(self, source: str) -> str:
                return source

            def from_nomenic(self, nomenic: str) -> str:
                return nomenic

        converter = TestConverter()

        # Test YAML detection
        yaml_content = "---\nkey: value\n---\n"
        assert converter._detect_format(yaml_content) == "yaml"

        # Test JSON detection
        json_content = '{"key": "value"}'
        assert converter._detect_format(json_content) == "json"

        # Test Markdown detection
        md_content = "# Header\n\nSome text"
        assert converter._detect_format(md_content) == "md"

        # Test unknown format
        unknown_content = "plain text"
        assert converter._detect_format(unknown_content) is None

    def test_extract_metadata(self):
        """Test metadata extraction."""
        converter = SimpleConverter()
        metadata = converter.extract_metadata("Test content")
        assert metadata == {}

    def test_apply_metadata(self):
        """Test metadata application."""
        converter = SimpleConverter()
        content = "Test content"
        metadata = {"title": "Test Document"}
        result = converter.apply_metadata(content, metadata)
        assert result == content

    def test_partial_convert_to_nomenic(self):
        """Test partial_convert with to_nomenic conversion."""
        converter = SimpleConverter()
        source = "Test content"
        result = converter.partial_convert(source, from_nomenic=False)
        assert result == "header: Test content"

    def test_partial_convert_from_nomenic(self):
        """Test partial_convert with from_nomenic conversion."""
        converter = SimpleConverter()
        source = "header: Test content"
        result = converter.partial_convert(source, from_nomenic=True)
        assert result == "Test content"

    def test_partial_convert_with_options(self):
        """Test partial_convert passes options correctly."""
        class OptionsConverter(FormatConverter):
            def to_nomenic(self, source: str, **options) -> str:
                return f"header: {source} with {options.get('option', 'default')}"

            def from_nomenic(self, nomenic: str, **options) -> str:
                return f"{nomenic} with {options.get('option', 'default')}"

        converter = OptionsConverter()
        source = "Test content"

        # Test to_nomenic with options
        result = converter.partial_convert(
            source, from_nomenic=False, option="test")
        assert result == "header: Test content with test"

        # Test from_nomenic with options
        result = converter.partial_convert(
            "nomenic content", from_nomenic=True, option="test")
        assert result == "nomenic content with test"
