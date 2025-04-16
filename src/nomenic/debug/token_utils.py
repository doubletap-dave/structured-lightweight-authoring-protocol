"""Token inspection and analysis utilities for Nomenic debug module."""

import os
import re
import sys
from typing import Any, Dict, List, Optional, Union

from src.nomenic.lexer import Lexer
from src.nomenic.tokens import TOKEN_MAP, TokenType

# Import from parent package
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")))


def analyze_tokens(
    content: str,
    token_type: Optional[str] = None,
    show_position: bool = True,
    detailed: bool = False,
) -> List[Dict[str, Union[str, int]]]:
    """
    Analyze and inspect tokens in a Nomenic document.

    Args:
        content: The document content to analyze
        token_type: Optional filter for specific token type
        show_position: Whether to include position information
        detailed: Whether to include detailed token information

    Returns:
        List of token information dictionaries
    """
    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Filter by token type if specified
    if token_type:
        token_enum = getattr(TokenType, token_type.upper(), None)
        if not token_enum:
            valid_types = [t.name.lower() for t in TokenType]
            raise ValueError(
                f"Invalid token type: {token_type}. Valid types: {', '.join(valid_types)}"
            )
        tokens = [t for t in tokens if t.type == token_enum]

    # Build result with requested details
    result = []
    for token in tokens:
        token_info = {
            "type": token.type.name,
            "value": token.value,
        }

        if show_position:
            token_info.update(
                {
                    "line": token.line,
                    "column": token.column,
                }
            )

        if detailed:
            # Add context (surrounding lines) from the content
            lines = content.splitlines()
            line_idx = token.line - 1  # Convert to 0-indexed

            # Get context with 1 line before and after
            start_idx = max(0, line_idx - 1)
            end_idx = min(len(lines), line_idx + 2)
            context = lines[start_idx:end_idx]

            token_info.update(
                {
                    "context": context,
                    "context_line_start": start_idx + 1,  # Convert back to 1-indexed
                }
            )

        result.append(token_info)

    return result


def visualize_ast(content: str, **kwargs) -> Dict[str, any]:
    """
    Visualize the AST structure of a Nomenic document.

    Args:
        content: The document content to visualize
        **kwargs: Additional visualization options

    Returns:
        Dictionary with visualization information
    """
    from ..parser import Parser

    # Tokenize the content
    tokens = tokenize(content)

    # Parse into an AST
    parser = Parser(tokens)
    document = parser.parse()

    # TODO: Implement proper AST visualization
    # This is a placeholder that returns a basic representation
    return {
        "document_type": "Nomenic",
        "block_count": len(document.blocks) if hasattr(document, "blocks") else 0,
        "has_errors": len(parser.errors) > 0,
        "error_count": len(parser.errors),
    }


def check_token_patterns(
    content: str, line_number: Optional[int] = None
) -> Dict[str, bool]:
    """
    Test token regex patterns against content to diagnose tokenization issues.

    Args:
        content: The content to test patterns against
        line_number: Optional specific line to check

    Returns:
        Dictionary with pattern match results
    """
    lines = content.splitlines()

    # If line number specified, only check that line
    if line_number is not None:
        if 1 <= line_number <= len(lines):
            test_lines = [lines[line_number - 1]]  # Convert to 0-indexed
        else:
            raise ValueError(
                f"Line number {line_number} out of range (1-{len(lines)})")
    else:
        test_lines = lines

    results = {}

    # Test patterns for each line
    for i, line in enumerate(test_lines):
        line_idx = line_number if line_number else i + 1
        results[f"line_{line_idx}"] = {
            "content": line,
            "matches": _check_line_patterns(line),
        }

    return results


def _check_line_patterns(line: str) -> Dict[str, bool]:
    """Test various regex patterns against a single line."""
    patterns = {
        "block_token_strict": (
            r"^([a-zA-Z0-9_-]+):\s+",
            "Block token with required space",
        ),
        "block_token_flexible": (
            r"^([a-zA-Z0-9_-]+):\s*",
            "Block token with optional space",
        ),
        "list_item": (r"^\s*-\s+", "List item"),
        "code_block": (r"^\s*```", "Code block delimiter"),
        "multiline_start": (r"^\s*>>>", "Multiline text start"),
        "multiline_end": (r"^\s*<<<", "Multiline text end"),
    }

    results = {}
    for pattern_name, (regex, description) in patterns.items():
        pattern = re.compile(regex)
        match = pattern.match(line)
        results[pattern_name] = bool(match)

    # Special check for TOKEN_MAP keys
    if results["block_token_flexible"]:
        pattern = re.compile(patterns["block_token_flexible"][0])
        match = pattern.match(line)
        token_key = match.group(1)
        token_str = f"{token_key}:"
        results["token_in_map"] = token_str in TOKEN_MAP

    return results


def format_tokens_summary(tokens: list[dict[str, Any]]) -> str:
    """Format tokens as a text summary."""
    if not tokens:
        return "No tokens found"

    lines = []
    type_counts = {}

    # Count token types
    for token in tokens:
        token_type = token["type"]
        type_counts[token_type] = type_counts.get(token_type, 0) + 1

    # Format summary
    lines.append(f"Found {len(tokens)} tokens:")
    for token_type, count in type_counts.items():
        lines.append(f"  {token_type}: {count}")

    return "\n".join(lines)


def get_token_context(tokens: list[Token], index: int, context_lines: int = 2) -> dict[str, Any]:
    """Get context information for a token."""
    if not tokens or index < 0 or index >= len(tokens):
        return {"error": "Invalid token index"}

    token = tokens[index]
    context = {
        "token": {
            "type": token.type.name,
            "line": token.line,
            "column": token.column,
            "content": token.content
        },
        "before": [],
        "after": []
    }

    # Get tokens before the current one
    start_idx = max(0, index - context_lines)
    for i in range(start_idx, index):
        t = tokens[i]
        context["before"].append({
            "type": t.type.name,
            "line": t.line,
            "column": t.column,
            "content": t.content
        })

    # Get tokens after the current one
    end_idx = min(len(tokens), index + context_lines + 1)
    for i in range(index + 1, end_idx):
        t = tokens[i]
        context["after"].append({
            "type": t.type.name,
            "line": t.line,
            "column": t.column,
            "content": t.content
        })

    return context


def extract_token_statistics(content: str) -> dict[str, Any]:
    """Extract statistics about tokens in a document."""
    lexer = Lexer(content)
    tokens = lexer.tokenize()

    # Count by type
    type_counts = {}
    line_counts = {}
    longest_token = {"type": "", "length": 0, "content": ""}

    for token in tokens:
        # Update type counts
        token_type = token.type.name
        type_counts[token_type] = type_counts.get(token_type, 0) + 1

        # Update line counts
        line_counts[token.line] = line_counts.get(token.line, 0) + 1

        # Track longest token
        if len(token.content) > longest_token["length"]:
            longest_token = {
                "type": token_type,
                "length": len(token.content),
                "content": token.content if len(token.content) < 100 else token.content[:97] + "..."
            }

    return {
        "total_tokens": len(tokens),
        "unique_token_types": len(type_counts),
        "token_type_counts": type_counts,
        "tokens_per_line": {
            "max": max(line_counts.values()) if line_counts else 0,
            "min": min(line_counts.values()) if line_counts else 0,
            "avg": sum(line_counts.values()) / len(line_counts) if line_counts else 0
        },
        "longest_token": longest_token
    }


def format_tokens_rich(tokens: list[dict[str, Any]]) -> Any:
    """Format tokens for rich output."""
    try:
        from rich.console import Console
        from rich.table import Table

        table = Table(title="Token Analysis")
        table.add_column("Type", style="green")
        table.add_column("Line", style="cyan")
        table.add_column("Column", style="cyan")
        table.add_column("Content", style="white")

        for token in tokens:
            table.add_row(
                token["type"],
                str(token["line"]),
                str(token["column"]),
                token["content"]
            )

        console = Console()
        console.print(table)
        return table
    except ImportError:
        return "Rich library not available. Install with: pip install rich"
