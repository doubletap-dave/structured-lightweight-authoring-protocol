"""Markdown renderer for Nomenic documents."""

import re
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
        Visitor,  # Import Visitor protocol
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
            Visitor,  # Import Visitor protocol
        )
    except ImportError:
        print("ERROR: Failed to import Nomenic core components. Please make sure the package is properly installed.")
        sys.exit(1)


class MarkdownVisitor(Visitor):
    """Visitor to render Nomenic AST as Markdown."""

    def __init__(self, include_frontmatter: bool = True):
        self.include_frontmatter = include_frontmatter
        self.parts: List[str] = []
        self.current_depth = 0 # Tracks header depth

    def render(self, document: DocumentNode) -> str:
        """Render the document by visiting the root node."""
        document.accept(self)
        
        # Remove trailing empty lines
        while self.parts and self.parts[-1] == "":
            self.parts.pop()
            
        return "\n".join(self.parts)

    def visit_document(self, node: DocumentNode):
        """Visit the root document node."""
        meta_block = None
        
        # First, look for metadata to put in frontmatter
        for child in node.children:
            if isinstance(child, BlockNode) and child.block_type == "meta":
                meta_block = child
                break

        # Add frontmatter if present and requested
        if self.include_frontmatter and meta_block and hasattr(meta_block, 'meta') and meta_block.meta:
            self.parts.append("---")
            for key, value in meta_block.meta.items():
                if key.startswith("_"): continue # Skip internal metadata
                
                # Basic YAML serialization (can be improved)
                if isinstance(value, (dict, list)):
                    self.parts.append(f"{key}:")
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            self.parts.append(f"  {sub_key}: {sub_value}")
                    else: # list
                        for item in value:
                            self.parts.append(f"  - {item}")
                else:
                    self.parts.append(f"{key}: {value}")
            self.parts.append("---")
            self.parts.append("")

        # Process the rest of the document children
        for child in node.children:
            # Skip meta block if already processed
            if isinstance(child, BlockNode) and child.block_type == "meta":
                continue
            child.accept(self)
            # Add spacing after most block elements
            if not isinstance(child, TextNode):
                 self.parts.append("")

    def visit_header(self, node: HeaderNode):
        """Visit a header node."""
        # Determine header level based on node's level attribute
        # We assume level 1 is top-level, adjust based on actual AST structure if needed
        header_level = "#" * node.level 
        # Process inline formatting within the header text
        processed_text = self._process_inline_formatting(node.text)
        self.parts.append(f"{header_level} {processed_text}")
        # Reset depth tracking if needed? Or pass depth down?
        # For now, assume HeaderNode.level is authoritative

    def visit_text(self, node: TextNode):
        """Visit a text node."""
        processed_text = self._process_inline_formatting(node.text)
        
        # Check if this is a section title - use a more generic approach
        # This is a heuristic approach that might need refinement based on actual document structure
        if processed_text and processed_text.strip() and not processed_text.startswith(('#', '>', '-', '*', '```', '|')):
            # Look for specific patterns that indicate section titles
            # For example, if it's short, not part of a list, and not in metadata
            if len(processed_text.strip().split()) <= 5 and ":" not in processed_text:
                self.parts.append(f"## {processed_text}")
                return
        
        # Avoid adding empty paragraphs
        if processed_text.strip():
            self.parts.append(processed_text)

    def visit_list(self, node: ListNode):
        """Visit a list node."""
        # Store current parts to handle nested lists correctly
        original_parts = self.parts
        self.parts = []

        for item in node.items:
            # Each item needs its own context
            item_visitor = MarkdownVisitor(include_frontmatter=False) # Avoid nested frontmatter
            # Set depth? Visitor needs depth tracking for nested lists.
            # Let's assume simple list for now
            item_result = item_visitor.render(item) if isinstance(item, DocumentNode) else item_visitor._render_single_node_to_string(item)
            
            # Indent nested content? Markdown doesn't always require explicit indent for sub-blocks
            # Basic list item rendering:
            self.parts.append(f"- {item_result.strip()}") 

        # Get the rendered list items
        rendered_items = "\n".join(self.parts)
        
        # Restore original parts and add the rendered list
        self.parts = original_parts
        self.parts.append(rendered_items)
        
    def _render_single_node_to_string(self, node: ASTNode) -> str:
        """Helper to render a single node (used for list items etc.)."""
        temp_visitor = MarkdownVisitor(include_frontmatter=False)
        node.accept(temp_visitor)
        return "\n".join(temp_visitor.parts)

    def visit_block(self, node: BlockNode):
        """Visit a generic or specific block node (code, table, etc.)."""
        if node.block_type == "code":
            self._visit_code_block(node)
        elif node.block_type == "section":
            # Format section blocks as markdown headers
            if node.children and isinstance(node.children[0], TextNode):
                section_title = node.children[0].text.strip()
                self.parts.append(f"## {section_title}")
                # Process any remaining children
                for child in node.children[1:]:
                    child.accept(self)
            else:
                # Handle empty sections or non-standard sections
                self.parts.append(f"## {node.block_type}")
        elif node.block_type == "note":
            # Format notes as markdown callouts
            if node.children and isinstance(node.children[0], TextNode):
                note_text = node.children[0].text.strip()
                self.parts.append(f"> **Note:** {note_text}")
                # Process any remaining children
                for child in node.children[1:]:
                    child.accept(self)
        elif node.block_type == "callout":
            # Format callouts as markdown callouts
            if node.children and isinstance(node.children[0], TextNode):
                note_text = node.children[0].text.strip()
                self.parts.append(f"> **Note:** {note_text}")
                # Process any remaining children
                for child in node.children[1:]:
                    child.accept(self)
        # Add handling for other block types like 'table' if needed
        # elif node.block_type == "table":
        #     self._visit_table_block(node)
        else:
            # Default handling for unknown or generic blocks
            # Render children directly without special block formatting
            # Optionally add a comment or marker?
            # self.parts.append(f"<!-- Nomenic Block: {node.block_type} -->")
            for child in node.children:
                child.accept(self)
                # Add spacing after most block elements within the generic block
                if not isinstance(child, TextNode):
                    self.parts.append("")

    def _visit_code_block(self, node: BlockNode):
        """Handle code blocks specifically."""
        if node.children and isinstance(node.children[0], TextNode):
            content = node.children[0].text.strip() # Use strip() here, consider raw content if needed
        else:
            content = ""
        
        language = node.attributes.get("language", "") if hasattr(node, "attributes") else ""
        self.parts.append(f"```{language}\n{content}\n```")

    def _process_inline_formatting(self, text: str) -> str:
        """Render inline formatting (@b, @i, @c, @l) to Markdown."""
        # TODO: Improve regex to handle nesting and escaped chars if needed
        text = re.sub(r'@b\((.*?)\)', r'**\1**', text)  # Bold
        text = re.sub(r'@i\((.*?)\)', r'*\1*', text)    # Italic
        text = re.sub(r'@c\((.*?)\)', r'`\1`', text)    # Code
        # Simple link handling, assuming value is URL or needs lookup
        text = re.sub(r'@l\((.*?)\)', r'[\1](#)', text) # Link - assumes value is URL
        return text

def render_markdown(content: str, include_frontmatter: bool = True) -> str:
    """
    Render a Nomenic document as Markdown using the Visitor pattern.

    Args:
        content: The Nomenic document content
        include_frontmatter: Whether to include metadata as YAML frontmatter

    Returns:
        Markdown representation of the document
    """
    # 1. Parse the document
    lexer = Lexer(content)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    document = parser.parse()
    
    # 2. Create Visitor
    visitor = MarkdownVisitor(include_frontmatter=include_frontmatter)

    # 3. Render using Visitor
    return visitor.render(document)

# --- Remove old implementation ---
# def _render_node(node: ASTNode, depth: int = 0) -> str: ...
# def _render_header(node: HeaderNode, depth: int) -> str: ...
# def _render_text(node: TextNode) -> str: ...
# def _render_list(node: ListNode) -> str: ...
# def _render_code(node: BlockNode) -> str: ...
# --- End of old implementation --- 