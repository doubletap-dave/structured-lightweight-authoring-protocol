"""JSON renderer for Nomenic documents."""

import json
import sys
from typing import Any, Dict, List, Optional, Union

# Try absolute imports first (recommended approach)
try:
    from nomenic import Lexer, Parser
    from nomenic.ast import (
        ASTNode,
        BlockNode,
        DocumentNode,
        HeaderNode,
        ListNode,
        TextNode,
        Visitor,
    )
except ImportError:
    # Fall back to relative imports if absolute imports fail
    try:
        from .. import Lexer, Parser
        from ..ast import (
            ASTNode,
            BlockNode,
            DocumentNode,
            HeaderNode,
            ListNode,
            TextNode,
            Visitor,
        )
    except ImportError:
        print("ERROR: Failed to import Nomenic core components. Please make sure the package is properly installed.")
        sys.exit(1)


class JSONRendererVisitor(Visitor):
    """Visitor that renders AST nodes as JSON structures."""

    def __init__(self, pretty: bool = True, include_content: bool = True):
        """
        Initialize the JSON renderer visitor.

        Args:
            pretty: Whether to generate pretty (indented) JSON
            include_content: Whether to include full content or just structure
        """
        self.pretty = pretty
        self.include_content = include_content
        self.result: Dict[str, Any] = {}
        
    def visit_document(self, node: DocumentNode) -> Dict[str, Any]:
        """Process a document node into a JSON dictionary."""
        result = {}
        
        # Process metadata first
        meta_block = next(
            (child for child in node.children 
             if isinstance(child, BlockNode) and child.block_type == "meta"),
            None
        )
        
        # Add metadata if present
        if meta_block and hasattr(meta_block, 'meta') and meta_block.meta:
            for key, value in meta_block.meta.items():
                # Skip internal metadata
                if key.startswith("_"):
                    continue
                result[key] = value
        
        # Add document content
        sections = []
        
        for child in node.children:
            # Skip meta block, already processed
            if isinstance(child, BlockNode) and child.block_type == "meta":
                continue
                
            sections.append(child.accept(self))
        
        result["sections"] = sections
        return result
        
    def visit_header(self, node: HeaderNode) -> Dict[str, Any]:
        """Process a header node into a JSON dictionary."""
        return {
            "type": "section",
            "title": node.text,
            "level": node.level,
            "content": []
        }
        
    def visit_text(self, node: TextNode) -> Dict[str, Any]:
        """Process a text node into a JSON dictionary."""
        if self.include_content:
            return {
                "type": "text",
                "content": node.text
            }
        else:
            return {
                "type": "text"
            }
        
    def visit_list(self, node: ListNode) -> Dict[str, Any]:
        """Process a list node into a JSON dictionary."""
        items = []
        for item in node.items:
            if isinstance(item, TextNode):
                items.append(item.text if self.include_content else {"type": "text"})
            else:
                # Handle more complex items by accepting them as visitors
                items.append(item.accept(self))
                
        return {
            "type": "list",
            "ordered": node.ordered,
            "items": items
        }
        
    def visit_block(self, node: BlockNode) -> Dict[str, Any]:
        """Process a block node into a JSON dictionary."""
        if node.block_type == "meta":
            return self._process_meta_block(node)
        elif node.block_type == "code":
            return self._process_code_block(node)
        elif node.block_type == "table":
            return self._process_table_block(node)
        elif node.block_type in ("section", "note", "callout"):
            return self._process_semantic_block(node)
        else:
            return self._process_generic_block(node)
                
    def _process_meta_block(self, node: BlockNode) -> Dict[str, Any]:
        """Process a metadata block."""
        if self.include_content and hasattr(node, 'meta') and node.meta:
            return {
                "type": "meta",
                "metadata": {key: value for key, value in node.meta.items() 
                             if not key.startswith("_")}
            }
        else:
            return {
                "type": "meta"
            }
            
    def _process_code_block(self, node: BlockNode) -> Dict[str, Any]:
        """Process a code block into a JSON dictionary."""
        code_content = ""
        language = None
        
        # Extract content from child nodes
        if node.children and isinstance(node.children[0], TextNode):
            code_content = node.children[0].text
        
        # Get language from metadata if available
        if node.meta and "language" in node.meta:
            language = node.meta["language"]
            
        if self.include_content:
            result = {
                "type": "code",
                "content": code_content
            }
            
            if language:
                result["language"] = language
                
            return result
        else:
            return {
                "type": "code"
            }
            
    def _process_table_block(self, node: BlockNode) -> Dict[str, Any]:
        """Process a table block into a JSON dictionary."""
        rows = []
        
        for child in node.children:
            if isinstance(child, TextNode):
                # Split by pipes and clean up
                columns = [col.strip() for col in child.text.split("|")]
                rows.append(columns)
        
        if self.include_content:
            return {
                "type": "table",
                "rows": rows
            }
        else:
            return {
                "type": "table"
            }
            
    def _process_semantic_block(self, node: BlockNode) -> Dict[str, Any]:
        """Process a semantic block (section, note, callout)."""
        title = ""
        content = []
        
        # Extract title and content
        if node.children and isinstance(node.children[0], TextNode):
            title = node.children[0].text
            
            # Process remaining children
            for child in node.children[1:]:
                content.append(child.accept(self))
        
        if self.include_content:
            result = {
                "type": node.block_type,
                "title": title
            }
            
            if content:
                result["content"] = content
                
            return result
        else:
            return {
                "type": node.block_type
            }
            
    def _process_generic_block(self, node: BlockNode) -> Dict[str, Any]:
        """Process a generic block node."""
        if self.include_content:
            content = []
            
            for child in node.children:
                if isinstance(child, TextNode):
                    content.append({"type": "text", "content": child.text})
                else:
                    content.append(child.accept(self))
            
            return {
                "type": node.block_type,
                "content": content
            }
        else:
            return {
                "type": node.block_type
            }

    def render(self, document: DocumentNode) -> Dict[str, Any]:
        """Render a document into a dictionary structure."""
        return document.accept(self)


def render_json(content: str, pretty: bool = True, include_content: bool = True) -> str:
    """
    Render a Nomenic document as JSON.

    Args:
        content: The Nomenic document content
        pretty: Whether to generate pretty (indented) JSON
        include_content: Whether to include full content or just structure

    Returns:
        JSON representation of the document
    """
    # Parse the document
    lexer = Lexer(content)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    document = parser.parse()
    
    # Use the visitor to generate JSON structure
    visitor = JSONRendererVisitor(pretty=pretty, include_content=include_content)
    result = visitor.render(document)
    
    # Convert to JSON string
    indent = 2 if pretty else None
    return json.dumps(result, indent=indent) 