# Nomenic Core - Token Definitions

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional


class TokenType(Enum):
    """Enum representing the different types of tokens in Nomenic Core."""

    # Block level tokens
    META = auto()
    HEADER = auto()
    SECTION = auto()
    TEXT = auto()
    LIST = auto()
    CODE = auto()
    TABLE = auto()
    DEF_LIST = auto()
    DEF_TERM = auto()
    DEF_DESC = auto()
    BLOCKQUOTE = auto()
    FIGURE = auto()
    SRC = auto()
    CAPTION = auto()

    # Inline elements & modifiers
    LIST_ITEM = auto()
    TEXT_BLOCK_START = auto()
    TEXT_BLOCK_END = auto()
    PAREN_ANNOTATION = auto()
    BRACKET_ANNOTATION = auto()
    INLINE_KEY_VALUE = auto()
    CALLOUT = auto()
    CUSTOM_DIRECTIVE = auto()
    ORDERED_LIST_ITEM = auto()
    COMMENT = auto()
    ESCAPE = auto()
    STYLE_BOLD = auto()
    STYLE_ITALIC = auto()
    STYLE_CODE = auto()
    STYLE_LINK = auto()

    # Structural tokens
    INDENTATION = auto()
    NEWLINE = auto()
    WHITESPACE = auto()
    EOF = auto()


@dataclass
class Token:
    """
    Represents a token in Nomenic Core syntax.

    Attributes:
        type: The type of token
        value: The string value of the token (or None for EOF)
        line: Line number in source (1-indexed)
        column: Column number in source (1-indexed)
        indent_level: Indentation level (0 for root level)
        metadata: Optional additional data for the token
    """

    type: TokenType
    value: Optional[Any]  # Can be string, list, dict, or None
    line: int
    column: int
    indent_level: int = 0
    metadata: Optional[dict[str, Any]] = None

    def __str__(self) -> str:
        # Use repr for value to handle strings vs other types correctly
        # Use {self.type.name} to get the enum member name
        return (
            f"Token(type=TokenType.{self.type.name}, value={self.value!r}, "
            f"line={self.line}, column={self.column}, "
            f"indent_level={self.indent_level}, metadata={self.metadata!r})"
        )


# Maps token strings to their types for easy lookup
TOKEN_MAP = {
    "meta:": TokenType.META,
    "m:": TokenType.META,
    "header:": TokenType.HEADER,
    "h:": TokenType.HEADER,
    "section:": TokenType.SECTION,
    "s:": TokenType.SECTION,
    "text:": TokenType.TEXT,
    "t:": TokenType.TEXT,
    "list:": TokenType.LIST,
    "l:": TokenType.LIST,
    "code:": TokenType.CODE,
    "c:": TokenType.CODE,
    "table:": TokenType.TABLE,
    "tbl:": TokenType.TABLE,
    "def-list:": TokenType.DEF_LIST,
    "dl:": TokenType.DEF_LIST,
    "def-term:": TokenType.DEF_TERM,
    "dt:": TokenType.DEF_TERM,
    "def-desc:": TokenType.DEF_DESC,
    "dd:": TokenType.DEF_DESC,
    "blockquote:": TokenType.BLOCKQUOTE,
    "bq:": TokenType.BLOCKQUOTE,
    "figure:": TokenType.FIGURE,
    "fig:": TokenType.FIGURE,
    "src:": TokenType.SRC,
    "caption:": TokenType.CAPTION,
    ">>>": TokenType.TEXT_BLOCK_START,
    "<<<": TokenType.TEXT_BLOCK_END,
    "note:": TokenType.CALLOUT,
    "warn:": TokenType.CALLOUT,
    "tip:": TokenType.CALLOUT,
    "#": TokenType.COMMENT,
    "\\\\": TokenType.ESCAPE,
}

# Patterns that need to be matched rather than exact strings
# These will be implemented in the lexer with regex
