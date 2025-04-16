"""JSON converter for Nomenic documents."""

import json
import sys
from typing import Any, Dict, Optional

# Try absolute imports first (recommended approach)
try:
    from nomenic import Lexer, Parser
    from nomenic.ast import DocumentNode
    from nomenic.renderers.json import render_json
    from nomenic.converters.base import FormatConverter
except ImportError:
    # Fall back to relative imports if absolute imports fail
    try:
        from .. import Lexer, Parser
        from ..ast import DocumentNode
        from ..renderers.json import render_json
        from .base import FormatConverter
    except ImportError:
        print("ERROR: Failed to import Nomenic core components. Please make sure the package is properly installed.")
        sys.exit(1)


class JSONConverter(FormatConverter):
    """Converter for JSON format."""
    
    def __init__(self):
        """Initialize JSON converter."""
        super().__init__()
    
    def to_nomenic(self, source: str, **options) -> str:
        """Convert JSON to Nomenic.
        
        Args:
            source: JSON content
            **options: Additional conversion options
                include_metadata: Whether to include metadata (default: True)
                
        Returns:
            Nomenic-formatted content
        """
        # Extract options
        include_metadata = options.get('include_metadata', True)
        
        try:
            # Parse JSON content
            json_data = json.loads(source)
            
            # Convert to Nomenic
            return self._json_to_nomenic(json_data, include_metadata)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON content: {e}")
    
    def from_nomenic(self, nomenic: str, **options) -> str:
        """Convert Nomenic to JSON.
        
        Args:
            nomenic: Nomenic content
            **options: Additional conversion options
                pretty: Whether to pretty-print JSON (default: True)
                include_content: Whether to include raw content (default: True)
                
        Returns:
            JSON-formatted content
        """
        # Extract options
        pretty = options.get('pretty', True)
        include_content = options.get('include_content', True)
        
        # Use the existing JSON renderer
        return render_json(
            nomenic, 
            pretty=pretty, 
            include_content=include_content
        )
    
    def extract_metadata(self, source: str) -> Dict[str, Any]:
        """Extract metadata from JSON content.
        
        Args:
            source: JSON content
            
        Returns:
            Dictionary of metadata
        """
        try:
            # Parse JSON content
            json_data = json.loads(source)
            
            # Extract metadata if available
            if isinstance(json_data, dict) and 'metadata' in json_data:
                return json_data['metadata']
            
            return {}
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def _json_to_nomenic(self, json_data: Any, include_metadata: bool) -> str:
        """Convert JSON data to Nomenic format.
        
        Args:
            json_data: Parsed JSON data
            include_metadata: Whether to include metadata
            
        Returns:
            Nomenic-formatted content
        """
        lines = []
        metadata = {}
        
        # Extract metadata if available
        if isinstance(json_data, dict) and 'metadata' in json_data and include_metadata:
            metadata = json_data['metadata']
            
            # Add metadata block
            if metadata:
                lines.append("meta:")
                for key, value in metadata.items():
                    if isinstance(value, dict):
                        lines.append(f"  {key}:")
                        for sub_key, sub_value in value.items():
                            lines.append(f"    {sub_key}: {sub_value}")
                    elif isinstance(value, list):
                        lines.append(f"  {key}:")
                        for item in value:
                            lines.append(f"    - {item}")
                    else:
                        lines.append(f"  {key}: {value}")
                lines.append("")
        
        # Process document content
        if isinstance(json_data, dict):
            # Handle document structure with sections
            if 'document' in json_data:
                content = json_data['document']
                lines.extend(self._process_json_document(content))
            elif 'content' in json_data:
                content = json_data['content']
                lines.extend(self._process_json_document(content))
            else:
                # Process the JSON object directly
                lines.extend(self._process_json_object(json_data))
        elif isinstance(json_data, list):
            # Process as a list of sections
            lines.extend(self._process_json_list(json_data))
            
        return "\n".join(lines)
    
    def _process_json_document(self, content: Any) -> list:
        """Process a JSON document structure.
        
        Args:
            content: Document content
            
        Returns:
            List of Nomenic lines
        """
        lines = []
        
        if isinstance(content, dict):
            # Process sections
            for key, value in content.items():
                if key == 'headers':
                    for header in value:
                        lines.extend(self._process_header(header))
                elif key == 'sections':
                    for section in value:
                        lines.extend(self._process_section(section))
                elif key == 'content':
                    if isinstance(value, list):
                        for item in value:
                            lines.extend(self._process_content_item(item))
                    else:
                        lines.append(f"  text: {value}")
        elif isinstance(content, list):
            # Process as a list of sections or content items
            for item in content:
                if isinstance(item, dict) and 'header' in item:
                    lines.extend(self._process_section(item))
                else:
                    lines.extend(self._process_content_item(item))
                    
        return lines
    
    def _process_json_object(self, obj: Dict[str, Any]) -> list:
        """Process a JSON object.
        
        Args:
            obj: JSON object
            
        Returns:
            List of Nomenic lines
        """
        lines = []
        
        for key, value in obj.items():
            # Skip metadata as it's handled separately
            if key == 'metadata':
                continue
                
            if key == 'header' or key == 'title':
                lines.append(f"header: {value}")
            elif isinstance(value, dict):
                lines.append(f"header: {key}")
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, list):
                        lines.append(f"  list:")
                        for item in sub_value:
                            lines.append(f"    - {item}")
                    elif isinstance(sub_value, dict):
                        lines.append(f"  header: {sub_key}")
                        for k, v in sub_value.items():
                            lines.append(f"    text: {k}: {v}")
                    else:
                        lines.append(f"  text: {sub_key}: {sub_value}")
            elif isinstance(value, list):
                lines.append(f"header: {key}")
                lines.append("  list:")
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            lines.append(f"    - {k}: {v}")
                    else:
                        lines.append(f"    - {item}")
            else:
                lines.append(f"header: {key}")
                lines.append(f"  text: {value}")
                
        return lines
    
    def _process_json_list(self, items: list) -> list:
        """Process a JSON list.
        
        Args:
            items: JSON list
            
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
                    if 'header' in item or 'title' in item:
                        lines.extend(self._process_section(item))
                    else:
                        lines.extend(self._process_content_item(item))
                else:
                    lines.extend(self._process_content_item(item))
                    
        return lines
    
    def _process_header(self, header: Any) -> list:
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
            # Process header level if available
            if 'level' in header:
                # Adjust indentation based on level
                prefix = "  " * (int(header['level']) - 1)
                lines[-1] = f"{prefix}header: {lines[-1].split(':', 1)[1].strip()}"
        else:
            lines.append(f"header: {header}")
            
        return lines
    
    def _process_section(self, section: Dict[str, Any]) -> list:
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
            
        # Process section content
        if 'content' in section:
            content = section['content']
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and ('text' in item or 'content' in item):
                        text = item.get('text', item.get('content', ''))
                        lines.append(f"  text: {text}")
                    elif isinstance(item, dict) and 'list' in item:
                        lines.append("  list:")
                        for list_item in item['list']:
                            lines.append(f"    - {list_item}")
                    elif isinstance(item, dict) and 'code' in item:
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
                        lines.append(f"  text: {item}")
            else:
                lines.append(f"  text: {content}")
                
        return lines
    
    def _process_content_item(self, item: Any) -> list:
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
                # Generic object processing
                for key, value in item.items():
                    if isinstance(value, (str, int, float, bool)):
                        lines.append(f"  text: {key}: {value}")
                    elif isinstance(value, list):
                        lines.append(f"  header: {key}")
                        lines.append("    list:")
                        for list_item in value:
                            lines.append(f"      - {list_item}")
        elif isinstance(item, str):
            lines.append(f"  text: {item}")
            
        return lines 