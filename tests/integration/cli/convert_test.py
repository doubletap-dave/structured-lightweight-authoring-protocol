"""Integration tests for the CLI convert command."""

import os
import tempfile
from pathlib import Path

import pytest
from nomenic.cli.main import handle_convert


class TestCLIConvert:
    """Test suite for the CLI convert command."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_convert_markdown_to_nomenic(self, temp_dir):
        """Test converting Markdown to Nomenic format."""
        # Create input file
        input_file = temp_dir / "test.md"
        input_file.write_text("""# Header
Some text

## Subheader
- List item 1
- List item 2
""")

        # Create output file
        output_file = temp_dir / "output.nmc"

        # Run conversion
        args = type('Args', (), {
            'file': str(input_file),
            'from_format': None,
            'to_format': 'nmc',
            'output': str(output_file)
        })
        handle_convert(args)

        # Check output
        expected = """header: Header
text: Some text

header: Subheader
list:
  - List item 1
  - List item 2
"""
        assert output_file.read_text() == expected

    def test_convert_yaml_to_nomenic(self, temp_dir):
        """Test converting YAML to Nomenic format."""
        # Create input file
        input_file = temp_dir / "test.yaml"
        input_file.write_text("""title: Test Document
sections:
  - header: Introduction
    content: This is the intro
  - header: Main Content
    items:
      - Item 1
      - Item 2
""")

        # Create output file
        output_file = temp_dir / "output.nmc"

        # Run conversion
        args = type('Args', (), {
            'file': str(input_file),
            'from_format': None,
            'to_format': 'nmc',
            'output': str(output_file)
        })
        handle_convert(args)

        # Check output
        expected = """meta:
  title: Test Document

header: Introduction
text: This is the intro

header: Main Content
list:
  - Item 1
  - Item 2
"""
        assert output_file.read_text() == expected

    def test_convert_json_to_nomenic(self, temp_dir):
        """Test converting JSON to Nomenic format."""
        # Create input file
        input_file = temp_dir / "test.json"
        input_file.write_text("""{
    "title": "Test Document",
    "sections": [
        {
            "header": "Introduction",
            "content": "This is the intro"
        },
        {
            "header": "Main Content",
            "items": ["Item 1", "Item 2"]
        }
    ]
}""")

        # Create output file
        output_file = temp_dir / "output.nmc"

        # Run conversion
        args = type('Args', (), {
            'file': str(input_file),
            'from_format': None,
            'to_format': 'nmc',
            'output': str(output_file)
        })
        handle_convert(args)

        # Check output
        expected = """meta:
  title: Test Document

header: Introduction
text: This is the intro

header: Main Content
list:
  - Item 1
  - Item 2
"""
        assert output_file.read_text() == expected

    def test_convert_nomenic_to_markdown(self, temp_dir):
        """Test converting Nomenic to Markdown format."""
        # Create input file
        input_file = temp_dir / "test.nmc"
        input_file.write_text("""meta:
  title: Test Document

header: Introduction
text: This is the intro

header: Main Content
list:
  - Item 1
  - Item 2
""")

        # Create output file
        output_file = temp_dir / "output.md"

        # Run conversion
        args = type('Args', (), {
            'file': str(input_file),
            'from_format': None,
            'to_format': 'md',
            'output': str(output_file)
        })
        handle_convert(args)

        # Check output
        expected = """---
title: Test Document
---
# Introduction
This is the intro

## Main Content
- Item 1
- Item 2
"""
        assert output_file.read_text() == expected

    def test_convert_nomenic_to_yaml(self, temp_dir):
        """Test converting Nomenic to YAML format."""
        # Create input file
        input_file = temp_dir / "test.nmc"
        input_file.write_text("""meta:
  title: Test Document

header: Introduction
text: This is the intro

header: Main Content
list:
  - Item 1
  - Item 2
""")

        # Create output file
        output_file = temp_dir / "output.yaml"

        # Run conversion
        args = type('Args', (), {
            'file': str(input_file),
            'from_format': None,
            'to_format': 'yaml',
            'output': str(output_file)
        })
        handle_convert(args)

        # Check output
        expected = """title: Test Document
sections:
  - header: Introduction
    content: This is the intro
  - header: Main Content
    items:
      - Item 1
      - Item 2
"""
        assert output_file.read_text() == expected

    def test_convert_nomenic_to_json(self, temp_dir):
        """Test converting Nomenic to JSON format."""
        # Create input file
        input_file = temp_dir / "test.nmc"
        input_file.write_text("""meta:
  title: Test Document

header: Introduction
text: This is the intro

header: Main Content
list:
  - Item 1
  - Item 2
""")

        # Create output file
        output_file = temp_dir / "output.json"

        # Run conversion
        args = type('Args', (), {
            'file': str(input_file),
            'from_format': None,
            'to_format': 'json',
            'output': str(output_file)
        })
        handle_convert(args)

        # Check output
        expected = """{
    "title": "Test Document",
    "sections": [
        {
            "header": "Introduction",
            "content": "This is the intro"
        },
        {
            "header": "Main Content",
            "items": ["Item 1", "Item 2"]
        }
    ]
}"""
        assert output_file.read_text() == expected

    def test_convert_with_explicit_format(self, temp_dir):
        """Test converting with explicit format specification."""
        # Create input file
        input_file = temp_dir / "test.txt"
        input_file.write_text("""# Header
Some text

## Subheader
- List item 1
- List item 2
""")

        # Create output file
        output_file = temp_dir / "output.nmc"

        # Run conversion with explicit format
        args = type('Args', (), {
            'file': str(input_file),
            'from_format': 'md',
            'to_format': 'nmc',
            'output': str(output_file)
        })
        handle_convert(args)

        # Check output
        expected = """header: Header
text: Some text

header: Subheader
list:
  - List item 1
  - List item 2
"""
        assert output_file.read_text() == expected

    def test_convert_file_not_found(self):
        """Test handling of non-existent input file."""
        args = type('Args', (), {
            'file': 'nonexistent.txt',
            'from_format': None,
            'to_format': 'nmc',
            'output': None
        })
        with pytest.raises(FileNotFoundError):
            handle_convert(args)
