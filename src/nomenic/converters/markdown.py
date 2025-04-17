"""Markdown converter for transforming between Nomenic and Markdown formats."""

import re
from typing import Dict, List, Optional

from .base import FormatConverter
from .. import Lexer, Parser
from ..ast import ASTNode, HeaderNode, TextNode, ListNode, ListItemNode, CodeNode
from ..renderers.markdown import render_markdown, MarkdownVisitor


class MarkdownConverter(FormatConverter):
    """Converter for transforming between Nomenic and Markdown formats."""

    def extract_metadata(self, source: str) -> Dict[str, str]:
        """Extract metadata from Markdown frontmatter."""
        return self._extract_metadata(source)

    def _remove_frontmatter(self, source: str) -> str:
        """Remove Markdown frontmatter (--- ... ---) from source."""
        lines = source.splitlines()
        new_lines: List[str] = []
        in_frontmatter = False
        for line in lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue
            if not in_frontmatter:
                new_lines.append(line)
        # Remove leading blank lines after frontmatter
        while new_lines and new_lines[0].strip() == "":
            new_lines.pop(0)
        return "\n".join(new_lines)

    def to_nomenic(self, source: str, **options) -> str:
        """Convert Markdown to Nomenic format.

        Args:
            source: Markdown document as a string

        Returns:
            Nomenic document as a string
        """
        include_metadata = options.get("include_metadata", False)
        metadata = self.extract_metadata(source) if include_metadata else {}
        content = self._remove_frontmatter(source)
        lines = content.splitlines()
        nomenic_lines: List[str] = []
        current_list_level = 0
        in_code_block = False
        in_frontmatter = False

        # Process each line
        for line in lines:
            # Handle code blocks
            if line.startswith("```"):
                in_code_block = not in_code_block
                if in_code_block:
                    nomenic_lines.append("code:")
                else:
                    nomenic_lines.append("")
                continue

            if in_code_block:
                nomenic_lines.append(f"  {line}")
                continue

            # Handle frontmatter
            if line == "---":
                in_frontmatter = not in_frontmatter
                if in_frontmatter:
                    nomenic_lines.append("meta:")
                else:
                    nomenic_lines.append("")
                continue

            if in_frontmatter:
                if ":" in line:
                    key, value = line.split(":", 1)
                    nomenic_lines.append(f"  {key.strip()}: {value.strip()}")
                continue

            # Handle headers
            if line.startswith("#"):
                level = len(re.match(r"^#+", line).group())
                text = line.lstrip("#").strip()
                nomenic_lines.append(f"header: {text}")
                continue

            # Handle lists
            if line.startswith("- "):
                # Start new list if not already in one
                if current_list_level == 0:
                    nomenic_lines.append("list:")
                    current_list_level = 1
                indent = len(re.match(r"^\s*", line).group())
                text = line.lstrip("- ").strip()
                nomenic_lines.append(f"  - {text}")
                continue

            # Handle regular text
            if line.strip():
                nomenic_lines.append(f"text: {line}")
            else:
                nomenic_lines.append("")

        result = "\n".join(nomenic_lines)
        if include_metadata and metadata:
            meta_lines = ["meta:"]
            for key, val in metadata.items():
                meta_lines.append(f"  {key}: {val}")
            return "\n".join(meta_lines + ["", result])
        return result

    def from_nomenic(self, nomenic: str, **options) -> str:
        """Convert Nomenic to Markdown format.

        Args:
            nomenic: Nomenic document as a string

        Returns:
            Markdown document as a string
        """
        # Parse the Nomenic content into an AST
        ast = self._parse_nomenic(nomenic)

        # Render AST to Markdown
        from ..renderers.markdown import MarkdownVisitor
        visitor = MarkdownVisitor(include_frontmatter=False)
        body = visitor.render(ast)
        include_frontmatter = options.get("include_frontmatter", False)
        if include_frontmatter:
            metadata: Dict[str, str] = {}
            in_meta = False
            for line in nomenic.splitlines():
                if line.startswith("meta:"):
                    in_meta = True
                    continue
                if in_meta:
                    if not line.startswith("  "):
                        break
                    if ":" in line:
                        k, v = line.strip().split(":", 1)
                        metadata[k] = v.strip()
            if metadata:
                front = ["---"]
                for key, val in metadata.items():
                    front.append(f"{key}: {val}")
                front.append("---")
                return "\n".join(front + ["", body])
        return body

    def _extract_metadata(self, source: str) -> Dict[str, str]:
        """Extract metadata from Markdown frontmatter.

        Args:
            source: Markdown document as a string

        Returns:
            Dictionary of metadata key-value pairs
        """
        metadata: Dict[str, str] = {}
        in_frontmatter = False

        for line in source.splitlines():
            if line == "---":
                in_frontmatter = not in_frontmatter
                if not in_frontmatter:
                    break
                continue

            if in_frontmatter and ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        return metadata
