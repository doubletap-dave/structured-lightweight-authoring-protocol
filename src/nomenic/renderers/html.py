"""HTML renderer for Nomenic documents."""

import html
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


class HTMLRendererVisitor(Visitor):
    """Visitor that renders AST nodes as HTML."""

    def __init__(self, 
                 theme: Optional[str] = None,
                 include_styles: bool = True,
                 include_meta: bool = True):
        """
        Initialize the HTML renderer visitor.

        Args:
            theme: Optional theme name (default, dark, light)
            include_styles: Whether to include default styles
            include_meta: Whether to include metadata as HTML meta tags
        """
        self.theme = theme
        self.include_styles = include_styles
        self.include_meta = include_meta
        self.depth = 0
        
    def visit_document(self, node: DocumentNode) -> str:
        """Render a document node as HTML."""
        html_parts = []

        # Start with HTML doctype and head
        if self.include_styles:
            style_content = _get_theme_styles(self.theme)
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
        if self.include_meta:
            meta_block = next(
                (n for n in node.children if isinstance(n, BlockNode) and n.block_type == "meta"),
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
        for child in node.children:
            # Skip meta block, already processed
            if isinstance(child, BlockNode) and child.block_type == "meta":
                continue
                
            html_parts.append(child.accept(self))

        # Close body and html
        html_parts.append("</body>\n</html>")

        return "".join(html_parts)
        
    def visit_header(self, node: HeaderNode) -> str:
        """Render a header node as HTML."""
        # Convert content to HTML, handling basic formatting
        content = _process_inline_formatting(node.text)

        # Create id from header for linking
        header_id = node.text.lower().replace(" ", "-")

        return f"<h{min(self.depth + 1, 6)} id=\"{header_id}\" class=\"nomenic-header\">{content}</h{min(self.depth + 1, 6)}>\n"
        
    def visit_text(self, node: TextNode) -> str:
        """Render a text node as HTML."""
        # Convert content to HTML, handling basic formatting
        content = _process_inline_formatting(node.text)

        return f"<p class=\"nomenic-text\">{content}</p>\n"
        
    def visit_list(self, node: ListNode) -> str:
        """Render a list node as HTML."""
        result = "<ul class=\"nomenic-list\">\n"

        self.depth += 1
        for item in node.items:
            # Process inline formatting
            if isinstance(item, TextNode):
                item_content = _process_inline_formatting(item.text)
            else:
                item_content = item.accept(self)
            result += f"<li>{item_content}</li>\n"
        self.depth -= 1

        result += "</ul>\n"
        return result
        
    def visit_block(self, node: BlockNode) -> str:
        """Render a block node as HTML."""
        if node.block_type == "code":
            return self._render_code_block(node)
        elif node.block_type == "table":
            return self._render_table_block(node)
        else:
            # Generic block node, render children
            self.depth += 1
            result = f"<div class=\"nomenic-block nomenic-{node.block_type}\">\n"
            for child in node.children:
                result += child.accept(self)
            result += "</div>\n"
            self.depth -= 1
            return result
            
    def _render_code_block(self, node: BlockNode) -> str:
        """Render a code block as HTML."""
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
        
    def _render_table_block(self, node: BlockNode) -> str:
        """Render a table block as HTML."""
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

    # Create visitor and generate HTML
    visitor = HTMLRendererVisitor(theme, include_styles, include_meta)
    return document.accept(visitor)

# Keep helper functions as standalone for now
def _process_inline_formatting(text: str) -> str:
    """
    Process inline formatting in text.

    Handles:
    - @b(...) -> <strong>...</strong> (bold)
    - @i(...) -> <em>...</em> (italic)
    - @c(...) -> <code>...</code> (code/monospace)
    - @l(...) -> <a href="...">...</a> (link)

    Args:
        text: Text to process

    Returns:
        Text with formatting applied
    """
    # Escape HTML first
    processed = html.escape(text)

    # Bold: @b(text) -> <strong>text</strong>
    processed = re.sub(r'@b\((.*?)\)', r'<strong>\1</strong>', processed)

    # Italic: @i(text) -> <em>text</em>
    processed = re.sub(r'@i\((.*?)\)', r'<em>\1</em>', processed)

    # Code: @c(text) -> <code>text</code>
    processed = re.sub(r'@c\((.*?)\)', r'<code>\1</code>', processed)

    # Link: @l(url|text) -> <a href="url">text</a>
    # If no pipe, use the URL as text
    def link_replace(match):
        parts = match.group(1).split('|', 1)
        if len(parts) == 2:
            url, text = parts
        else:
            url = text = parts[0]
        return f'<a href="{url}">{text}</a>'

    processed = re.sub(r'@l\((.*?)\)', link_replace, processed)

    return processed


def _get_theme_styles(theme: Optional[str] = None) -> str:
    """
    Get CSS styles for the specified theme.

    Args:
        theme: Theme name (default, dark, light)

    Returns:
        CSS styles as a string
    """
    # Default theme
    if not theme or theme == "default":
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .nomenic-header {
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: #222;
        }
        .nomenic-text {
            margin-bottom: 1em;
        }
        .nomenic-code {
            background: #f5f5f5;
            border-radius: 3px;
            padding: 0.75em;
            font-family: monospace;
            overflow-x: auto;
        }
        .nomenic-list {
            margin-bottom: 1em;
        }
        .nomenic-table {
            border-collapse: collapse;
            margin-bottom: 1em;
            width: 100%;
        }
        .nomenic-table th, .nomenic-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .nomenic-table th {
            background-color: #f2f2f2;
        }
        """

    # Dark theme
    elif theme == "dark":
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #eee;
            background-color: #222;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .nomenic-header {
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: #fff;
        }
        .nomenic-text {
            margin-bottom: 1em;
        }
        .nomenic-code {
            background: #333;
            border-radius: 3px;
            padding: 0.75em;
            font-family: monospace;
            color: #ddd;
            overflow-x: auto;
        }
        .nomenic-list {
            margin-bottom: 1em;
        }
        .nomenic-table {
            border-collapse: collapse;
            margin-bottom: 1em;
            width: 100%;
        }
        .nomenic-table th, .nomenic-table td {
            border: 1px solid #444;
            padding: 8px;
            text-align: left;
        }
        .nomenic-table th {
            background-color: #333;
        }
        a {
            color: #6bf;
        }
        """

    # Light theme
    elif theme == "light":
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #222;
            background-color: #fff;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .nomenic-header {
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: #000;
        }
        .nomenic-text {
            margin-bottom: 1em;
        }
        .nomenic-code {
            background: #f8f8f8;
            border-radius: 3px;
            padding: 0.75em;
            font-family: monospace;
            border: 1px solid #eee;
            overflow-x: auto;
        }
        .nomenic-list {
            margin-bottom: 1em;
        }
        .nomenic-table {
            border-collapse: collapse;
            margin-bottom: 1em;
            width: 100%;
        }
        .nomenic-table th, .nomenic-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .nomenic-table th {
            background-color: #f5f5f5;
        }
        a {
            color: #07c;
        }
        """
    
    # Unknown theme, use default
    else:
        return _get_theme_styles("default")
