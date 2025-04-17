"""JSON converter for transforming between Nomenic and JSON formats."""

import json
from typing import Any, Dict, List, Optional

from .base import FormatConverter
from .. import Lexer, Parser
from ..ast import ASTNode, HeaderNode, TextNode, ListNode, ListItemNode
from ..renderers.json import render_json


class JSONConverter(FormatConverter):
    """Converter for transforming between Nomenic and JSON formats."""

    def extract_metadata(self, source: str) -> Dict[str, Any]:
        """Extract metadata dictionary from JSON content."""
        data = self._extract_metadata(source)
        if isinstance(data, dict) and "metadata" in data:
            return data["metadata"] or {}
        return {}

    def to_nomenic(self, source: str, **options) -> str:
        """Convert JSON to Nomenic format, including metadata and sections."""
        try:
            data = json.loads(source)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON") from e
        include_metadata = options.get('include_metadata', False)
        lines: List[str] = []
        # Metadata block: nested or flat
        if include_metadata:
            md = data.get('metadata')
            if not isinstance(md, dict):
                # collect top-level non-list values except sections
                md = {k: v for k, v in data.items() if k != 'sections' and not isinstance(v, list)}
            if md:
                lines.append('meta:')
                for k, v in md.items():
                    lines.append(f'  {k}: {v}')
                lines.append('')
        # Document sections
        # Determine document sections
        if isinstance(data, dict) and 'sections' in data and isinstance(data['sections'], list):
            sections = data['sections']
        elif isinstance(data, dict) and 'document' in data and isinstance(data['document'], list):
            sections = data['document']
        elif isinstance(data, list):
            sections = data
        else:
            sections = []
        for section in sections:
            t = section.get('type')
            if t in ('header', 'section'):
                title = section.get('content') or section.get('title', '')
                lines.append(f'header: {title}')
            elif t == 'text':
                lines.append(f'  text: {section.get("content", "")}')
            elif t == 'list':
                lines.append('  list:')
                for it in section.get('items', []):
                    lines.append(f'    - {it}')
            elif t == 'code':
                lines.append('  code:')
                lang = section.get('language')
                lines.append(f"    ```{lang}" if lang else '    ```')
                for ln in section.get('content', '').split('\n'):
                    lines.append(f'    {ln}')
                lines.append('    ```')
            else:
                # fallback generic
                lines.append(f'  {t}: {section}')
        return '\n'.join(lines)

    def from_nomenic(self, nomenic: str, **options) -> str:
        """Convert Nomenic to JSON format."""
        # Render JSON directly from Nomenic content
        pretty = options.get('pretty', False)
        include_content = options.get('include_content', False)
        return render_json(nomenic, pretty=pretty, include_content=include_content)

    def _extract_metadata(self, source: str) -> Dict[str, Any]:
        """Extract metadata from JSON document.

        Args:
            source: JSON document as a string

        Returns:
            Dictionary of metadata key-value pairs
        """
        try:
            return json.loads(source) or {}
        except json.JSONDecodeError:
            return {}
