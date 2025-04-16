"""Parser error analysis and debugging utilities for Nomenic."""

from typing import Dict, List, Optional, Tuple, Union

from ..lexer import tokenize
from ..parser import Parser
from ..tokens import Token


def analyze_errors(
    content: str,
    categorize: bool = True,
    include_context: bool = True,
) -> Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]:
    """
    Analyze parser errors in a Nomenic document.

    Args:
        content: The document content to analyze
        categorize: Whether to categorize errors by type
        include_context: Whether to include context lines around errors

    Returns:
        Dictionary with error analysis information
    """
    # Tokenize and parse
    tokens = tokenize(content)
    parser = Parser(tokens)
    parser.parse()  # We don't need the result, just gathering errors

    # Format errors for output
    formatted_errors = []
    for i, (msg, token) in enumerate(parser.errors):
        error_info = {
            "id": i + 1,
            "message": msg,
            "line": token.line,
            "column": token.column,
            "token_type": token.type.name,
            "token_value": token.value,
        }

        if include_context:
            error_info["context"] = _get_error_context(content, token)

        formatted_errors.append(error_info)

    result = {
        "total_errors": len(parser.errors),
        "errors": formatted_errors,
    }

    # Categorize errors if requested
    if categorize and parser.errors:
        result["categories"] = _categorize_errors(parser.errors)

    return result


def check_expected_errors(
    content: str,
    expected_types: Optional[List[str]] = None,
) -> Dict[str, Union[bool, List[str]]]:
    """
    Check if expected error types are present in a document.

    Args:
        content: The document content to check
        expected_types: List of expected error types or keywords

    Returns:
        Dictionary with check results
    """
    # Use common error types if none specified
    if expected_types is None:
        expected_types = ["header", "list item", "multi-line", "code block"]

    # Tokenize and parse
    tokens = tokenize(content)
    parser = Parser(tokens)
    parser.parse()

    # Extract error messages
    error_messages = [msg.lower() for msg, _ in parser.errors]

    # Check for each expected error type
    results = {}
    for expected in expected_types:
        found = any(expected.lower() in msg for msg in error_messages)
        results[expected] = found

    # Add summary
    all_found = all(results.values())
    missing = [err_type for err_type, found in results.items() if not found]

    return {
        "all_found": all_found,
        "results": results,
        "missing": missing,
    }


def validate_sample(name: str = "error_test") -> Dict[str, any]:
    """
    Validate a predefined error sample to test parser error handling.

    Args:
        name: The name of the predefined sample to test

    Returns:
        Dictionary with validation results
    """
    # Predefined samples with expected errors
    samples = {
        "error_test": {
            "content": """
header: # Missing header text
list:
- # Missing list item text
text:
>>> # Missing closing <<<
code:
# No code content
            """,
            "expected_errors": ["header", "list item", "multi-line", "code block"],
        },
        "minimal": {
            "content": """
header:
list:
            """,
            "expected_errors": ["header", "list"],
        },
    }

    # Check if the requested sample exists
    if name not in samples:
        raise ValueError(
            f"Unknown sample: {name}. Available samples: {', '.join(samples.keys())}"
        )

    # Get the sample and expected errors
    sample = samples[name]

    # Run the validation
    result = check_expected_errors(sample["content"], sample["expected_errors"])

    # Add the sample details to the result
    result["sample"] = name
    result["content"] = sample["content"]

    return result


def _get_error_context(
    content: str, token: Token, context_lines: int = 2
) -> Dict[str, Union[List[str], int]]:
    """Get context lines around an error location."""
    lines = content.splitlines()
    line_idx = token.line - 1  # Convert to 0-indexed

    # Get context with N lines before and after
    start_idx = max(0, line_idx - context_lines)
    end_idx = min(len(lines), line_idx + context_lines + 1)
    context = lines[start_idx:end_idx]

    # Add line numbers
    numbered_context = []
    for i, line in enumerate(context):
        line_num = start_idx + i + 1  # Convert back to 1-indexed
        # Mark the error line
        if line_num == token.line:
            numbered_context.append(f"-> {line_num}: {line}")
        else:
            numbered_context.append(f"   {line_num}: {line}")

    return {
        "lines": numbered_context,
        "start_line": start_idx + 1,  # Convert back to 1-indexed
        "error_line": token.line,
    }


def _categorize_errors(errors: List[Tuple[str, Token]]) -> Dict[str, int]:
    """Categorize errors by type."""
    categories = {
        "header": 0,
        "list": 0,
        "text": 0,
        "code": 0,
        "multiline": 0,
        "syntax": 0,
        "other": 0,
    }

    for msg, _ in errors:
        msg_lower = msg.lower()
        if "header" in msg_lower:
            categories["header"] += 1
        elif "list" in msg_lower or "item" in msg_lower:
            categories["list"] += 1
        elif "text" in msg_lower:
            categories["text"] += 1
        elif "code" in msg_lower:
            categories["code"] += 1
        elif "multi-line" in msg_lower or ">>>" in msg_lower or "<<<" in msg_lower:
            categories["multiline"] += 1
        elif "syntax" in msg_lower or "unexpected" in msg_lower:
            categories["syntax"] += 1
        else:
            categories["other"] += 1

    # Remove empty categories
    return {k: v for k, v in categories.items() if v > 0}
