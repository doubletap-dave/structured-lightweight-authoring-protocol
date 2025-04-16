"""Core debugging functionality for Nomenic.

This module provides a unified interface for debugging Nomenic documents.
It supports various modes for inspecting tokens, analyzing errors, 
examining styles, and visualizing document structure.
"""

import json
from importlib import util as importlib_util
from typing import Any, Optional, Union


def debug(
    content: str,
    mode: str = "tokens",
    output_format: str = "text",
    token_type: Optional[str] = None,
    error_category: Optional[str] = None,
    style_type: Optional[str] = None,
) -> Union[str, list[Any], dict[str, Any]]:
    """
    Unified debug interface for Nomenic documents.

    Args:
        content: The Nomenic document content to debug
        mode: Debug mode (tokens, errors, styles, ast)
        output_format: Output format (text, json, rich)
        token_type: Optional token type filter
        error_category: Optional error category filter
        style_type: Optional style token filter

    Returns:
        Debug information in the requested format
    """
    if mode == "tokens":
        from .token_utils import analyze_tokens
        result = analyze_tokens(content, token_type)
    elif mode == "errors":
        from .parser_utils import analyze_errors
        result = analyze_errors(content, error_category)
    elif mode == "styles":
        from .style_utils import analyze_styles
        result = analyze_styles(content, style_type)
    elif mode == "ast":
        from .parser_utils import analyze_ast
        result = analyze_ast(content)
    else:
        raise ValueError(f"Unknown debug mode: {mode}")

    if output_format == "text":
        return _format_as_text(result, mode)
    elif output_format == "json":
        return _format_as_json(result)
    elif output_format == "rich":
        return _format_as_rich(result, mode)
    else:
        raise ValueError(f"Unknown output format: {output_format}")


def _format_as_text(result: Union[list[Any], dict[str, Any]], mode: str) -> str:
    """Format debug results as plain text."""
    if isinstance(result, list):
        return "\n".join(str(item) for item in result)
    elif isinstance(result, dict):
        return "\n".join(f"{k}: {v}" for k, v in result.items())
    return str(result)


def _format_as_json(result: Any) -> str:
    """Format debug results as JSON."""
    return json.dumps(result, indent=2, default=str)


def _format_as_rich(result: Any, mode: str) -> Any:
    """Format debug results using rich library if available."""
    try:
        has_rich = importlib_util.find_spec("rich") is not None
        if not has_rich:
            raise ImportError(
                "Rich library not installed. Run 'pip install rich' to use rich output formatting.")

        if mode == "tokens":
            from .token_utils import format_tokens_rich
            return format_tokens_rich(result)
        elif mode == "errors":
            from .parser_utils import format_errors_rich
            return format_errors_rich(result)
        elif mode == "styles":
            from .style_utils import format_styles_rich
            return format_styles_rich(result)
        elif mode == "ast":
            from .parser_utils import format_ast_rich
            return format_ast_rich(result)
        return result
    except ImportError as err:
        raise ImportError(
            "Rich library not installed. Run 'pip install rich' to use rich output formatting.") from err


def format_as_json(data: dict[str, Any]) -> str:
    """Format data as JSON string."""
    return json.dumps(data, indent=2, default=str)
