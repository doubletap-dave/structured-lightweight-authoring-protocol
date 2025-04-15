# Nomenic Core - Abstract Syntax Tree (AST)

# This file will define the nodes for the AST produced by the parser.
# (e.g., DocumentNode, HeaderNode, ListNode, TextNode, etc.)

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ASTNode:
    """
    Base class for all AST nodes in Nomenic Core.
    """

    children: list["ASTNode"] = field(default_factory=list)
    value: Optional[Any] = None


@dataclass
class DocumentNode(ASTNode):
    """
    Root node representing the entire document.
    """

    pass


@dataclass
class HeaderNode(ASTNode):
    """
    Node representing a section header.
    """

    level: int = 1
    text: str = ""


@dataclass
class TextNode(ASTNode):
    """
    Node representing a paragraph or text block.
    """

    text: str = ""


@dataclass
class ListNode(ASTNode):
    """
    Node representing a list block (unordered or ordered).
    """

    ordered: bool = False
    items: list["ASTNode"] = field(default_factory=list)


@dataclass
class BlockNode(ASTNode):
    """
    Generic node for other block types (code, table, etc.).
    """

    block_type: str = ""
    meta: Optional[dict] = None
