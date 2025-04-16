"""HTML renderer for Nomenic documents."""

import html
import re
from typing import Any, Dict, List, Optional, Union

from .. import Lexer, Parser
from ..ast import (
    ASTNode,
    BlockNode,
    DocumentNode,
    HeaderNode,
    ListNode,
    TextNode,
)


def render_html(
    content: str,
    theme: Optional[str] = None,
    include_styles: bool = True,
    include_meta: bool = True,
) -> str:
    """
    Render a Nomenic document as HTML.

    Args:
        content: The Nomenic document content
        theme: Optional theme name (default, dark, light)
        include_styles: Whether to include default styles
        include_meta: Whether to include metadata as HTML meta tags

    Returns:
        HTML representation of the document
    """
    # Parse the document
    lexer = Lexer(content)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    document = parser.parse()

    # Generate HTML
    html_parts = []

    # Start with HTML doctype and head
    if include_styles:
        style_content = _get_theme_styles(theme)
        html_parts.append(
            f"<!DOCTYPE html>\n"
            f"<html>\n"
            f"<head>\n"
            f"<meta charset=\"UTF-8\">\n"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            f"<style>\n{style_content}\n</style>\n"
        )
    else:
        html_parts.append(
            f"<!DOCTYPE html>\n"
            f"<html>\n"
            f"<head>\n"
            f"<meta charset=\"UTF-8\">\n"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        )

    # Add metadata if present and requested
    if include_meta:
        meta_block = next(
            (node for node in document.children if isinstance(
                node, BlockNode) and node.block_type == "meta"),
            None
        )
        if meta_block and hasattr(meta_block, 'meta') and meta_block.meta:
            for key, value in meta_block.meta.items():
                # Skip internal metadata
                if key.startswith("_"):
                    continue

                html_parts.append(
                    f'<meta name="nomenic:{key}" content="{html.escape(str(value))}">\n')

            # Use title from metadata if available
            title = meta_block.meta.get("title", "Nomenic Document")
            html_parts.append(f"<title>{html.escape(str(title))}</title>\n")
        else:
            html_parts.append("<title>Nomenic Document</title>\n")
    else:
        html_parts.append("<title>Nomenic Document</title>\n")

    # Close head and start body
    html_parts.append("</head>\n<body>\n")

    # Process document nodes
    for node in document.children:
        # Skip meta block, already processed
        if isinstance(node, BlockNode) and node.block_type == "meta":
            continue

        html_parts.append(_render_node(node, 0))

    # Close body and html
    html_parts.append("</body>\n</html>")

    return "".join(html_parts)


def _render_node(node: ASTNode, depth: int = 0) -> str:
    """
    Render a node as HTML.

    Args:
        node: The node to render
        depth: Current nesting depth

    Returns:
        HTML representation of the node
    """
    if isinstance(node, HeaderNode):
        return _render_header(node, depth)
    elif isinstance(node, TextNode):
        return _render_text(node, depth)
    elif isinstance(node, ListNode):
        return _render_list(node, depth)
    elif isinstance(node, BlockNode) and node.block_type == "code":
        return _render_code(node, depth)
    elif isinstance(node, BlockNode) and node.block_type == "table":
        return _render_table(node, depth)
    elif isinstance(node, BlockNode):
        # Generic block node, render children
        result = f"<div class=\"nomenic-block nomenic-{node.block_type}\">\n"
        for child in node.children:
            result += _render_node(child, depth + 1)
        result += "</div>\n"
        return result

    # Unknown node type, render as plain text
    return f"<div>{html.escape(str(node))}</div>\n"


def _render_header(node: HeaderNode, depth: int) -> str:
    """Render a header node as HTML."""
    # Convert content to HTML, handling basic formatting
    content = _process_inline_formatting(node.text)

    # Create id from header for linking
    header_id = node.text.lower().replace(" ", "-")

    return f"<h{min(depth + 1, 6)} id=\"{header_id}\" class=\"nomenic-header\">{content}</h{min(depth + 1, 6)}>\n"


def _render_text(node: TextNode, depth: int) -> str:
    """Render a text node as HTML."""
    # Convert content to HTML, handling basic formatting
    content = _process_inline_formatting(node.text)

    return f"<p class=\"nomenic-text\">{content}</p>\n"


def _render_list(node: ListNode, depth: int) -> str:
    """Render a list node as HTML."""
    result = "<ul class=\"nomenic-list\">\n"

    for item in node.items:
        # Process inline formatting
        if isinstance(item, TextNode):
            item_content = _process_inline_formatting(item.text)
        else:
            item_content = _render_node(item, depth + 1)
        result += f"<li>{item_content}</li>\n"

    result += "</ul>\n"
    return result


def _render_code(node: BlockNode, depth: int) -> str:
    """Render a code node as HTML."""
    # Get content from children
    if node.children and isinstance(node.children[0], TextNode):
        content = node.children[0].text
    else:
        content = ""

    # Escape HTML in code content
    escaped_content = html.escape(content)

    # Try to get language from meta
    language = node.meta.get("language", "") if node.meta else ""
    language_class = f" class=\"language-{language}\"" if language else ""

    return (
        f"<pre class=\"nomenic-code\"><code{language_class}>"
        f"{escaped_content}"
        f"</code></pre>\n"
    )


def _render_table(node: BlockNode, depth: int) -> str:
    """Render a table node as HTML."""
    result = "<table class=\"nomenic-table\">\n"

    # Get rows from children
    rows = []
    for child in node.children:
        if isinstance(child, TextNode):
            # Split by pipes
            cells = [cell.strip() for cell in child.text.split('|')]
            # Filter out empty cells (e.g., from leading/trailing pipes)
            cells = [cell for cell in cells if cell]
            rows.append(cells)

    # Determine if first row should be a header
    has_header = len(rows) > 0

    for i, row in enumerate(rows):
        if i == 0 and has_header:
            result += "<thead>\n<tr>\n"
            for cell in row:
                cell_content = _process_inline_formatting(cell)
                result += f"<th>{cell_content}</th>\n"
            result += "</tr>\n</thead>\n<tbody>\n"
        else:
            result += "<tr>\n"
            for cell in row:
                cell_content = _process_inline_formatting(cell)
                result += f"<td>{cell_content}</td>\n"
            result += "</tr>\n"

    if has_header:
        result += "</tbody>\n"

    result += "</table>\n"
    return result


def _process_inline_formatting(text: str) -> str:
    """
    Process inline formatting in text.

    Supports:
    - **bold** -> <strong>bold</strong>
    - *italic* -> <em>italic</em>
    - `code` -> <code>code</code>
    - [link](url) -> <a href="url">link</a>

    Args:
        text: Input text with formatting markers

    Returns:
        HTML with formatting applied
    """
    # This is a simple implementation that could be improved with better parsing
    # For now, we'll use basic replacements for demonstration

    # Replace code first (to avoid formatting within code)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    return text


def _get_theme_styles(theme: Optional[str] = None) -> str:
    """Get CSS styles for the specified theme."""
    if theme == "dark":
        return """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
    line-height: 1.6;
    color: #e0e0e0;
    background-color: #1e1e1e;
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
}
.nomenic-header {
    color: #ffffff;
    border-bottom: 1px solid #444;
    margin-top: 1.5em;
}
.nomenic-text {
    margin: 1em 0;
}
.nomenic-list {
    margin: 1em 0;
    padding-left: 2em;
}
.nomenic-code {
    background-color: #2a2a2a;
    padding: 1em;
    border-radius: 4px;
    overflow-x: auto;
}
.nomenic-table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}
.nomenic-table th, .nomenic-table td {
    border: 1px solid #444;
    padding: 0.5em;
    text-align: left;
}
.nomenic-table th {
    background-color: #333;
}
.nomenic-block {
    margin: 1em 0;
    padding: 0.5em;
    border-left: 3px solid #666;
}
a {
    color: #60a5fa;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
"""
    elif theme == "light":
        return """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #fff;
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
}
.nomenic-header {
    color: #111;
    border-bottom: 1px solid #eee;
    margin-top: 1.5em;
}
.nomenic-text {
    margin: 1em 0;
}
.nomenic-list {
    margin: 1em 0;
    padding-left: 2em;
}
.nomenic-code {
    background-color: #f5f5f5;
    padding: 1em;
    border-radius: 4px;
    overflow-x: auto;
}
.nomenic-table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}
.nomenic-table th, .nomenic-table td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}
.nomenic-table th {
    background-color: #f5f5f5;
}
.nomenic-block {
    margin: 1em 0;
    padding: 0.5em;
    border-left: 3px solid #ddd;
}
a {
    color: #0366d6;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
"""
    else:  # default theme
        return """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #fff;
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
}
.nomenic-header {
    color: #111;
    border-bottom: 1px solid #eee;
    margin-top: 1.5em;
}
.nomenic-text {
    margin: 1em 0;
}
.nomenic-list {
    margin: 1em 0;
    padding-left: 2em;
}
.nomenic-code {
    background-color: #f6f8fa;
    padding: 1em;
    border-radius: 4px;
    overflow-x: auto;
    font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
}
.nomenic-table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}
.nomenic-table th, .nomenic-table td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}
.nomenic-table th {
    background-color: #f6f8fa;
}
.nomenic-block {
    margin: 1em 0;
    padding: 0.5em;
    border-left: 3px solid #eee;
}
a {
    color: #0366d6;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
"""
