"""YAML converter for transforming between Nomenic and YAML formats."""

import sys
from typing import Any, Dict, Optional, List

# Try absolute imports first (recommended approach)
try:
    from nomenic import Lexer, Parser
    from nomenic.ast import DocumentNode
    from nomenic.renderers.yaml import render_yaml
    from nomenic.converters.base import FormatConverter
except ImportError:
    # Fall back to relative imports if absolute imports fail
    try:
        from .. import Lexer, Parser
        from ..ast import DocumentNode
        from ..renderers.yaml import render_yaml
        from .base import FormatConverter
    except ImportError:
        print("ERROR: Failed to import Nomenic core components. Please make sure the package is properly installed.")
        sys.exit(1)

# Try to import YAML parser
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class YAMLConverter(FormatConverter):
    """Converter for transforming between Nomenic and YAML formats."""

    def __init__(self):
        """Initialize YAML converter."""
        super().__init__()
        if not HAS_YAML:
            print("WARNING: PyYAML not installed. YAML conversion will be limited.")
            print("Install with: pip install pyyaml")

    def to_nomenic(self, source: str, **options) -> str:
        """Convert YAML to Nomenic format."""
        # Parse YAML into Python objects
        try:
            data = yaml.safe_load(source)
        except yaml.YAMLError as e:
            raise ValueError("Invalid YAML") from e
        # Determine metadata option
        include_metadata = options.get('include_metadata', False)
        metadata = self._extract_metadata(source) if include_metadata else {}
        # Convert to Nomenic format
        nomenic_lines: List[str] = []

        def convert_to_nomenic(obj: Any, indent: int = 0) -> None:
            """Recursively convert YAML data to Nomenic format."""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, (dict, list)):
                        nomenic_lines.append(f"{'  ' * indent}{key}:")
                        convert_to_nomenic(value, indent + 1)
                    else:
                        nomenic_lines.append(f"{'  ' * indent}{key}: {value}")
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, (dict, list)):
                        nomenic_lines.append(f"{'  ' * indent}list:")
                        convert_to_nomenic(item, indent + 1)
                    else:
                        nomenic_lines.append(f"{'  ' * indent}- {item}")
            else:
                nomenic_lines.append(f"{'  ' * indent}text: {obj}")

        convert_to_nomenic(data)
        result = "\n".join(nomenic_lines)
        if include_metadata and metadata:
            meta_lines = ["meta:"]
            for key, val in metadata.items():
                meta_lines.append(f"  {key}: {val}")
            return "\n".join(meta_lines + ["", result])
        return result

    def from_nomenic(self, nomenic: str, **options) -> str:
        """Convert Nomenic to YAML format."""
        include_content = options.get('include_content', False)
        return render_yaml(nomenic, include_content=include_content)

    def _extract_metadata(self, source: str) -> Dict[str, Any]:
        """Extract metadata from YAML document.

        Args:
            source: YAML document as a string

        Returns:
            Dictionary of metadata key-value pairs
        """
        try:
            return yaml.safe_load(source) or {}
        except yaml.YAMLError:
            return {}

    def _parse_nomenic(self, nomenic: str) -> DocumentNode:
        # Implementation of _parse_nomenic method
        # This method should return a DocumentNode object
        # For now, we'll keep it as a placeholder
        return DocumentNode()  # Placeholder return, actual implementation needed

    def _process_metadata(self, metadata: Dict[str, Any], indent: int = 2) -> List[str]:
        """Process metadata into Nomenic format.

        Args:
            metadata: Metadata dictionary
            indent: Indentation level

        Returns:
            List of Nomenic lines
        """
        lines = []
        indent_str = " " * indent

        for key, value in metadata.items():
            if isinstance(value, dict):
                lines.append(f"{indent_str}{key}:")
                lines.extend(self._process_metadata(value, indent + 2))
            elif isinstance(value, list):
                lines.append(f"{indent_str}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        lines.extend(
                            [f"{indent_str}  - {k}: {v}" for k, v in item.items()])
                    else:
                        lines.append(f"{indent_str}  - {item}")
            else:
                lines.append(f"{indent_str}{key}: {value}")

        return lines

    def _process_yaml_document(self, content: Any) -> List[str]:
        """Process a YAML document structure.

        Args:
            content: Document content

        Returns:
            List of Nomenic lines
        """
        lines = []

        if isinstance(content, dict):
            # Process sections
            for key, value in content.items():
                if key in ('headers', 'header'):
                    if isinstance(value, list):
                        for header in value:
                            lines.extend(self._process_header(header))
                    else:
                        lines.extend(self._process_header(value))
                elif key == 'sections':
                    if isinstance(value, list):
                        for section in value:
                            lines.extend(self._process_section(section))
                    else:
                        lines.extend(self._process_section(value))
                elif key == 'content':
                    if isinstance(value, list):
                        for item in value:
                            lines.extend(self._process_content_item(item))
                    else:
                        lines.append(f"  text: {value}")
                elif key not in ('metadata'):  # Skip metadata as it's handled separately
                    # Treat as a section
                    lines.append(f"header: {key}")

                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            lines.extend(self._process_nested_content(
                                sub_key, sub_value))
                    elif isinstance(value, list):
                        lines.append("  list:")
                        for item in value:
                            if isinstance(item, dict):
                                for item_key, item_value in item.items():
                                    lines.append(
                                        f"    - {item_key}: {item_value}")
                            else:
                                lines.append(f"    - {item}")
                    else:
                        lines.append(f"  text: {value}")
        elif isinstance(content, list):
            # Process as a list of sections or content items
            for item in content:
                if isinstance(item, dict) and any(key in item for key in ('header', 'title', 'section')):
                    lines.extend(self._process_section(item))
                else:
                    lines.extend(self._process_content_item(item))

        return lines

    def _process_yaml_object(self, obj: Dict[str, Any], skip_metadata: bool = False) -> List[str]:
        """Process a YAML object.

        Args:
            obj: YAML object
            skip_metadata: Whether to skip metadata fields

        Returns:
            List of Nomenic lines
        """
        lines = []

        for key, value in obj.items():
            # Skip metadata if requested
            if skip_metadata and key == 'metadata':
                continue

            if key in ('header', 'title'):
                lines.append(f"header: {value}")
            elif isinstance(value, dict):
                # Process as a section with nested content
                lines.append(f"header: {key}")

                for sub_key, sub_value in value.items():
                    lines.extend(self._process_nested_content(
                        sub_key, sub_value))
            elif isinstance(value, list):
                # Process as a section with a list
                lines.append(f"header: {key}")
                lines.append("  list:")

                for item in value:
                    if isinstance(item, dict):
                        # Handle complex list items
                        item_str_parts = []

                        for item_key, item_value in item.items():
                            if isinstance(item_value, (dict, list)):
                                # For complex nested structures, add as separate content
                                lines.append(f"    - {item_key}")
                                lines.extend(self._process_nested_content(
                                    item_key, item_value, indent=6))
                            else:
                                item_str_parts.append(
                                    f"{item_key}: {item_value}")

                        if item_str_parts:
                            lines.append(f"    - {', '.join(item_str_parts)}")
                    else:
                        lines.append(f"    - {item}")
            else:
                # Process as a simple section with text
                lines.append(f"header: {key}")
                lines.append(f"  text: {value}")

        return lines

    def _process_yaml_list(self, items: List[Any]) -> List[str]:
        """Process a YAML list.

        Args:
            items: YAML list

        Returns:
            List of Nomenic lines
        """
        lines = []

        # Check if this is a list of simple items
        if all(isinstance(item, (str, int, float, bool)) for item in items):
            lines.append("list:")
            for item in items:
                lines.append(f"  - {item}")
        else:
            # Process as list of sections or content items
            for item in items:
                if isinstance(item, dict):
                    if any(key in item for key in ('header', 'title', 'section')):
                        lines.extend(self._process_section(item))
                    else:
                        lines.extend(self._process_content_item(item))
                else:
                    lines.append(f"  text: {item}")

        return lines

    def _process_header(self, header: Any) -> List[str]:
        """Process a header item.

        Args:
            header: Header content

        Returns:
            List of Nomenic lines
        """
        lines = []

        if isinstance(header, dict):
            if 'text' in header:
                lines.append(f"header: {header['text']}")
            elif 'title' in header:
                lines.append(f"header: {header['title']}")
            elif 'content' in header:
                lines.append(f"header: {header['content']}")

            # Process header level if available
            if 'level' in header:
                # Adjust indentation based on level
                level = int(header['level'])
                prefix = "  " * (level - 1)
                lines[-1] = f"{prefix}header: {lines[-1].split(':', 1)[1].strip()}"
        else:
            lines.append(f"header: {header}")

        return lines

    def _process_section(self, section: Dict[str, Any]) -> List[str]:
        """Process a section item.

        Args:
            section: Section content

        Returns:
            List of Nomenic lines
        """
        lines = []

        # Process section header
        if 'header' in section:
            lines.append(f"header: {section['header']}")
        elif 'title' in section:
            lines.append(f"header: {section['title']}")
        elif 'section' in section:
            lines.append(f"header: {section['section']}")

        # Process section content
        if 'content' in section:
            content = section['content']

            if isinstance(content, list):
                for item in content:
                    lines.extend(self._process_content_item(item))
            elif isinstance(content, dict):
                for key, value in content.items():
                    lines.extend(self._process_nested_content(key, value))
            else:
                lines.append(f"  text: {content}")
        elif 'text' in section:
            lines.append(f"  text: {section['text']}")
        elif 'list' in section:
            lines.append("  list:")

            for item in section['list']:
                if isinstance(item, dict):
                    item_str = ", ".join(f"{k}: {v}" for k, v in item.items())
                    lines.append(f"    - {item_str}")
                else:
                    lines.append(f"    - {item}")
        elif 'code' in section:
            lines.append("  code:")
            code_content = section['code']
            language = section.get('language', '')

            if language:
                lines.append(f"    ```{language}")
            else:
                lines.append("    ```")

            for code_line in code_content.split('\n'):
                lines.append(f"    {code_line}")

            lines.append("    ```")

        return lines

    def _process_content_item(self, item: Any) -> List[str]:
        """Process a content item.

        Args:
            item: Content item

        Returns:
            List of Nomenic lines
        """
        lines = []

        if isinstance(item, dict):
            if 'text' in item:
                lines.append(f"  text: {item['text']}")
            elif 'list' in item:
                lines.append("  list:")

                for list_item in item['list']:
                    if isinstance(list_item, dict):
                        item_str = ", ".join(
                            f"{k}: {v}" for k, v in list_item.items())
                        lines.append(f"    - {item_str}")
                    else:
                        lines.append(f"    - {list_item}")
            elif 'code' in item:
                lines.append("  code:")
                code_content = item['code']
                language = item.get('language', '')

                if language:
                    lines.append(f"    ```{language}")
                else:
                    lines.append("    ```")

                for code_line in code_content.split('\n'):
                    lines.append(f"    {code_line}")

                lines.append("    ```")
            else:
                # Handle generic item
                for key, value in item.items():
                    if isinstance(value, (dict, list)):
                        lines.extend(self._process_nested_content(key, value))
                    else:
                        lines.append(f"  text: {key}: {value}")
        elif isinstance(item, str):
            lines.append(f"  text: {item}")

        return lines

    def _process_nested_content(self, key: str, value: Any, indent: int = 4) -> List[str]:
        """Process nested content from YAML.

        Args:
            key: Content key
            value: Content value
            indent: Indentation level

        Returns:
            List of Nomenic lines
        """
        lines = []
        indent_str = " " * indent

        if isinstance(value, dict):
            # Add as a nested section
            lines.append(f"{indent_str[:-2]}header: {key}")

            for sub_key, sub_value in value.items():
                if isinstance(sub_value, (dict, list)):
                    lines.extend(self._process_nested_content(
                        sub_key, sub_value, indent + 2))
                else:
                    lines.append(f"{indent_str}text: {sub_key}: {sub_value}")
        elif isinstance(value, list):
            # Add as a list
            lines.append(f"{indent_str[:-2]}list:")

            for item in value:
                if isinstance(item, dict):
                    item_str = ", ".join(f"{k}: {v}" for k, v in item.items()
                                         if not isinstance(v, (dict, list)))

                    if item_str:
                        lines.append(f"{indent_str}- {item_str}")

                    # Process any complex nested structures
                    for sub_key, sub_value in item.items():
                        if isinstance(sub_value, (dict, list)):
                            lines.extend(self._process_nested_content(
                                sub_key, sub_value, indent + 4))
                else:
                    lines.append(f"{indent_str}- {item}")
        else:
            # Add as text
            lines.append(f"{indent_str[:-2]}text: {key}: {value}")

        return lines
