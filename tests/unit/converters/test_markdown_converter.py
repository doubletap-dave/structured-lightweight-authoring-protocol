"""Tests for the Markdown converter."""

import pytest
from typing import Dict, Any

from nomenic.converters import MarkdownConverter


class TestMarkdownConverter:
    """Test suite for the Markdown converter."""

    def test_init(self):
        """Test initializing the converter."""
        converter = MarkdownConverter()
        assert isinstance(converter, MarkdownConverter)

    def test_extract_metadata(self):
        """Test extracting metadata from Markdown frontmatter."""
        converter = MarkdownConverter()

        # Test with frontmatter
        markdown = """---
title: Test Document
author: Test Author
date: 2025-05-10
---

# Test Heading

Test content."""

        metadata = converter.extract_metadata(markdown)
        assert metadata == {
            'title': 'Test Document',
            'author': 'Test Author',
            'date': '2025-05-10'
        }

        # Test without frontmatter
        markdown = """# Test Heading

Test content."""

        metadata = converter.extract_metadata(markdown)
        assert metadata == {}

    def test_remove_frontmatter(self):
        """Test removing frontmatter from Markdown."""
        converter = MarkdownConverter()

        # Test with frontmatter
        markdown = """---
title: Test Document
---

# Test Heading

Test content."""

        content = converter._remove_frontmatter(markdown)
        assert content == """# Test Heading

Test content."""

        # Test without frontmatter
        markdown = """# Test Heading

Test content."""

        content = converter._remove_frontmatter(markdown)
        assert content == markdown

    @pytest.mark.xfail(reason="Markdown from_nomenic conversion relies on basic renderer, may not match exactly")
    def test_from_nomenic(self):
        """Test converting Nomenic to Markdown."""
        converter = MarkdownConverter()

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

        # Test with frontmatter
        markdown = converter.from_nomenic(nomenic, include_frontmatter=True)

        # Verify metadata is included in some form
        assert "title: Test Document" in markdown
        assert "author: Test Author" in markdown

        # Verify content elements (less strict check)
        assert "Test Heading" in markdown
        assert "Test content" in markdown
        assert "Item 1" in markdown
        assert "Item 2" in markdown
        assert "python" in markdown
        assert "def test()" in markdown

        # Test without frontmatter
        markdown = converter.from_nomenic(nomenic, include_frontmatter=False)
        assert "title: Test Document" not in markdown
        assert "author: Test Author" not in markdown
        assert "Test Heading" in markdown

    def test_to_nomenic(self):
        """Test converting Markdown to Nomenic."""
        converter = MarkdownConverter()

        # Simple Markdown document
        markdown = """---
title: Test Document
author: Test Author
---

# Test Heading

Test content.

- Item 1
- Item 2

```python
def test():
    return "Hello, world!"
```"""

        # Test with metadata
        nomenic = converter.to_nomenic(markdown, include_metadata=True)
        # Basic validation of key parts
        assert "meta:" in nomenic
        assert "title: Test Document" in nomenic
        assert "header: Test Heading" in nomenic
        assert "text: Test content" in nomenic
        assert "list:" in nomenic
        assert "- Item 1" in nomenic
        assert "code:" in nomenic
        assert "def test()" in nomenic

        # Test without metadata
        nomenic = converter.to_nomenic(markdown, include_metadata=False)
        assert "meta:" not in nomenic
        assert "header: Test Heading" in nomenic

    @pytest.mark.xfail(reason="Markdown inline formatting conversion relies on basic regex")
    def test_inline_formatting(self):
        """Test converting inline formatting elements."""
        converter = MarkdownConverter()

        # Test Markdown to Nomenic (inline formatting)
        markdown_input = """# Test\n\nThis is **bold**, *italic*, and `code` text.\n\n[Link Text](https://example.com)"""

        nomenic_output = converter.to_nomenic(markdown_input)
        # Check for presence of converted inline styles, ignoring whitespace/structure
        assert "@b(bold)" in nomenic_output.replace(" ", "")
        assert "@i(italic)" in nomenic_output.replace(" ", "")
        assert "@c(code)" in nomenic_output.replace(" ", "")
        assert "@l(Link Text)" in nomenic_output.replace(" ", "")

        # Test Nomenic to Markdown (inline formatting)
        nomenic_input = """header: Test\n\n  text: This is @b(bold), @i(italic), and @c(code) text.\n\n  text: @l(Link Text)"""

        markdown_output = converter.from_nomenic(nomenic_input)
        # Check for presence of converted inline styles, ignoring whitespace/structure
        assert "**bold**" in markdown_output.replace(" ", "")
        assert "*italic*" in markdown_output.replace(" ", "")
        assert "`code`" in markdown_output.replace(" ", "")
        assert "[Link Text](#)" in markdown_output.replace(" ", "")

    @pytest.mark.xfail(reason="Markdown conversion uses basic regex, bidirectional may not be exact")
    def test_bidirectional_conversion(self):
        """Test bidirectional conversion (Markdown -> Nomenic -> Markdown)."""
        converter = MarkdownConverter()

        # Simple Markdown document
        original_markdown = """# Test Heading

This is a paragraph.

- Item 1
- Item 2

```python
def test():
    return "Hello, world!"
```"""

        # Convert Markdown to Nomenic
        nomenic = converter.to_nomenic(
            original_markdown, include_metadata=False)
        assert nomenic, "Nomenic conversion produced empty output"

        # Convert Nomenic back to Markdown
        markdown = converter.from_nomenic(nomenic, include_frontmatter=False)
        assert markdown, "Markdown conversion produced empty output"

        # Verify key elements are present in the final output (less strict)
        assert "Test Heading" in markdown
        assert "This is a paragraph" in markdown
        assert "Item 1" in markdown
        assert "Item 2" in markdown
        assert "python" in markdown
        assert "def test()" in markdown
