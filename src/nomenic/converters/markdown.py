"""Markdown converter for Nomenic documents."""

import re
import sys
from typing import Any, Dict, Optional

# Try absolute imports first (recommended approach)
try:
    from nomenic import Lexer, Parser
    from nomenic.ast import DocumentNode
    from nomenic.renderers.markdown import render_markdown
    from nomenic.converters.base import FormatConverter
except ImportError:
    # Fall back to relative imports if absolute imports fail
    try:
        from .. import Lexer, Parser
        from ..ast import DocumentNode
        from ..renderers.markdown import render_markdown
        from .base import FormatConverter
    except ImportError:
        print("ERROR: Failed to import Nomenic core components. Please make sure the package is properly installed.")
        sys.exit(1)


class MarkdownConverter(FormatConverter):
    """Converter for markdown format."""
    
    def __init__(self):
        """Initialize markdown converter."""
        super().__init__()
        
    def to_nomenic(self, markdown: str, **options) -> str:
        """Convert markdown to Nomenic.
        
        Args:
            markdown: Markdown content
            **options: Additional conversion options
                include_metadata: Whether to include metadata (default: True)
                preserve_formatting: Whether to preserve original formatting where possible (default: True)
                
        Returns:
            Nomenic-formatted content
        """
        # Extract options
        include_metadata = options.get('include_metadata', True)
        preserve_formatting = options.get('preserve_formatting', True)
        
        # Extract metadata from frontmatter if present
        metadata = {}
        content = markdown
        if include_metadata:
            metadata = self.extract_metadata(markdown)
            # Remove frontmatter from content if present
            content = self._remove_frontmatter(markdown)
        
        # Convert markdown content to Nomenic
        nomenic_content = self._markdown_to_nomenic(content, preserve_formatting)
        
        # Apply metadata if needed
        if include_metadata and metadata:
            nomenic_content = self._apply_nomenic_metadata(nomenic_content, metadata)
            
        return nomenic_content
    
    def from_nomenic(self, nomenic: str, **options) -> str:
        """Convert Nomenic to markdown.
        
        Args:
            nomenic: Nomenic content
            **options: Additional conversion options
                include_frontmatter: Whether to include frontmatter (default: True)
                
        Returns:
            Markdown-formatted content
        """
        # Extract options
        include_frontmatter = options.get('include_frontmatter', True)
        
        # Use the existing markdown renderer
        return render_markdown(nomenic, include_frontmatter=include_frontmatter)
    
    def extract_metadata(self, markdown: str) -> Dict[str, Any]:
        """Extract metadata from markdown frontmatter.
        
        Args:
            markdown: Markdown content
            
        Returns:
            Dictionary of metadata
        """
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', markdown, re.DOTALL)
        if not frontmatter_match:
            return {}
        
        frontmatter = frontmatter_match.group(1)
        metadata = {}
        
        # Simple YAML-like parsing
        for line in frontmatter.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Handle nested properties (basic implementation)
                if key in metadata and isinstance(metadata[key], dict) and ': ' in value:
                    nested_key, nested_value = value.split(': ', 1)
                    metadata[key][nested_key.strip()] = nested_value.strip()
                else:
                    metadata[key] = value
        
        return metadata
    
    def _remove_frontmatter(self, markdown: str) -> str:
        """Remove frontmatter from markdown content.
        
        Args:
            markdown: Markdown content
            
        Returns:
            Markdown content without frontmatter
        """
        return re.sub(r'^---\s*\n.*?\n---\s*\n', '', markdown, flags=re.DOTALL)
    
    def _markdown_to_nomenic(self, markdown: str, preserve_formatting: bool) -> str:
        """Convert markdown content to Nomenic format.
        
        Args:
            markdown: Markdown content without frontmatter
            preserve_formatting: Whether to preserve original formatting
            
        Returns:
            Nomenic-formatted content
        """
        # TODO: Implement markdown parsing logic
        # This would require a proper markdown parser to build an AST
        # and then convert it to Nomenic format
        
        # For now, we'll implement a basic converter using regex patterns
        # This is a limited implementation and should be replaced with proper parsing
        
        # Convert headers
        content = re.sub(r'^# (.*?)$', r'header: \1', markdown, flags=re.MULTILINE)
        content = re.sub(r'^## (.*?)$', r'  header: \1', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.*?)$', r'    header: \1', content, flags=re.MULTILINE)
        
        # Convert lists
        content = re.sub(r'^\s*- (.*?)$', r'  list:\n    - \1', content, flags=re.MULTILINE)
        
        # Convert code blocks
        content = re.sub(r'```(\w*)\n(.*?)```', r'  code:\n    ```\1\n    \2```', content, flags=re.DOTALL)
        
        # Convert inline formatting
        content = re.sub(r'\*\*(.*?)\*\*', r'@b(\1)', content)
        content = re.sub(r'\*(.*?)\*', r'@i(\1)', content)
        content = re.sub(r'`(.*?)`', r'@c(\1)', content)
        content = re.sub(r'\[(.*?)\]\((.*?)\)', r'@l(\1)', content)
        
        # Basic structure
        # Ensure there's a text node for paragraphs that aren't part of a structure
        lines = []
        in_structure = False
        
        for line in content.split('\n'):
            if line.strip().startswith(('header:', 'list:', 'code:', '  -')):
                in_structure = True
                lines.append(line)
            elif line.strip() == '':
                in_structure = False
                lines.append(line)
            elif not in_structure and line.strip():
                # Add text: prefix for regular paragraphs
                lines.append(f"  text: {line}")
                in_structure = True
            else:
                lines.append(line)
                
        return '\n'.join(lines)
    
    def _apply_nomenic_metadata(self, content: str, metadata: Dict[str, Any]) -> str:
        """Apply metadata to Nomenic content.
        
        Args:
            content: Nomenic content
            metadata: Metadata to apply
            
        Returns:
            Nomenic content with metadata
        """
        # Convert metadata to Nomenic format
        meta_lines = ['meta:']
        
        for key, value in metadata.items():
            if isinstance(value, dict):
                meta_lines.append(f"  {key}:")
                for sub_key, sub_value in value.items():
                    meta_lines.append(f"    {sub_key}: {sub_value}")
            else:
                meta_lines.append(f"  {key}: {value}")
        
        meta_block = '\n'.join(meta_lines)
        
        # Add metadata at the beginning of the document
        return f"{meta_block}\n\n{content}" 