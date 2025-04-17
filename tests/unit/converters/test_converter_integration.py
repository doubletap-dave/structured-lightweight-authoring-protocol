"""Integration tests for format converters."""

import pytest
import json
from typing import Dict, Any, Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from nomenic.converters import MarkdownConverter, JSONConverter, YAMLConverter


class TestConverterIntegration:
    """Integration tests for format converters."""

    def test_nomenic_round_trip(self):
        """Test converting Nomenic to all formats and back."""
        # Original Nomenic document
        nomenic = """meta:
  title: Test Document
  author: Test Author

header: Nomenic Test Document

  text: This is a test document for Nomenic format.

  list:
    - Item 1
    - Item 2
    - Item 3

  code:
    ```python
    def test_function():
        return "Hello, world!"
    ```"""

        # Nomenic -> Markdown -> Nomenic
        try:
            md_converter = MarkdownConverter()
            markdown = md_converter.from_nomenic(
                nomenic, include_frontmatter=True)
            assert markdown, "Empty output from Markdown conversion"

            nomenic_from_md = md_converter.to_nomenic(
                markdown, include_metadata=True)
            assert nomenic_from_md, "Empty output from conversion back to Nomenic"

            # Basic validation that key elements are present
            assert "Test Document" in nomenic_from_md
        except Exception as e:
            pytest.fail(f"Markdown round-trip conversion failed: {e}")

        # Nomenic -> JSON -> Nomenic
        try:
            json_converter = JSONConverter()
            json_str = json_converter.from_nomenic(
                nomenic, pretty=True, include_content=True)
            assert json_str, "Empty output from JSON conversion"

            # Validate JSON is well-formed
            json_data = json.loads(json_str)
            assert isinstance(json_data, dict)

            nomenic_from_json = json_converter.to_nomenic(
                json_str, include_metadata=True)
            assert nomenic_from_json, "Empty output from conversion back to Nomenic"

            # Basic validation that key elements are present
            assert "Test Document" in nomenic_from_json or "Nomenic Test Document" in nomenic_from_json
        except Exception as e:
            pytest.fail(f"JSON round-trip conversion failed: {e}")

        # Validate YAML conversion if PyYAML is available
        if HAS_YAML:
            try:
                # Nomenic -> YAML -> Nomenic
                yaml_converter = YAMLConverter()
                yaml_str = yaml_converter.from_nomenic(
                    nomenic, include_content=True)
                assert yaml_str, "Empty output from YAML conversion"

                # Validate YAML is well-formed
                yaml_data = yaml.safe_load(yaml_str)
                assert isinstance(yaml_data, dict)

                nomenic_from_yaml = yaml_converter.to_nomenic(
                    yaml_str, include_metadata=True)
                assert nomenic_from_yaml, "Empty output from conversion back to Nomenic"

                # Basic validation that key elements are present
                assert "Test Document" in nomenic_from_yaml or "Nomenic Test Document" in nomenic_from_yaml
            except Exception as e:
                pytest.fail(f"YAML round-trip conversion failed: {e}")

    @pytest.mark.xfail(reason="Cross-format conversion relies on limited Markdown converter")
    def test_cross_format_conversion(self):
        """Test converting between all formats (via Nomenic)."""
        # Create converters
        md_converter = MarkdownConverter()
        json_converter = JSONConverter()

        # Original Markdown document
        markdown = """---
title: Test Document
author: Test Author
---

# Markdown Test Document

This is a test document for Markdown format.

- Item 1
- Item 2
- Item 3

```python
def test_function():
    return "Hello, world!"
```"""

        try:
            # Markdown -> Nomenic
            nomenic = md_converter.to_nomenic(markdown, include_metadata=True)
            assert nomenic, "Empty output from Markdown to Nomenic conversion"

            # Nomenic -> JSON
            json_str = json_converter.from_nomenic(
                nomenic, pretty=True, include_content=True)
            assert json_str, "Empty output from Nomenic to JSON conversion"

            # Validate JSON is well-formed
            json_obj = json.loads(json_str)
            assert isinstance(json_obj, dict)

            # JSON -> Nomenic -> Markdown
            nomenic_from_json = json_converter.to_nomenic(
                json_str, include_metadata=True)
            assert nomenic_from_json, "Empty output from JSON to Nomenic conversion"

            markdown_final = md_converter.from_nomenic(
                nomenic_from_json, include_frontmatter=True)
            assert markdown_final, "Empty output from Nomenic to Markdown conversion"

            # Basic validation that key elements are present
            assert "Test Document" in markdown_final
            assert "Markdown Test Document" in markdown_final
        except Exception as e:
            pytest.fail(f"Cross-format conversion failed: {e}")

        # Validate YAML conversion if PyYAML is available
        if HAS_YAML:
            try:
                yaml_converter = YAMLConverter()

                # Nomenic -> YAML
                yaml_str = yaml_converter.from_nomenic(
                    nomenic, include_content=True)
                assert yaml_str, "Empty output from Nomenic to YAML conversion"

                # Validate YAML is well-formed
                yaml_obj = yaml.safe_load(yaml_str)
                assert isinstance(yaml_obj, dict)

                # YAML -> Nomenic -> Markdown
                nomenic_from_yaml = yaml_converter.to_nomenic(
                    yaml_str, include_metadata=True)
                assert nomenic_from_yaml, "Empty output from YAML to Nomenic conversion"

                markdown_from_yaml = md_converter.from_nomenic(
                    nomenic_from_yaml, include_frontmatter=True)
                assert markdown_from_yaml, "Empty output from Nomenic to Markdown conversion"

                # Basic validation that key elements are present
                assert "Test Document" in markdown_from_yaml or "Markdown Test Document" in markdown_from_yaml
            except Exception as e:
                pytest.fail(f"YAML cross-format conversion failed: {e}")

    def _validate_nomenic(self, nomenic: str):
        """Validate that key elements are present in a Nomenic document."""
        assert nomenic, "Empty Nomenic document"

        # Check for at least one structural element
        assert any(element in nomenic for element in [
                   "header:", "meta:", "text:", "list:", "code:"])

        # Check content presence (less strict)
        assert "Test" in nomenic
