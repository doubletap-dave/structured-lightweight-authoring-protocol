"""Main CLI entry point for Nomenic."""

import sys
import argparse
import json
from pathlib import Path
from typing import List, Optional

# Try absolute imports first (recommended approach)
try:
    from nomenic import Lexer, Parser
except ImportError:
    # Fall back to relative imports if absolute imports fail
    try:
        from .. import Lexer, Parser
    except ImportError:
        print("ERROR: Failed to import Nomenic core components. Please make sure the package is properly installed.")
        sys.exit(1)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the Nomenic CLI.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    if args is None:
        args = sys.argv[1:]

    parser = create_parser()
    parsed_args = parser.parse_args(args)

    # If no subcommand is provided, show help
    if not hasattr(parsed_args, 'func'):
        parser.print_help()
        return 1

    # Execute the selected subcommand
    try:
        return parsed_args.func(parsed_args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Nomenic Document Language (NDL) processor"
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Command to execute")

    # Debug command
    debug_parser = subparsers.add_parser(
        "debug", help="Debug and inspect Nomenic documents"
    )
    _setup_debug_parser(debug_parser)

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate Nomenic documents against the specification"
    )
    _setup_validate_parser(validate_parser)

    # Render command
    render_parser = subparsers.add_parser(
        "render", help="Render Nomenic documents to other formats"
    )
    _setup_render_parser(render_parser)

    # Convert command
    convert_parser = subparsers.add_parser(
        "convert", help="Convert between document formats"
    )
    _setup_convert_parser(convert_parser)

    # Lint command
    lint_parser = subparsers.add_parser(
        "lint", help="Check Nomenic documents for style and best practices"
    )
    _setup_lint_parser(lint_parser)

    return parser


def _setup_debug_parser(parser: argparse.ArgumentParser) -> None:
    """Set up the debug subcommand parser."""
    parser.add_argument(
        "file",
        type=str,
        help="File to debug"
    )
    parser.add_argument(
        "--mode",
        choices=["tokens", "errors", "styles", "ast"],
        default="tokens",
        help="Debug mode (default: tokens)"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "rich"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--filter",
        type=str,
        help="Filter by token type, error category, or style type"
    )
    parser.set_defaults(func=handle_debug)


def _setup_validate_parser(parser: argparse.ArgumentParser) -> None:
    """Set up the validate subcommand parser."""
    parser.add_argument(
        "file",
        type=str,
        help="File to validate"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Apply strict validation rules"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.set_defaults(func=handle_validate)


def _setup_render_parser(parser: argparse.ArgumentParser) -> None:
    """Set up the render subcommand parser."""
    parser.add_argument(
        "file",
        type=str,
        help="File to render"
    )
    parser.add_argument(
        "--format",
        choices=["html", "md", "yaml", "json"],
        default="html",
        help="Output format (default: html)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--theme",
        type=str,
        help="Theme for HTML output"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Generate pretty (indented) JSON/YAML output (default: True)"
    )
    parser.add_argument(
        "--include-frontmatter",
        action="store_true",
        default=True,
        help="Include metadata as frontmatter in Markdown output (default: True)"
    )
    parser.set_defaults(func=handle_render)


def _setup_convert_parser(parser: argparse.ArgumentParser) -> None:
    """Set up the convert subcommand parser."""
    parser.add_argument(
        "file",
        type=str,
        help="File to convert"
    )
    parser.add_argument(
        "--from",
        dest="from_format",
        choices=["nmc", "md", "yaml", "json"],
        help="Source format (default: auto-detect from extension)"
    )
    parser.add_argument(
        "--to",
        dest="to_format",
        choices=["nmc", "md", "yaml", "json"],
        required=True,
        help="Target format"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file (default: stdout)"
    )
    parser.set_defaults(func=handle_convert)


def _setup_lint_parser(parser: argparse.ArgumentParser) -> None:
    """Set up the lint subcommand parser."""
    parser.add_argument(
        "file",
        type=str,
        help="File to lint"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix linting issues"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.set_defaults(func=handle_lint)


def handle_debug(args: argparse.Namespace) -> int:
    """Handle the debug command."""
    try:
        from nomenic.debug import debug

        # Read the file
        file_path = Path(args.file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Prepare debug parameters and map filters to the correct arguments
        dbg_kwargs = {"mode": args.mode, "output_format": args.format}
        if args.filter:
            if args.mode == "tokens":
                dbg_kwargs["token_type"] = args.filter
            elif args.mode == "errors":
                dbg_kwargs["error_category"] = args.filter
            elif args.mode == "styles":
                dbg_kwargs["style_type"] = args.filter
        result = debug(content, **dbg_kwargs)

        print(result)
        return 0
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_validate(args: argparse.Namespace) -> int:
    """Handle the validate command."""
    try:
        # Read the file
        file_path = Path(args.file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Tokenize and parse the content
        lexer = Lexer(content)
        tokens = list(lexer.tokenize())
        parser = Parser(tokens)
        document = parser.parse()

        # Validate the document
        validation_errors = []
        if args.strict:
            # Add strict validation rules
            # TODO: Implement strict validation
            pass

        # Output results
        if args.format == "json":
            result = {
                "valid": len(parser.errors) == 0 and len(validation_errors) == 0,
                "file": str(file_path),
                "errors": []
            }

            # Add parser errors
            for msg, token in parser.errors:
                error_info = {
                    "message": msg,
                    "type": "parser"
                }
                if token:  # Token might be None for document-level errors
                    error_info.update({
                        "line": token.line,
                        "column": token.column,
                        "token": token.content
                    })
                result["errors"].append(error_info)

            print(json.dumps(result, indent=2))
        else:
            # Text format
            if len(parser.errors) == 0 and len(validation_errors) == 0:
                print(f" Document is valid: {args.file}")
                return 0
            else:
                print(f" Document validation failed: {args.file}")

                if parser.errors:
                    print(f"\nParser errors ({len(parser.errors)}):")
                    for i, (msg, token) in enumerate(parser.errors):
                        print(
                            f"  {i+1}. Line {token.line}, Column {token.column}: {msg}")

                if validation_errors:
                    print(f"\nValidation errors ({len(validation_errors)}):")
                    for i, (msg, token) in enumerate(validation_errors):
                        if token:
                            print(
                                f"  {i+1}. Line {token.line}, Column {token.column}: {msg}")
                        else:
                            print(f"  {i+1}. {msg}")

                return 1

        return 0 if len(parser.errors) == 0 and len(validation_errors) == 0 else 1
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_render(args: argparse.Namespace) -> int:
    """Handle the render command."""
    try:
        # Read the file
        file_path = Path(args.file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Determine output format
        if args.format == "html":
            from nomenic.renderers.html import render_html
            output = render_html(
                content,
                theme=args.theme,
                include_styles=True,
                include_meta=True
            )
        elif args.format == "md":
            from nomenic.renderers.markdown import render_markdown
            output = render_markdown(
                content,
                include_frontmatter=args.include_frontmatter
            )
        elif args.format == "yaml":
            from nomenic.renderers.yaml import render_yaml
            output = render_yaml(
                content,
                include_content=True
            )
        elif args.format == "json":
            from nomenic.renderers.json import render_json
            output = render_json(
                content,
                pretty=args.pretty,
                include_content=True
            )
        else:
            print(
                f"Output format '{args.format}' not supported", file=sys.stderr)
            return 1

        # Determine output destination
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output, encoding='utf-8')
            print(f"Rendered output written to {output_path}")
        else:
            print(output)

        return 0
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_convert(args: argparse.Namespace) -> int:
    """Handle the convert command."""
    try:
        from nomenic.converters import MarkdownConverter, YAMLConverter, JSONConverter

        # Read the input file
        file_path = Path(args.file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Determine source format if not specified
        from_format = args.from_format
        if not from_format:
            # Try to detect from file extension
            ext = file_path.suffix.lower()
            if ext == '.md':
                from_format = 'md'
            elif ext == '.yaml' or ext == '.yml':
                from_format = 'yaml'
            elif ext == '.json':
                from_format = 'json'
            elif ext == '.nmc':
                from_format = 'nmc'
            else:
                # Try to detect from content
                if content.startswith('---\n') and '\n---\n' in content:
                    from_format = 'yaml'
                elif content.startswith('{'):
                    from_format = 'json'
                elif any(marker in content for marker in ['# ', '## ', '### ']):
                    from_format = 'md'
                else:
                    from_format = 'nmc'  # Default to Nomenic format

        # Create appropriate converter
        if args.to_format == 'md':
            converter = MarkdownConverter()
        elif args.to_format == 'yaml':
            converter = YAMLConverter()
        elif args.to_format == 'json':
            converter = JSONConverter()
        else:
            raise ValueError(f"Unsupported target format: {args.to_format}")

        # Perform conversion
        if from_format == 'nmc':
            # Convert from Nomenic to target format
            result = converter.from_nomenic(content)
        else:
            # Convert from source format to Nomenic
            result = converter.to_nomenic(content)

        # Write output
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
        else:
            print(result)

        return 0
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_lint(args: argparse.Namespace) -> int:
    """Handle the lint command."""
    # Placeholder for future implementation
    print("Lint command not yet implemented")
    return 1


if __name__ == "__main__":
    sys.exit(main())
