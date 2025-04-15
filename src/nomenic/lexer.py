# Nomenic Core - Lexer (Tokenizer)

# This file will contain the lexer implementation.
# It reads the input string (.nmc content) and yields Tokens.

import re
from collections.abc import Generator

from .errors import LexerError
from .tokens import TOKEN_MAP, Token, TokenType


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
        self.col_idx = 0  # Current column (0-indexed)
        self.current_line = self.lines[0] if self.lines else ""

        # Regular expression patterns
        self.re_indentation = re.compile(r"^(\s+)")
        # Stricter block token key: Allow letters, numbers, underscore, hyphen
        self.re_block_token_key = r"[a-zA-Z0-9_-]+"  # nosec B105
        # Make whitespace after colon optional by changing \s+ to \s*
        self.re_block_token = re.compile(rf"^({self.re_block_token_key}):\s*")
        self.re_list_item = re.compile(r"^-\s+")
        # Stricter list marker: Allow numbers or single letters
        self.re_ordered_list_item = re.compile(r"^(\d+|[a-zA-Z])\.(\s+)")
        # Stricter custom directive key - also make whitespace optional
        self.re_custom_directive = re.compile(rf"^x-({self.re_block_token_key}):\s*")
        # Make whitespace optional for callouts too
        self.re_callout = re.compile(r"^(note|warn|tip):\s*")
        self.re_inline_annotation_paren = re.compile(r"\([^)]*\)")
        self.re_inline_annotation_bracket = re.compile(r"\[[^\]]*\]")
        self.re_inline_key_value = re.compile(r"\{[^}]*\}")
        self.re_style_bold = re.compile(r"@b\(([^)]*)\)|@bold\(([^)]*)\)")
        self.re_style_italic = re.compile(r"@i\(([^)]*)\)|@italic\(([^)]*)\)")
        self.re_style_code = re.compile(r"@c\(([^)]*)\)|@code\(([^)]*)\)")
        self.re_style_link = re.compile(r"@l\(([^)]*)\)|@link\(([^)]*)\)")

    def tokenize(self) -> list[Token]:
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
        if not self.lines:
            yield Token(type=TokenType.EOF, value="", line=1, column=1)
            return

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
                    value="\\n",
                    line=self.line_idx,
                    column=len(self.current_line) + 1,
                    indent_level=0,
                )

        # Add EOF token
        yield Token(
            type=TokenType.EOF,
            value="",
            line=self.line_idx + 1,
            column=1,
            indent_level=0,
        )

    def _tokenize_line(self) -> Generator[Token, None, None]:
        """
        Tokenize a single line of content.
        # Complexity ignored via Ruff config (PLR0911, PLR0912, PLR0915)

        Yields:
            Token objects for the current line
        """
        line = self.current_line
        if not line.strip():
            return

        indent_level = 0
        indent_match = self.re_indentation.match(line)
        if indent_match:
            indent_str = indent_match.group(1)
            indent_level = len(indent_str) // 2
            if len(indent_str) % 2 != 0:
                raise LexerError(
                    f"Invalid indentation at line {self.line_idx + 1}. "
                    f"Must be multiples of 2 spaces."
                )
            yield Token(
                type=TokenType.INDENTATION,
                value=indent_str,
                line=self.line_idx + 1,
                column=1,
                indent_level=indent_level,
            )
            self.col_idx = len(indent_str)

        remaining_line = line[self.col_idx :]
        remaining_line_stripped = remaining_line.strip()

        # --- Handle indented lines differently ---
        if indent_level > 0:
            # Check for block tokens first at any indentation level
            block_match = self.re_block_token.match(remaining_line)
            if block_match:
                token_key = block_match.group(1)
                token_str = f"{token_key}:"
                token_type = TOKEN_MAP.get(token_str)
                if token_type is None:
                    token_type = TOKEN_MAP.get(token_str.lower())

                # If it's a recognized block token (from TOKEN_MAP), process it
                if token_type is not None:
                    match_len = len(block_match.group(0))
                    token_col_start = self.col_idx + 1
                    self.col_idx += match_len

                    # Special handling for code blocks to include the code content
                    if token_type == TokenType.CODE:
                        # Extract the rest of the current line
                        rest_of_line = line[self.col_idx :].strip()

                        # Check if this is a code block with '|' marker (multi-line)
                        if rest_of_line == "|":
                            # Collect the code content from subsequent lines
                            code_content = []
                            next_line_idx = self.line_idx + 1

                            # Continue collecting until we find a line with a different
                            # indentation level
                            while (
                                next_line_idx < len(self.lines)
                                and self.lines[next_line_idx].strip()
                                and self.lines[next_line_idx].startswith(
                                    " " * (indent_level * 2 + 2)
                                )
                            ):
                                code_content.append(self.lines[next_line_idx].lstrip())
                                next_line_idx += 1

                            # Join the code lines and create a CODE token with the full
                            # content
                            code_str = "\n".join(code_content)
                            yield Token(
                                type=token_type,
                                value=code_str,
                                line=self.line_idx + 1,
                                column=token_col_start,
                                indent_level=indent_level,
                            )

                            # Skip the lines we've consumed
                            self.line_idx = (
                                next_line_idx - 1
                            )  # -1 because main loop increments
                            return  # Processed code block

                    # Special handling for text blocks with inline styles
                    elif token_type == TokenType.TEXT:
                        # First yield the TEXT token itself
                        yield Token(
                            type=token_type,
                            value=token_str,
                            line=self.line_idx + 1,
                            column=token_col_start,
                            indent_level=indent_level,
                        )

                        # If there's content after "text:", process it for inline styles
                        if self.col_idx < len(line):
                            remaining_text = line[self.col_idx :].strip()

                            # Process text for inline styles if '@' is present
                            if "@" in remaining_text:
                                current_pos = 0
                                text_len = len(remaining_text)

                                # Find all style patterns
                                bold_matches = list(
                                    self.re_style_bold.finditer(remaining_text)
                                )
                                italic_matches = list(
                                    self.re_style_italic.finditer(remaining_text)
                                )
                                code_matches = list(
                                    self.re_style_code.finditer(remaining_text)
                                )
                                link_matches = list(
                                    self.re_style_link.finditer(remaining_text)
                                )

                                # Combine all matches and sort by position
                                all_matches = []
                                for match in bold_matches:
                                    all_matches.append(
                                        (
                                            match.start(),
                                            match.end(),
                                            TokenType.STYLE_BOLD,
                                            match.group(1) or match.group(2),
                                        )
                                    )
                                for match in italic_matches:
                                    all_matches.append(
                                        (
                                            match.start(),
                                            match.end(),
                                            TokenType.STYLE_ITALIC,
                                            match.group(1) or match.group(2),
                                        )
                                    )
                                for match in code_matches:
                                    all_matches.append(
                                        (
                                            match.start(),
                                            match.end(),
                                            TokenType.STYLE_CODE,
                                            match.group(1) or match.group(2),
                                        )
                                    )
                                for match in link_matches:
                                    all_matches.append(
                                        (
                                            match.start(),
                                            match.end(),
                                            TokenType.STYLE_LINK,
                                            match.group(1) or match.group(2),
                                        )
                                    )

                                all_matches.sort()  # Sort by start position

                                # Process styles if we found any
                                if all_matches:
                                    # Text before first style
                                    if all_matches[0][0] > 0:
                                        yield Token(
                                            type=TokenType.TEXT,
                                            value=remaining_text[: all_matches[0][0]],
                                            line=self.line_idx + 1,
                                            column=self.col_idx + 1,
                                            indent_level=indent_level,
                                        )

                                    # Process each style
                                    for i, (
                                        start,
                                        end,
                                        token_type,
                                        content,
                                    ) in enumerate(all_matches):
                                        # Yield the style token
                                        yield Token(
                                            type=token_type,
                                            value=content,
                                            line=self.line_idx + 1,
                                            column=self.col_idx + start + 1,
                                            indent_level=indent_level,
                                        )

                                        # Text between this style and the next (if any)
                                        if i < len(all_matches) - 1:
                                            next_start = all_matches[i + 1][0]
                                            if next_start > end:
                                                yield Token(
                                                    type=TokenType.TEXT,
                                                    value=remaining_text[
                                                        end:next_start
                                                    ],
                                                    line=self.line_idx + 1,
                                                    column=self.col_idx + end + 1,
                                                    indent_level=indent_level,
                                                )

                                    # Text after the last style
                                    last_end = all_matches[-1][1]
                                    if last_end < text_len:
                                        yield Token(
                                            type=TokenType.TEXT,
                                            value=remaining_text[last_end:],
                                            line=self.line_idx + 1,
                                            column=self.col_idx + last_end + 1,
                                            indent_level=indent_level,
                                        )
                                else:
                                    # No matches found, just yield the text
                                    yield Token(
                                        type=TokenType.TEXT,
                                        value=remaining_text,
                                        line=self.line_idx + 1,
                                        column=self.col_idx + 1,
                                        indent_level=indent_level,
                                    )
                            else:
                                # No @ symbol, just yield as regular text
                                yield Token(
                                    type=TokenType.TEXT,
                                    value=remaining_text,
                                    line=self.line_idx + 1,
                                    column=self.col_idx + 1,
                                    indent_level=indent_level,
                                )
                        return  # Processed indented text with potential styles

                    # For other block tokens
                    else:
                        yield Token(
                            type=token_type,
                            value=token_str,
                            line=self.line_idx + 1,
                            column=token_col_start,
                            indent_level=indent_level,
                        )

                    # If there's any content on the same line (and it's not handled by a
                    # special case above)
                    if (
                        token_type != TokenType.TEXT
                        and token_type != TokenType.CODE
                        and self.col_idx < len(line)
                    ):
                        yield Token(
                            type=TokenType.TEXT,
                            value=line[self.col_idx :],
                            line=self.line_idx + 1,
                            column=self.col_idx + 1,
                            indent_level=indent_level,
                        )
                    return  # Processed indented block token

                # For custom directives and callouts
                elif token_key.startswith("x-") or token_key in ("note", "warn", "tip"):
                    custom_directive_match = self.re_custom_directive.match(
                        remaining_line
                    )
                    callout_match = self.re_callout.match(remaining_line)

                    if custom_directive_match:
                        directive_name = custom_directive_match.group(1)
                        token_str = f"x-{directive_name}:"
                        match_len = len(custom_directive_match.group(0))
                        token_col_start = self.col_idx + 1
                        self.col_idx += match_len
                        yield Token(
                            type=TokenType.CUSTOM_DIRECTIVE,
                            value=token_str,
                            line=self.line_idx + 1,
                            column=token_col_start,
                            indent_level=indent_level,
                            metadata={"directive_name": directive_name},
                        )

                        # Process rest of line as TEXT
                        if self.col_idx < len(line):
                            yield Token(
                                type=TokenType.TEXT,
                                value=line[self.col_idx :],
                                line=self.line_idx + 1,
                                column=self.col_idx + 1,
                                indent_level=indent_level,
                            )
                        return  # Processed indented custom directive

                    elif callout_match:
                        callout_type = callout_match.group(1)
                        token_str = f"{callout_type}:"
                        match_len = len(callout_match.group(0))
                        token_col_start = self.col_idx + 1
                        self.col_idx += match_len
                        yield Token(
                            type=TokenType.CALLOUT,
                            value=token_str,
                            line=self.line_idx + 1,
                            column=token_col_start,
                            indent_level=indent_level,
                            metadata={"callout_type": callout_type},
                        )

                        # Process rest of line as TEXT
                        if self.col_idx < len(line):
                            yield Token(
                                type=TokenType.TEXT,
                                value=line[self.col_idx :],
                                line=self.line_idx + 1,
                                column=self.col_idx + 1,
                                indent_level=indent_level,
                            )
                        return  # Processed indented callout

            # Now check for list items
            list_match = self.re_list_item.match(remaining_line)
            ordered_list_match = self.re_ordered_list_item.match(remaining_line)

            if list_match:
                match_len = len(list_match.group(0))
                yield Token(
                    type=TokenType.LIST_ITEM,
                    value=list_match.group(0),
                    line=self.line_idx + 1,
                    column=self.col_idx + 1,
                    indent_level=indent_level,
                )
                self.col_idx += match_len
                # Yield rest of line as TEXT if anything remains
                if self.col_idx < len(line):
                    yield Token(
                        type=TokenType.TEXT,
                        value=line[self.col_idx :],
                        line=self.line_idx + 1,
                        column=self.col_idx + 1,
                        indent_level=indent_level,
                    )
                return  # Processed indented list item

            elif ordered_list_match:
                marker, whitespace = ordered_list_match.groups()
                match_len = len(ordered_list_match.group(0))
                yield Token(
                    type=TokenType.ORDERED_LIST_ITEM,
                    value=f"{marker}.{whitespace}",
                    line=self.line_idx + 1,
                    column=self.col_idx + 1,
                    indent_level=indent_level,
                    metadata={"marker": marker},
                )
                self.col_idx += match_len
                # Yield rest of line as TEXT if anything remains
                if self.col_idx < len(line):
                    yield Token(
                        type=TokenType.TEXT,
                        value=line[self.col_idx :],
                        line=self.line_idx + 1,
                        column=self.col_idx + 1,
                        indent_level=indent_level,
                    )
                return  # Processed indented ordered list item

            else:
                # Treat the entire remaining indented line as TEXT
                yield Token(
                    type=TokenType.TEXT,
                    value=remaining_line,
                    line=self.line_idx + 1,
                    column=self.col_idx + 1,
                    indent_level=indent_level,
                )
                return  # Processed indented line as TEXT

        # --- Continue with original logic for indent_level == 0 ---

        # Check for comments FIRST at indent 0
        if remaining_line_stripped.startswith("#"):
            yield Token(
                type=TokenType.COMMENT,
                value=remaining_line,
                line=self.line_idx + 1,
                column=self.col_idx + 1,
                indent_level=indent_level,
            )
            return  # Comments consume the whole line

        processed_start = False
        # --- Check for specific line start patterns (indent_level == 0) ---

        # Check for list items
        list_match = self.re_list_item.match(remaining_line)
        if list_match:
            processed_start = True
            match_len = len(list_match.group(0))
            yield Token(
                type=TokenType.LIST_ITEM,
                value=list_match.group(0),
                line=self.line_idx + 1,
                column=self.col_idx + 1,
                indent_level=indent_level,
            )
            self.col_idx += match_len

        # Check for ordered list items
        elif self.re_ordered_list_item.match(remaining_line):
            processed_start = True
            ordered_list_match = self.re_ordered_list_item.match(remaining_line)
            marker, whitespace = ordered_list_match.groups()
            match_len = len(ordered_list_match.group(0))
            yield Token(
                type=TokenType.ORDERED_LIST_ITEM,
                value=f"{marker}.{whitespace}",
                line=self.line_idx + 1,
                column=self.col_idx + 1,
                indent_level=indent_level,
                metadata={"marker": marker},
            )
            self.col_idx += match_len

        # Check for block tokens (standard, custom, callout)
        # This needs careful checking to differentiate known, custom, callout,
        # vs unknown
        else:
            block_match = self.re_block_token.match(remaining_line)
            if block_match:
                token_key = block_match.group(1)
                token_str = f"{token_key}:"

                token_type = TOKEN_MAP.get(token_str)
                if token_type is None:
                    token_type = TOKEN_MAP.get(token_str.lower())

                # Case 1: Known Block Token
                if token_type is not None:
                    processed_start = True
                    match_len = len(block_match.group(0))
                    token_col_start = self.col_idx + 1
                    self.col_idx += match_len
                    yield Token(
                        type=token_type,
                        value=token_str,
                        line=self.line_idx + 1,
                        column=token_col_start,
                        indent_level=indent_level,
                    )
                # Case 2: Potential Custom Directive or Callout
                elif token_key.startswith("x-") or token_key in (
                    "note",
                    "warn",
                    "tip",
                ):
                    custom_directive_match = self.re_custom_directive.match(
                        remaining_line
                    )
                    callout_match = self.re_callout.match(remaining_line)

                    if custom_directive_match:
                        processed_start = True
                        directive_name = custom_directive_match.group(1)
                        token_str = f"x-{directive_name}:"
                        match_len = len(custom_directive_match.group(0))
                        token_col_start = self.col_idx + 1
                        self.col_idx += match_len
                        yield Token(
                            type=TokenType.CUSTOM_DIRECTIVE,
                            value=token_str,
                            line=self.line_idx + 1,
                            column=token_col_start,
                            indent_level=indent_level,
                            metadata={"directive_name": directive_name},
                        )
                    elif callout_match:
                        processed_start = True
                        callout_type = callout_match.group(1)
                        token_str = f"{callout_type}:"
                        match_len = len(callout_match.group(0))
                        token_col_start = self.col_idx + 1
                        self.col_idx += match_len
                        yield Token(
                            type=TokenType.CALLOUT,
                            value=token_str,
                            line=self.line_idx + 1,
                            column=token_col_start,
                            indent_level=indent_level,
                            metadata={"callout_type": callout_type},
                        )
                    # Case 3: Looks like a block token but isn't known/custom/callout
                    else:
                        # Fall through to TEXT handling if it matched block_token but
                        # wasn't a valid custom/callout
                        pass
                # Case 4: Matched block pattern but wasn't known/custom/callout type
                else:
                    # Fall through to TEXT handling
                    pass
            # Case 5: Did not match re_block_token at all (likely just plain text)
            # else: # No need for explicit else, fallthrough to TEXT works
            #     pass

        # --- Process the rest of the line as TEXT ---
        if self.col_idx < len(line) or not processed_start:
            start_col = self.col_idx + 1  # Text starts after the prefix/indent
            text_value = line[self.col_idx :]

            # Adjust if no prefix was processed (whole line is text)
            if not processed_start:
                # Text starts at column 1 (after potential indent)
                start_col = 1
                text_value = remaining_line

            # Check for multiline text block start/end
            if text_value.strip() == ">>>":
                yield Token(
                    type=TokenType.TEXT_BLOCK_START,
                    value=">>>",
                    line=self.line_idx + 1,
                    column=start_col,
                    indent_level=indent_level,
                )
            elif text_value.strip() == "<<<":
                yield Token(
                    type=TokenType.TEXT_BLOCK_END,
                    value="<<<",
                    line=self.line_idx + 1,
                    column=start_col,
                    indent_level=indent_level,
                )
            elif text_value:  # Don't yield empty TEXT tokens
                # Process the text for inline styles
                current_pos = 0
                text_len = len(text_value)

                # Only try to process if there might be styles (@)
                if "@" in text_value:
                    # Find all style patterns
                    bold_matches = list(self.re_style_bold.finditer(text_value))
                    italic_matches = list(self.re_style_italic.finditer(text_value))
                    code_matches = list(self.re_style_code.finditer(text_value))
                    link_matches = list(self.re_style_link.finditer(text_value))

                    # Combine all matches and sort by position
                    all_matches = []
                    for match in bold_matches:
                        all_matches.append(
                            (
                                match.start(),
                                match.end(),
                                TokenType.STYLE_BOLD,
                                match.group(1) or match.group(2),
                            )
                        )
                    for match in italic_matches:
                        all_matches.append(
                            (
                                match.start(),
                                match.end(),
                                TokenType.STYLE_ITALIC,
                                match.group(1) or match.group(2),
                            )
                        )
                    for match in code_matches:
                        all_matches.append(
                            (
                                match.start(),
                                match.end(),
                                TokenType.STYLE_CODE,
                                match.group(1) or match.group(2),
                            )
                        )
                    for match in link_matches:
                        all_matches.append(
                            (
                                match.start(),
                                match.end(),
                                TokenType.STYLE_LINK,
                                match.group(1) or match.group(2),
                            )
                        )

                    all_matches.sort()  # Sort by start position

                    # Process text interleaved with style tokens
                    for start, end, token_type, content in all_matches:
                        # Emit any text before this style
                        if start > current_pos:
                            yield Token(
                                type=TokenType.TEXT,
                                value=text_value[current_pos:start],
                                line=self.line_idx + 1,
                                column=start_col + current_pos,
                                indent_level=indent_level,
                            )

                        # Emit the style token
                        yield Token(
                            type=token_type,
                            value=content,
                            line=self.line_idx + 1,
                            column=start_col + start,
                            indent_level=indent_level,
                        )

                        # Update current position
                        current_pos = end

                    # Emit any remaining text after the last style
                    if current_pos < text_len:
                        yield Token(
                            type=TokenType.TEXT,
                            value=text_value[current_pos:],
                            line=self.line_idx + 1,
                            column=start_col + current_pos,
                            indent_level=indent_level,
                        )
                else:
                    # No styles to process, just emit the text as is
                    yield Token(
                        type=TokenType.TEXT,
                        value=text_value,
                        line=self.line_idx + 1,
                        column=start_col,  # Use adjusted start column
                        indent_level=indent_level,
                    )


def tokenize(content: str) -> list[Token]:
    """Convenience function to tokenize Nomenic content."""
    lexer = Lexer(content)
    return lexer.tokenize()
