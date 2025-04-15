# Nomenic Core - Lexer (Tokenizer)

# This file will contain the lexer implementation.
# It reads the input string (.nmc content) and yields Tokens. 

import re
from typing import Generator, List, Optional, Match, Tuple
import io

from .tokens import Token, TokenType, TOKEN_MAP
from .errors import LexerError

class Lexer:
    """
    Tokenizes Nomenic Core content according to the language specification.
    
    The lexer reads input text and generates a stream of tokens that the parser
    can use to build the AST.
    """
    
    def __init__(self, content: str):
        """
        Initialize the lexer with Nomenic content.
        
        Args:
            content: The string content of a Nomenic file
        """
        self.content = content
        self.lines = content.splitlines()
        self.line_idx = 0  # Current line (0-indexed)
        self.col_idx = 0   # Current column (0-indexed)
        self.current_line = self.lines[0] if self.lines else ""
        
        # Regular expression patterns
        self.re_indentation = re.compile(r'^(\s+)')
        self.re_block_token = re.compile(r'^([a-zA-Z0-9_-]+):\s+')
        self.re_list_item = re.compile(r'^-\s+')
        self.re_ordered_list_item = re.compile(r'^(\d+|[a-zA-Z]+)\.(\s+)')
        self.re_custom_directive = re.compile(r'^x-([a-zA-Z0-9_-]+):\s+')
        self.re_callout = re.compile(r'^(note|warn|tip):\s+')
        self.re_inline_annotation_paren = re.compile(r'\([^)]*\)')
        self.re_inline_annotation_bracket = re.compile(r'\[[^\]]*\]')
        self.re_inline_key_value = re.compile(r'\{[^}]*\}')
        self.re_style_bold = re.compile(r'@b\(([^)]*)\)|@bold\(([^)]*)\)')
        self.re_style_italic = re.compile(r'@i\(([^)]*)\)|@italic\(([^)]*)\)')
        self.re_style_code = re.compile(r'@c\(([^)]*)\)|@code\(([^)]*)\)')
        self.re_style_link = re.compile(r'@l\(([^)]*)\)|@link\(([^)]*)\)')

    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire content and return a list of tokens.
        
        Returns:
            List of Token objects representing the content
        """
        return list(self.generate_tokens())
    
    def generate_tokens(self) -> Generator[Token, None, None]:
        """
        Generate tokens from the content.
        
        Yields:
            Token objects as they are recognized
        """
        while self.line_idx < len(self.lines):
            self.current_line = self.lines[self.line_idx]
            self.col_idx = 0
            
            # Process the current line
            yield from self._tokenize_line()
            
            # Move to the next line
            self.line_idx += 1
            
            # Add NEWLINE token (except for the last line)
            if self.line_idx < len(self.lines):
                yield Token(
                    type=TokenType.NEWLINE,
                    value="\n",
                    line=self.line_idx,
                    column=len(self.current_line) + 1,
                    indent_level=0
                )
        
        # Add EOF token
        yield Token(
            type=TokenType.EOF,
            value="",
            line=self.line_idx + 1,
            column=1,
            indent_level=0
        )
    
    def _tokenize_line(self) -> Generator[Token, None, None]:
        """
        Tokenize a single line of content.
        
        Yields:
            Token objects for the current line
        """
        line = self.current_line
        
        # Skip empty lines (just yield a NEWLINE)
        if not line.strip():
            return
        
        # Process indentation
        indent_level = 0
        indent_match = self.re_indentation.match(line)
        if indent_match:
            indent_str = indent_match.group(1)
            indent_level = len(indent_str) // 2  # Assuming 2 spaces per level
            
            # Check if indentation is valid (multiples of 2 spaces)
            if len(indent_str) % 2 != 0:
                raise LexerError(f"Invalid indentation at line {self.line_idx + 1}. Must be multiples of 2 spaces.")
            
            yield Token(
                type=TokenType.INDENTATION,
                value=indent_str,
                line=self.line_idx + 1,
                column=1,
                indent_level=indent_level
            )
            
            self.col_idx = len(indent_str)
        
        # Check for comments
        if line[self.col_idx:].strip().startswith('#'):
            yield Token(
                type=TokenType.COMMENT,
                value=line[self.col_idx:],
                line=self.line_idx + 1,
                column=self.col_idx + 1,
                indent_level=indent_level
            )
            return
        
        # Check for list items
        list_match = self.re_list_item.match(line[self.col_idx:])
        if list_match:
            yield Token(
                type=TokenType.LIST_ITEM,
                value=list_match.group(0),
                line=self.line_idx + 1,
                column=self.col_idx + 1,
                indent_level=indent_level
            )
            self.col_idx += len(list_match.group(0))
            
            # Process the rest of the line as content
            if self.col_idx < len(line):
                yield Token(
                    type=TokenType.TEXT,
                    value=line[self.col_idx:],
                    line=self.line_idx + 1,
                    column=self.col_idx + 1,
                    indent_level=indent_level
                )
            return
        
        # Check for ordered list items
        ordered_list_match = self.re_ordered_list_item.match(line[self.col_idx:])
        if ordered_list_match:
            marker, whitespace = ordered_list_match.groups()
            yield Token(
                type=TokenType.ORDERED_LIST_ITEM,
                value=f"{marker}.{whitespace}",
                line=self.line_idx + 1,
                column=self.col_idx + 1,
                indent_level=indent_level,
                metadata={"marker": marker}
            )
            self.col_idx += len(ordered_list_match.group(0))
            
            # Process the rest of the line as content
            if self.col_idx < len(line):
                yield Token(
                    type=TokenType.TEXT,
                    value=line[self.col_idx:],
                    line=self.line_idx + 1,
                    column=self.col_idx + 1,
                    indent_level=indent_level
                )
            return
        
        # Check for block tokens (e.g., "header:", "text:")
        block_match = self.re_block_token.match(line[self.col_idx:])
        if block_match:
            token_str = block_match.group(1) + ":"
            token_type = TOKEN_MAP.get(token_str, None)
            
            # Check for token aliases (short forms)
            if token_type is None:
                token_type = TOKEN_MAP.get(token_str.lower(), None)
            
            # If still None, it might be a custom directive or unknown token
            if token_type is None:
                custom_directive_match = self.re_custom_directive.match(line[self.col_idx:])
                callout_match = self.re_callout.match(line[self.col_idx:])
                
                if custom_directive_match:
                    directive_name = custom_directive_match.group(1)
                    token_str = f"x-{directive_name}:"
                    token_type = TokenType.CUSTOM_DIRECTIVE
                    self.col_idx += len(custom_directive_match.group(0))
                    
                    yield Token(
                        type=token_type,
                        value=token_str,
                        line=self.line_idx + 1,
                        column=self.col_idx - len(custom_directive_match.group(0)) + 1,
                        indent_level=indent_level,
                        metadata={"directive_name": directive_name}
                    )
                    
                    # Process rest of line as content
                    if self.col_idx < len(line):
                        yield Token(
                            type=TokenType.TEXT,
                            value=line[self.col_idx:],
                            line=self.line_idx + 1,
                            column=self.col_idx + 1,
                            indent_level=indent_level
                        )
                    
                    return
                
                elif callout_match:
                    callout_type = callout_match.group(1)
                    token_str = f"{callout_type}:"
                    token_type = TokenType.CALLOUT
                    self.col_idx += len(callout_match.group(0))
                    
                    yield Token(
                        type=token_type,
                        value=token_str,
                        line=self.line_idx + 1,
                        column=self.col_idx - len(callout_match.group(0)) + 1,
                        indent_level=indent_level,
                        metadata={"callout_type": callout_type}
                    )
                    
                    # Process rest of line as content
                    if self.col_idx < len(line):
                        yield Token(
                            type=TokenType.TEXT,
                            value=line[self.col_idx:],
                            line=self.line_idx + 1,
                            column=self.col_idx + 1,
                            indent_level=indent_level
                        )
                    
                    return
                
                else:
                    # Unknown token, treat as plain text
                    yield Token(
                        type=TokenType.TEXT,
                        value=line[self.col_idx:],
                        line=self.line_idx + 1,
                        column=self.col_idx + 1,
                        indent_level=indent_level
                    )
                    return
            
            self.col_idx += len(block_match.group(0))
            
            yield Token(
                type=token_type,
                value=token_str,
                line=self.line_idx + 1,
                column=self.col_idx - len(block_match.group(0)) + 1,
                indent_level=indent_level
            )
            
            # Process rest of line as content
            if self.col_idx < len(line):
                # Check for multiline text block start/end
                if line[self.col_idx:].strip() == ">>>":
                    yield Token(
                        type=TokenType.TEXT_BLOCK_START,
                        value=">>>",
                        line=self.line_idx + 1,
                        column=self.col_idx + 1,
                        indent_level=indent_level
                    )
                elif line[self.col_idx:].strip() == "<<<":
                    yield Token(
                        type=TokenType.TEXT_BLOCK_END,
                        value="<<<",
                        line=self.line_idx + 1,
                        column=self.col_idx + 1,
                        indent_level=indent_level
                    )
                else:
                    yield Token(
                        type=TokenType.TEXT,
                        value=line[self.col_idx:],
                        line=self.line_idx + 1,
                        column=self.col_idx + 1,
                        indent_level=indent_level
                    )
            return
        
        # If none of the above, treat the rest of the line as plain text
        yield Token(
            type=TokenType.TEXT,
            value=line[self.col_idx:],
            line=self.line_idx + 1,
            column=self.col_idx + 1,
            indent_level=indent_level
        )


def tokenize(content: str) -> List[Token]:
    """Convenience function to tokenize Nomenic content."""
    lexer = Lexer(content)
    return lexer.tokenize() 