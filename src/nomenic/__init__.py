"""Nomenic Document Language Parser and Toolkit.

This package provides tools for working with Nomenic Document Language (NDL) files.
"""

from .lexer import Lexer, tokenize
from .parser import Parser
from .tokens import TokenType
from .ast import (
    ASTNode, DocumentNode, HeaderNode,
    TextNode, ListNode, BlockNode,
)

# For CLI access
try:
    from .cli import main as cli_main
except ImportError:
    # CLI functionality might not be available in all environments
    pass

# Import converters for format conversion
try:
    from .converters import (
        FormatConverter,
        MarkdownConverter,
        JSONConverter,
        YAMLConverter,
    )
except ImportError:
    # Converters might not be fully initialized during installation
    pass

__version__ = "0.1.0"

__all__ = [
    "Lexer", "tokenize", "Parser",
    "TokenType",
    "ASTNode", "DocumentNode", "HeaderNode",
    "TextNode", "ListNode", "BlockNode",
    "FormatConverter", "MarkdownConverter", "JSONConverter", "YAMLConverter",
]
