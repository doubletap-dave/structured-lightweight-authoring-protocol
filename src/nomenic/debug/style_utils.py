"""Style token inspection and analysis utilities for Nomenic debug module."""

import re
import sys
from typing import Dict, List, Optional, Union

# Try absolute imports first (recommended approach)
try:
    from nomenic.lexer import Lexer
    from nomenic.tokens import TokenType
except ImportError:
    # Fall back to relative imports if absolute imports fail
    try:
        from ..lexer import Lexer
        from ..tokens import TokenType
    except ImportError:
        print("ERROR: Failed to import Nomenic core components. Please make sure the package is properly installed.")
        sys.exit(1)


def analyze_styles(
    content: str,
    style_type: Optional[str] = None,
    include_matches: bool = True,
) -> Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]:
    """
    Analyze and inspect style tokens in a Nomenic document.

    Args:
        content: The document content to analyze
        style_type: Optional filter for specific style type (bold, italic, code, link)
        include_matches: Whether to include regex match information

    Returns:
        Dictionary with style analysis information
    """
    # Tokenize the content
    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Get all style tokens
    style_tokens = [
        t
        for t in tokens
        if t.type
        in (
            TokenType.STYLE_BOLD,
            TokenType.STYLE_ITALIC,
            TokenType.STYLE_CODE,
            TokenType.STYLE_LINK,
        )
    ]

    # Filter by style type if specified
    if style_type:
        style_token_map = {
            "bold": TokenType.STYLE_BOLD,
            "italic": TokenType.STYLE_ITALIC,
            "code": TokenType.STYLE_CODE,
            "link": TokenType.STYLE_LINK,
        }

        if style_type.lower() not in style_token_map:
            raise ValueError(
                f"Invalid style type: {style_type}. Valid types: bold, italic, code, link"
            )

        style_tokens = [
            t for t in style_tokens if t.type == style_token_map[style_type.lower()]
        ]

    # Format style tokens for output
    formatted_styles = []
    for token in style_tokens:
        style_info = {
            "type": token.type.name,
            "value": token.value,
            "line": token.line,
            "column": token.column,
        }
        formatted_styles.append(style_info)

    result = {
        "total_styles": len(style_tokens),
        "styles": formatted_styles,
    }

    # Add direct regex matches if requested
    if include_matches:
        result["matches"] = _check_style_patterns(content)

    return result


def find_style_in_lines(
    content: str,
    style_marker: str = "@",
) -> Dict[str, List[Dict[str, Union[str, int]]]]:
    """
    Find lines containing style markers and associated tokens.

    Args:
        content: The document content to analyze
        style_marker: The style marker to search for (default: @)

    Returns:
        Dictionary with line information
    """
    # Tokenize the content
    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Split content into lines
    lines = content.splitlines()

    # Find lines with style markers
    result = {"lines": []}

    for i, line in enumerate(lines):
        if style_marker in line:
            line_num = i + 1  # Convert to 1-indexed

            # Find text tokens on this line
            text_tokens = [
                t for t in tokens if t.type == TokenType.TEXT and t.line == line_num
            ]

            # Find style tokens on this line
            style_tokens = [
                t
                for t in tokens
                if t.type
                in (
                    TokenType.STYLE_BOLD,
                    TokenType.STYLE_ITALIC,
                    TokenType.STYLE_CODE,
                    TokenType.STYLE_LINK,
                )
                and t.line == line_num
            ]

            # Add line info to result
            line_info = {
                "line_number": line_num,
                "content": line,
                "text_tokens": [
                    {
                        "type": t.type.name,
                        "value": t.value,
                        "column": t.column,
                    }
                    for t in text_tokens
                ],
                "style_tokens": [
                    {
                        "type": t.type.name,
                        "value": t.value,
                        "column": t.column,
                    }
                    for t in style_tokens
                ],
            }

            result["lines"].append(line_info)

    # Add summary
    result["total_lines"] = len(result["lines"])

    return result


def _check_style_patterns(content: str) -> Dict[str, List[Dict[str, str]]]:
    """Test style regex patterns against content."""
    # Define regex patterns for different styles
    patterns = {
        "bold": re.compile(r"@b\(([^)]*)\)|@bold\(([^)]*)\)"),
        "italic": re.compile(r"@i\(([^)]*)\)|@italic\(([^)]*)\)"),
        "code": re.compile(r"@c\(([^)]*)\)|@code\(([^)]*)\)"),
        "link": re.compile(r"@l\(([^)]*)\)|@link\(([^)]*)\)"),
    }

    results = {}

    # Find all matches for each style pattern
    for style, pattern in patterns.items():
        matches = list(pattern.finditer(content))

        formatted_matches = []
        for match in matches:
            match_info = {
                "full_match": match.group(0),
                "content": match.group(1) or match.group(2),
                "start": match.start(),
                "end": match.end(),
            }
            formatted_matches.append(match_info)

        results[style] = formatted_matches

    return results
