# Nomenic Core - Parser

# This file contains the parser implementation.
# It takes a stream of tokens from the lexer and builds an Abstract Syntax Tree (AST).
# The parser handles both block-level elements (header, text, list, etc.) and
# their content, including multi-line text blocks.

from typing import Optional

# Add other necessary AST node types
from .ast import BlockNode, DocumentNode, HeaderNode, ListNode, TextNode
from .errors import ParserError
from .tokens import Token, TokenType


class Parser:
    """
    Parses a stream of Nomenic Core tokens into an Abstract Syntax Tree (AST).

    The parser processes tokens sequentially, building a document tree with
    various node types. It handles:

    - Block elements (header, text, list, code, table, etc.)
    - Nested content with proper hierarchy
    - Multi-line text blocks (>>> ... <<<)
    - Custom directives and extensions
    """

    def __init__(self, tokens: list[Token]):
        """
        Initialize the parser with a list of tokens.

        Args:
            tokens: List of Token objects from the lexer
        """
        self.tokens = tokens
        self.position = 0
        # List of (message, token) tuples
        self.errors: list[tuple[str, Token]] = []
        self.strict_mode = False  # If True, errors will raise exceptions

    def _error(self, message: str, token: Optional[Token] = None) -> None:
        """
        Record an error with the given message and token.

        Args:
            message: Error message
            token: The token where the error occurred (or current token if None)
        """
        if token is None:
            token = self._peek() or self._previous()
        self.errors.append((message, token))
        if self.strict_mode:
            raise ParserError(f"{message} at line {token.line}, column {token.column}")

    def _report_error(self, message: str, token: Optional[Token] = None) -> None:
        """
        Record an error and raise a ParserError exception.

        Args:
            message: Error message
            token: The token where the error occurred

        Raises:
            ParserError: Always raised with the formatted error message
        """
        if token is None:
            token = self._peek() or self._previous()

        error_msg = f"{message} at line {token.line}, column {token.column}"
        self.errors.append((message, token))
        raise ParserError(error_msg)

    def _synchronize(self) -> None:
        """
        Recover from a parsing error by advancing until a statement boundary.
        This helps the parser continue after encountering an error.
        """
        self._advance()  # Skip the problematic token

        while not self._is_at_end():
            # Skip tokens until we find a potential statement boundary
            if self._previous().type == TokenType.NEWLINE:
                return

            current = self._peek()
            if current is None:
                return

            # Block tokens typically start new statements
            if current.type in (
                TokenType.HEADER,
                TokenType.LIST,
                TokenType.CODE,
                TokenType.TABLE,
                TokenType.BLOCKQUOTE,
                TokenType.FIGURE,
                TokenType.CUSTOM_DIRECTIVE,
            ):
                return

            self._advance()

    def parse(self) -> DocumentNode:
        """
        Parse the token stream into a DocumentNode.

        This is the main parsing method that processes the entire token stream
        and constructs a complete AST. It handles:
        - Headers and sections
        - Text blocks (single-line and multi-line)
        - Lists (ordered and unordered)
        - Code blocks
        - Tables
        - Callouts
        - Custom directives
        - And other Nomenic Core syntax elements

        Returns:
            DocumentNode containing the full parsed AST

        Raises:
            ParserError: If strict error checking is enabled and a parsing error occurs
        """
        document = DocumentNode()
        self.errors = []  # Reset errors before parsing

        while self.position < len(self.tokens):
            token = self._peek()
            if token is None:
                break

            if token.type == TokenType.HEADER:
                self._advance()  # Skip the 'header:' token
                value_token = self._peek()
                # Check if there's content after the header and it's not empty
                # or a comment
                if (
                    value_token
                    and value_token.type == TokenType.TEXT
                    and value_token.value
                    and value_token.value.strip()
                    and not value_token.value.strip().startswith("#")
                ):
                    node = HeaderNode(level=1, text=value_token.value or "")
                    document.children.append(node)
                    self._advance()
                else:
                    # Record the error and skip this token
                    self._error(
                        "Expected text content after header, found empty or comment",
                        token,
                    )
                    # Check if we're at a comment
                    if (
                        value_token
                        and value_token.value
                        and value_token.value.strip().startswith("#")
                    ):
                        self._advance()  # Skip the comment
                    self._synchronize()
            elif token.type == TokenType.LIST:
                self._advance()  # Skip the 'list:' token
                node = self._parse_list()
                if node:
                    document.children.append(node)
                else:
                    self._error("Expected list items after list:", token)
                    self._synchronize()
            elif token.type == TokenType.CODE:
                self._advance()  # Skip the 'code:' token
                node = self._parse_code_block()
                if node:
                    document.children.append(node)
                else:
                    self._error("Expected code content after code:", token)
                    self._synchronize()
            elif token.type == TokenType.TABLE:
                self._advance()  # Skip the 'table:' token
                node = self._parse_table_block()
                if node:
                    document.children.append(node)
                else:
                    self._error("Expected table content after table:", token)
                    self._synchronize()
            elif token.type == TokenType.DEF_LIST:
                self._advance()  # Skip the 'def-list:' token
                node = self._parse_def_list_block()
                if node:
                    document.children.append(node)
                else:
                    self._error(
                        "Expected definition terms/descriptions after def-list:", token
                    )
                    self._synchronize()
            elif token.type == TokenType.CALLOUT:
                self._advance()  # Skip the 'note:' or 'warn:' token
                value_token = self._peek()
                if value_token and value_token.type == TokenType.TEXT:
                    node = BlockNode(
                        block_type="callout",
                        children=[TextNode(text=value_token.value or "")],
                    )
                    document.children.append(node)
                    self._advance()
                else:
                    self._error("Expected callout content after note:/warn:", token)
                    self._synchronize()
            elif token.type == TokenType.BLOCKQUOTE:
                self._advance()  # Skip the 'blockquote:' token
                node = self._parse_blockquote_block()
                if node:
                    document.children.append(node)
                else:
                    self._error("Expected quoted lines after blockquote:", token)
                    self._synchronize()
            elif token.type == TokenType.FIGURE:
                self._advance()  # Skip the 'figure:' token
                node = self._parse_figure_block()
                if node:
                    document.children.append(node)
                else:
                    self._error(
                        "Expected figure content (src:, caption:) after figure:", token
                    )
                    self._synchronize()
            elif token.type == TokenType.CUSTOM_DIRECTIVE:
                directive_name = token.value.rstrip(":") if token.value else "custom"
                self._advance()  # Skip the 'x-foo:' token
                node = self._parse_custom_directive_block(directive_name)
                if node:
                    document.children.append(node)
                else:
                    self._error(
                        f"Expected content after custom directive {directive_name}:",
                        token,
                    )
                    self._synchronize()
            elif token.type == TokenType.TEXT:
                # Handle text: tokens specifically - there are two cases:
                # 1. Multi-line text block with >>> and <<<
                # 2. Single-line text token (like in header_and_text test)
                if token.value and token.value.strip() == "text:":
                    # First check if this is the start of a multi-line text block
                    saved_position = self.position
                    node = self._parse_multiline_text_block()

                    if node:
                        # Successfully parsed a multi-line text block
                        document.children.append(node)
                        continue  # Skip to next iteration

                    # If multiline parsing failed, restore position and handle as
                    # regular text: token
                    self.position = saved_position
                    self._advance()  # Skip the 'text:' token

                    # Get the text content that follows
                    if self._peek() and self._peek().type == TokenType.TEXT:
                        text_token = self._peek()
                        document.children.append(TextNode(text=text_token.value or ""))
                        self._advance()
                    else:
                        self._error("Expected text content after text:", token)
                        self._synchronize()
                # Handle unexpected >>> without text: prefix
                elif token.value and token.value.strip() == ">>>":
                    self._error(
                        "Unexpected block start marker ('>>>') without preceding "
                        "'text:'",
                        token,
                    )
                    self._advance()  # Skip the marker

                    # Skip content until block end or EOF
                    terminator_found = False
                    while not self._is_at_end():
                        next_token = self._peek()
                        if next_token and next_token.type == TokenType.TEXT_BLOCK_END:
                            self._advance()  # Skip the closing marker
                            terminator_found = True
                            break
                        self._advance()

                    if not terminator_found:
                        self._error("Unterminated block (missing '<<<')", token)
                # Don't process block keyword tokens like 'header:' as nodes themselves
                elif not (token.value and token.value.strip().endswith(":")):
                    node = TextNode(text=token.value or "")
                    document.children.append(node)
                    self._advance()  # Move past the text token
                else:
                    # Skip over block keyword tokens without creating nodes
                    self._advance()
            elif token.type == TokenType.NEWLINE:
                self._advance()  # Skip top-level newlines
            else:
                # Skip other unknown/unhandled tokens at the top level for now
                self._advance()

        return document

    def _parse_header(self):
        token = self._advance()
        # For now, assume level 1 and use token.value as text
        return HeaderNode(level=1, text=token.value or "")

    def _parse_text(self):
        token = self._advance()
        return TextNode(text=token.value or "")

    def _parse_list(self):
        """
        Parse a list block, which can be ordered or unordered.

        Handles both bulleted lists (started with -) and ordered lists
        (numbered or lettered). Collects list items into a ListNode.

        Returns:
            ListNode containing all items or None if no valid list items found
        """
        items = []
        ordered = False
        list_token = self._previous()  # Get the starting list token for error reporting

        while not self._is_at_end():
            token = self._peek()
            if token is None:
                break

            if token.type == TokenType.LIST_ITEM:
                self._advance()
                value_token = self._peek()
                if (
                    value_token
                    and value_token.type == TokenType.TEXT
                    and value_token.value
                    and value_token.value.strip()
                    and not value_token.value.strip().startswith("#")
                ):
                    items.append(TextNode(text=value_token.value or ""))
                    self._advance()
                else:
                    if (
                        value_token
                        and value_token.value
                        and value_token.value.strip().startswith("#")
                    ):
                        self._error("Missing list item content (found comment)", token)
                        self._advance()  # Skip the comment
                    else:
                        self._error(
                            "Expected text content after list item marker", token
                        )
                    items.append(TextNode(text=""))
            elif token.type == TokenType.ORDERED_LIST_ITEM:
                ordered = True
                self._advance()
                value_token = self._peek()
                if (
                    value_token
                    and value_token.type == TokenType.TEXT
                    and value_token.value
                    and value_token.value.strip()
                    and not value_token.value.strip().startswith("#")
                ):
                    items.append(TextNode(text=value_token.value or ""))
                    self._advance()
                else:
                    if (
                        value_token
                        and value_token.value
                        and value_token.value.strip().startswith("#")
                    ):
                        self._error(
                            "Missing ordered list item content (found comment)", token
                        )
                        self._advance()  # Skip the comment
                    else:
                        self._error(
                            "Expected text content after ordered list item marker",
                            token,
                        )
                    items.append(TextNode(text=""))
            elif token.type == TokenType.NEWLINE:
                self._advance()
            else:
                break  # End of list block

        if not items:
            self._error("Empty list block", list_token)

        if items:
            return ListNode(ordered=ordered, items=items)
        return None

    def _parse_code_block(self):
        """
        Parse a code block, preserving indentation and newlines.

        Code blocks are introduced by 'code:' and followed by indented lines.
        All content is collected into a single BlockNode with type 'code'.

        Returns:
            BlockNode containing the code content or None if empty
        """
        code_lines = []
        code_token = self._previous()  # Get the starting code token for error reporting

        while not self._is_at_end():
            token = self._peek()
            if token is None:
                break

            if token.type == TokenType.INDENTATION:
                self._advance()  # Skip indentation token
                text_token = self._peek()
                if text_token and text_token.type == TokenType.TEXT:
                    code_lines.append(text_token.value or "")
                    self._advance()
                else:
                    self._error("Expected code content after indentation", token)
                    break
            elif token.type == TokenType.TEXT and token.value and token.value.strip():
                # Handle code on the same line as code: (rare)
                code_lines.append(token.value)
                self._advance()
            elif token.type == TokenType.NEWLINE:
                self._advance()
            else:
                break

        if not code_lines:
            self._error("Empty code block", code_token)

        if code_lines:
            code_text = "\n".join(code_lines)
            return BlockNode(block_type="code", children=[TextNode(text=code_text)])
        return None

    def _parse_table_block(self):
        """
        Parse a table, handling rows as list items prefixed with 'row:'.

        Tables are structured as collections of rows, each with comma-separated
        values. These are parsed into a BlockNode with type 'table'.

        Returns:
            BlockNode containing table rows or None if empty
        """
        rows = []
        while not self._is_at_end():
            token = self._peek()
            if token is None:
                break
            if token.type == TokenType.LIST_ITEM:
                self._advance()  # Skip '- '
                value_token = self._peek()
                if value_token and value_token.type == TokenType.TEXT:
                    # Remove 'row: ' prefix if present
                    text = value_token.value or ""
                    if text.startswith("row: "):
                        text = text[len("row: ") :]
                    rows.append(TextNode(text=text))
                    self._advance()
                else:
                    rows.append(TextNode(text=""))
            elif token.type == TokenType.NEWLINE:
                self._advance()
            else:
                break  # End of table block
        if rows:
            return BlockNode(block_type="table", children=rows)
        return None

    def _parse_blockquote_block(self):
        lines = []
        while not self._is_at_end():
            token = self._peek()
            if token is None:
                break
            if (
                token.type == TokenType.TEXT
                and token.value
                and token.value.strip().startswith(">")
            ):
                # Remove '> ' prefix
                text = token.value.lstrip("> ").strip()
                lines.append(TextNode(text=text))
                self._advance()
            elif token.type == TokenType.NEWLINE:
                self._advance()
            else:
                break
        if lines:
            return BlockNode(block_type="blockquote", children=lines)
        return None

    def _parse_figure_block(self):
        children = []
        # Track metadata (unused now but may be useful later)
        while not self._is_at_end():
            token = self._peek()
            if token is None:
                break
            if token.type == TokenType.SRC:
                self._advance()
                value_token = self._peek()
                if value_token and value_token.type == TokenType.TEXT:
                    children.append(TextNode(text=value_token.value or ""))
                    self._advance()
            elif token.type == TokenType.CAPTION:
                self._advance()
                value_token = self._peek()
                if value_token and value_token.type == TokenType.TEXT:
                    children.append(TextNode(text=value_token.value or ""))
                    self._advance()
            elif token.type == TokenType.NEWLINE:
                self._advance()
            else:
                break
        if children:
            return BlockNode(block_type="figure", children=children)
        return None

    def _parse_custom_directive_block(self, directive_name):
        children = []
        while not self._is_at_end():
            token = self._peek()
            if token is None:
                break
            if token.type == TokenType.TEXT:
                children.append(TextNode(text=token.value or ""))
                self._advance()
            elif token.type == TokenType.NEWLINE:
                self._advance()
            else:
                break
        if children:
            return BlockNode(block_type=directive_name, children=children)
        return None

    def _parse_def_list_block(self):
        children = []
        while not self._is_at_end():
            token = self._peek()
            if token is None:
                break
            if token.type in (TokenType.DEF_TERM, TokenType.DEF_DESC):
                self._advance()  # Skip 'dt:' or 'dd:'
                value_token = self._peek()
                if value_token and value_token.type == TokenType.TEXT:
                    children.append(TextNode(text=value_token.value or ""))
                    self._advance()
                else:
                    children.append(TextNode(text=""))
            elif token.type == TokenType.NEWLINE:
                self._advance()
            else:
                break
        if children:
            return BlockNode(block_type="def-list", children=children)
        return None

    def _parse_multiline_text_block(self) -> Optional[TextNode]:
        """
        Parse a multi-line text block (text: followed by >>>, content, <<<).

        This method handles the pattern:
            text:
            >>>
            Line 1
            Line 2
            ...
            <<<

        It properly processes NEWLINE tokens between parts of the block and
        constructs a single TextNode with all content joined with newlines.

        Returns:
            TextNode with combined content or None if parsing fails
        """
        # Verify we are at 'text:'
        if not (
            self._peek()
            and self._peek().type == TokenType.TEXT
            and self._peek().value
            and self._peek().value.strip() == "text:"
        ):
            return None

        text_token = self._peek()  # Save for potential error reporting
        self._advance()  # Consume the 'text:' token

        # Skip any NEWLINE tokens until we find TEXT_BLOCK_START
        while self._peek() and self._peek().type == TokenType.NEWLINE:
            self._advance()

        # Verify we're now at '>>>'
        if not (self._peek() and self._peek().type == TokenType.TEXT_BLOCK_START):
            self._error(
                "Expected '>>>' to start multi-line text block after 'text:'",
                text_token,
            )
            return None  # Not a valid multi-line text block

        start_token = self._peek()  # Save for potential error reporting
        self._advance()  # Consume the '>>>' token

        # Skip any NEWLINE tokens after the TEXT_BLOCK_START
        while self._peek() and self._peek().type == TokenType.NEWLINE:
            self._advance()

        # Collect all text, building paragraphs separated by newlines
        paragraphs = []
        current_paragraph = []
        terminator_found = False

        while not self._is_at_end():
            token = self._peek()

            if token is None:
                break

            if token.type == TokenType.TEXT_BLOCK_END:
                self._advance()  # Consume '<<<'
                terminator_found = True
                break  # Exit multi-line block processing

            if token.type == TokenType.TEXT:
                # Add this text to the current paragraph
                current_paragraph.append(token.value or "")
                self._advance()
            elif token.type == TokenType.NEWLINE:
                # Found a newline, finish the current paragraph and start a new one
                if current_paragraph:
                    paragraphs.append("".join(current_paragraph))
                    current_paragraph = []
                self._advance()
            else:
                # Skip any other token types
                self._advance()

        # Check if we found the closing marker
        if not terminator_found:
            self._error("Unterminated multi-line text block (missing <<<)", start_token)

        # Add the final paragraph if there is one
        if current_paragraph:
            paragraphs.append("".join(current_paragraph))

        # Join all paragraphs with newlines into the final text
        if paragraphs:
            return TextNode(text="\n".join(paragraphs))

        # Empty block, but valid syntax
        return TextNode(text="")

    def _peek(self) -> Optional[Token]:
        """Return the next token without consuming it."""
        if self._is_at_end():
            return None
        return self.tokens[self.position]

    def _advance(self) -> Token:
        """Consume and return the next token."""
        if not self._is_at_end():
            self.position += 1
        return self._previous()

    def _previous(self) -> Token:
        """Return the most recently consumed token."""
        return self.tokens[self.position - 1]

    def _is_at_end(self) -> bool:
        """Check if we have reached the end of the token stream."""
        if self.position >= len(self.tokens):
            return True
        current_token = self.tokens[self.position]
        return current_token.type == TokenType.EOF

    def _match(self, *token_types: TokenType) -> bool:
        """Check if the current token matches any of the given types."""
        if self._is_at_end():
            return False
        current_token_type = self._peek().type
        if current_token_type in token_types:
            self._advance()  # Consume if matched
            return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        """Check if the current token is of the given type without consuming."""
        if self._is_at_end():
            return False
        peeked_token = self._peek()
        return peeked_token is not None and peeked_token.type == token_type

    def _peek_ahead(self, n):
        pos = self.position + n
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    # Placeholder for block parsing logic
    # def _parse_block(self):
    #     # ... logic to determine and parse the next block (header, section,
    #     # list, etc.)
    #     pass


def parse(tokens: list[Token]) -> DocumentNode:
    """Convenience function to parse Nomenic tokens."""
    parser = Parser(tokens)
    return parser.parse()
