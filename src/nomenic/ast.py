# Nomenic Core - Abstract Syntax Tree (AST)

# This file will define the nodes for the AST produced by the parser.
# (e.g., DocumentNode, HeaderNode, ListNode, TextNode, etc.)

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol, TypeVar


class Visitor(Protocol):
    """Visitor protocol for AST traversal."""

    def visit_document(self, node: "DocumentNode") -> Any: ...
    def visit_header(self, node: "HeaderNode") -> Any: ...
    def visit_text(self, node: "TextNode") -> Any: ...
    def visit_list(self, node: "ListNode") -> Any: ...
    def visit_list_item(self, node: "ListItemNode") -> Any: ...
    def visit_code(self, node: "CodeNode") -> Any: ...
    def visit_block(self, node: "BlockNode") -> Any: ...


T = TypeVar("T", bound="ASTNode")


@dataclass
class ASTNode:
    """
    Base class for all AST nodes in Nomenic Core.
    """

    children: list["ASTNode"] = field(default_factory=list)
    value: Optional[Any] = None

    def accept(self, visitor: Visitor) -> Any:
        """
        Accept a visitor to process this node.

        This is part of the Visitor pattern implementation.

        Args:
            visitor: The visitor to process this node

        Returns:
            The result of the visitor's visit method for this node
        """
        method_name = f"visit_{self.__class__.__name__.lower().replace('node', '')}"
        method = getattr(visitor, method_name, visitor.visit_block)
        return method(self)

    def normalize(self: T) -> T:
        """
        Normalize the node structure for consistent output.

        This performs basic normalization like:
        - Removing empty text
        - Flattening unnecessary nested structures
        - Standardizing whitespace

        Returns:
            The normalized node (self)
        """
        # Normalize children recursively
        self.children = [child.normalize() for child in self.children if child]

        # Remove empty children
        self.children = [
            child
            for child in self.children
            if not (isinstance(child, TextNode) and not child.text.strip())
        ]

        return self

    def optimize(self: T) -> T:
        """
        Optimize the AST for better performance.

        This might combine nodes, eliminate redundancies, or
        perform other optimizations.

        Returns:
            The optimized node (self)
        """
        # Optimize children recursively
        self.children = [child.optimize() for child in self.children]

        return self


@dataclass
class DocumentNode(ASTNode):
    """
    Root node representing the entire document.
    """

    def normalize(self) -> "DocumentNode":
        """
        Normalize the document structure.

        For a document, we ensure:
        - Meta block is at the beginning if present
        - Remove duplicate blocks or merge similar consecutive blocks

        Returns:
            The normalized document node
        """
        super().normalize()

        # Ensure meta block is at the beginning
        meta_blocks = [
            c
            for c in self.children
            if isinstance(c, BlockNode) and c.block_type == "meta"
        ]
        non_meta_blocks = [
            c
            for c in self.children
            if not (isinstance(c, BlockNode) and c.block_type == "meta")
        ]

        if meta_blocks:
            # Keep only the first meta block
            self.children = [meta_blocks[0], *non_meta_blocks]
        else:
            self.children = non_meta_blocks

        return self

    def optimize(self) -> "DocumentNode":
        """
        Optimize the document structure.

        Document-specific optimizations:
        - Merge adjacent text nodes
        - Flatten unnecessary nested structures

        Returns:
            The optimized document node
        """
        super().optimize()

        # Merge adjacent text nodes
        optimized_children = []
        i = 0
        while i < len(self.children):
            if (
                i < len(self.children) - 1
                and isinstance(self.children[i], TextNode)
                and isinstance(self.children[i + 1], TextNode)
            ):
                # Merge adjacent text nodes
                merged_text = self.children[i].text + "\n" + self.children[i + 1].text
                optimized_children.append(TextNode(text=merged_text))
                i += 2
            else:
                optimized_children.append(self.children[i])
                i += 1

        self.children = optimized_children
        return self


@dataclass
class HeaderNode(ASTNode):
    """
    Node representing a section header.
    """

    level: int = 1
    text: str = ""

    def normalize(self) -> "HeaderNode":
        """Normalize header text."""
        super().normalize()
        # Trim whitespace and normalize newlines
        self.text = self.text.strip()
        return self

    def optimize(self) -> "HeaderNode":
        """Optimize the header node."""
        super().optimize()
        # Headers typically don't need further optimization
        return self


@dataclass
class TextNode(ASTNode):
    """
    Node representing a paragraph or text block.
    """

    text: str = ""

    def normalize(self) -> "TextNode":
        """Normalize text content."""
        super().normalize()
        # Standardize whitespace
        if self.text:
            # Convert all line endings to \n
            self.text = self.text.replace("\r\n", "\n").replace("\r", "\n")
            # Handle trailing whitespace
            self.text = "\n".join(line.rstrip() for line in self.text.split("\n"))
        return self

    def optimize(self) -> "TextNode":
        """Optimize text node."""
        super().optimize()
        # Text nodes are already efficient
        return self


@dataclass
class ListNode(ASTNode):
    """
    Node representing a list block (unordered or ordered).
    """

    ordered: bool = False
    items: list["ListItemNode"] = field(default_factory=list)

    def normalize(self) -> "ListNode":
        """Normalize list items."""
        super().normalize()
        # Also normalize items list
        self.items = [item.normalize() for item in self.items if item]
        return self

    def optimize(self) -> "ListNode":
        """Optimize list structure."""
        super().optimize()
        # Also optimize items list
        self.items = [item.optimize() for item in self.items]
        return self


@dataclass
class ListItemNode(ASTNode):
    """
    Node representing a list item.
    """

    def normalize(self) -> "ListItemNode":
        """Normalize list item."""
        super().normalize()
        return self

    def optimize(self) -> "ListItemNode":
        """Optimize list item."""
        super().optimize()
        return self


@dataclass
class CodeNode(ASTNode):
    """
    Node representing a code block.
    """

    def normalize(self) -> "CodeNode":
        """Normalize code block."""
        super().normalize()
        return self

    def optimize(self) -> "CodeNode":
        """Optimize code block."""
        super().optimize()
        return self


@dataclass
class BlockNode(ASTNode):
    """
    Generic node for other block types (code, table, etc.).
    """

    block_type: str = ""
    meta: Optional[dict] = None

    def normalize(self) -> "BlockNode":
        """Normalize block content based on type."""
        super().normalize()

        # Type-specific normalization
        if self.block_type == "code":
            # For code blocks, preserve whitespace but ensure consistent line endings
            for i, child in enumerate(self.children):
                if isinstance(child, TextNode):
                    self.children[i].text = child.text.replace("\r\n", "\n").replace(
                        "\r", "\n"
                    )

        elif self.block_type == "table":
            # For tables, ensure each row is a separate child
            pass

        return self

    def optimize(self) -> "BlockNode":
        """Optimize block structure based on type."""
        super().optimize()
        return self
