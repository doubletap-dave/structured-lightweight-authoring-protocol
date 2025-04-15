# Nomenic Core - Parser

# This file will contain the parser implementation.
# It takes a stream of tokens from the lexer and builds an AST. 

from .tokens import Token, TokenType
from .errors import ParserError, ValidationError, ExtensionError
from typing import List, Optional

class Parser:
    """
    Nomenic Core Parser with robust error handling and error collection.
    Takes a stream of tokens from the lexer and builds an AST (stub for now).
    """
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.errors = []  # Collects errors for graceful degradation

    def current_token(self) -> Optional[Token]:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def advance(self):
        self.position += 1

    def parse(self):
        """
        Main parse loop. Demonstrates error handling and logging.
        Returns a stub AST (None for now).
        """
        try:
            while self.current_token() and self.current_token().type != TokenType.EOF:
                token = self.current_token()
                # Example: check for required META block at start
                if token.type == TokenType.META:
                    self.advance()
                    # (Stub) parse meta block
                elif token.type in (TokenType.HEADER, TokenType.TEXT, TokenType.LIST, TokenType.CODE, TokenType.TABLE):
                    self.advance()
                    # (Stub) parse block
                elif token.type == TokenType.CUSTOM_DIRECTIVE:
                    # For now, raise extension error for unknown directives
                    self.errors.append(ExtensionError(f"Unknown custom directive at line {token.line}"))
                    self.advance()
                else:
                    # Unexpected token: raise parser error but continue
                    self.errors.append(ParserError(f"Unexpected token {token.type} at line {token.line}"))
                    self.advance()
        except (ParserError, ValidationError, ExtensionError) as e:
            self.errors.append(e)
        # Return stub AST (None) and collected errors
        return None, self.errors 