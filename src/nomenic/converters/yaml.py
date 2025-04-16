"""YAML converter for Nomenic documents."""

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
    """Converter for YAML format."""
    
    def __init__(self):
        """Initialize YAML converter."""
        super().__init__()
        if not HAS_YAML:
            print("WARNING: PyYAML not installed. YAML conversion will be limited.")
            print("Install with: pip install pyyaml")
    
    def to_nomenic(self, source: str, **options) -> str:
        """Convert YAML to Nomenic.
        
        Args:
            source: YAML content
            **options: Additional conversion options
                include_metadata: Whether to include metadata (default: True)
                
        Returns:
            Nomenic-formatted content
        """
        # Extract options
        include_metadata = options.get('include_metadata', True)
        
        if not HAS_YAML:
            raise ImportError("PyYAML is required for YAML to Nomenic conversion. Install with: pip install pyyaml")
        
        try:
            # Parse YAML content
            yaml_data = yaml.safe_load(source)
            
            # Convert to Nomenic
            return self._yaml_to_nomenic(yaml_data, include_metadata)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML content: {e}")
    
    def from_nomenic(self, nomenic: str, **options) -> str:
        """Convert Nomenic to YAML.
        
        Args:
            nomenic: Nomenic content
            **options: Additional conversion options
                include_content: Whether to include raw content (default: True)
                
        Returns:
            YAML-formatted content
        """
        # Extract options
        include_content = options.get('include_content', True)
        
        # Use the existing YAML renderer
        return render_yaml(nomenic, include_content=include_content)
    
    def extract_metadata(self, source: str) -> Dict[str, Any]:
        """Extract metadata from YAML content.
        
        Args:
            source: YAML content
            
        Returns:
            Dictionary of metadata
        """
        if not HAS_YAML:
            return {}
            
        try:
            # Parse YAML content
            yaml_data = yaml.safe_load(source)
            
            # Extract metadata if available
            if isinstance(yaml_data, dict) and 'metadata' in yaml_data:
                return yaml_data['metadata']
            
            # Check for document-level metadata
            if isinstance(yaml_data, dict):
                # Look for common metadata fields
                metadata_fields = {'title', 'author', 'date', 'version', 'description', 'keywords', 'tags'}
                metadata = {}
                
                for field in metadata_fields:
                    if field in yaml_data:
                        metadata[field] = yaml_data[field]
                        
                if metadata:
                    return metadata
            
            return {}
        except yaml.YAMLError:
            return {}
    
    def _yaml_to_nomenic(self, yaml_data: Any, include_metadata: bool) -> str:
        """Convert YAML data to Nomenic format.
        
        Args:
            yaml_data: Parsed YAML data
            include_metadata: Whether to include metadata
            
        Returns:
            Nomenic-formatted content
        """
        lines = []
        metadata = {}
        
        # Extract metadata if available
        if isinstance(yaml_data, dict) and 'metadata' in yaml_data and include_metadata:
            metadata = yaml_data['metadata']
            
            # Add metadata block
            if metadata:
                lines.append("meta:")
                lines.extend(self._process_metadata(metadata))
                lines.append("")
        
        # Process document content
        if isinstance(yaml_data, dict):
            # Handle document structure
            if 'document' in yaml_data:
                content = yaml_data['document']
                lines.extend(self._process_yaml_document(content))
            elif 'content' in yaml_data:
                content = yaml_data['content']
                lines.extend(self._process_yaml_document(content))
            else:
                # Process the YAML object directly
                lines.extend(self._process_yaml_object(yaml_data, include_metadata))
        elif isinstance(yaml_data, list):
            # Process as a list of sections or items
            lines.extend(self._process_yaml_list(yaml_data))
            
        return "\n".join(lines)
    
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
                        lines.extend([f"{indent_str}  - {k}: {v}" for k, v in item.items()])
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
                            lines.extend(self._process_nested_content(sub_key, sub_value))
                    elif isinstance(value, list):
                        lines.append("  list:")
                        for item in value:
                            if isinstance(item, dict):
                                for item_key, item_value in item.items():
                                    lines.append(f"    - {item_key}: {item_value}")
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
                    lines.extend(self._process_nested_content(sub_key, sub_value))
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
                                lines.extend(self._process_nested_content(item_key, item_value, indent=6))
                            else:
                                item_str_parts.append(f"{item_key}: {item_value}")
                                
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
                        item_str = ", ".join(f"{k}: {v}" for k, v in list_item.items())
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
                    lines.extend(self._process_nested_content(sub_key, sub_value, indent + 2))
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
                            lines.extend(self._process_nested_content(sub_key, sub_value, indent + 4))
                else:
                    lines.append(f"{indent_str}- {item}")
        else:
            # Add as text
            lines.append(f"{indent_str[:-2]}text: {key}: {value}")
            
        return lines 