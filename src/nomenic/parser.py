# Nomenic Core - Parser

# This file will contain the parser implementation.
# It takes a stream of tokens from the lexer and builds an AST.

from typing import Optional

from .ast import DocumentNode  # Add other necessary AST node types
from .tokens import Token, TokenType


class Parser:
    """
    Parses a stream of Nomenic Core tokens into an Abstract Syntax Tree (AST).
    """

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def parse(self) -> DocumentNode:
        """Parse the token stream into a DocumentNode."""
        # Placeholder: Actual parsing logic will go here
        # This will involve consuming tokens and building the AST structure
        # based on the Nomenic grammar rules.

        # Example of how it might start:
        # document = DocumentNode()
        # while not self._is_at_end():
        #     node = self._parse_block()
        #     if node:
        #         document.add_child(node)
        # return document

        raise NotImplementedError("Parser logic not yet implemented.")

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
        peeked_token = self._peek()
        return peeked_token is not None and peeked_token.type == TokenType.EOF

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

    # Placeholder for block parsing logic
    # def _parse_block(self):
    #     # ... logic to determine and parse the next block (header, section,
    #     # list, etc.)
    #     pass


def parse(tokens: list[Token]) -> DocumentNode:
    """Convenience function to parse Nomenic tokens."""
    parser = Parser(tokens)
    return parser.parse()
