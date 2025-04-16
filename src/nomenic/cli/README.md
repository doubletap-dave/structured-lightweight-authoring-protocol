# Nomenic CLI

The Nomenic CLI provides command-line tools for working with Nomenic Document Language (NDL) files.

## Installation

The CLI is included with the Nomenic package:

```bash
pip install nomenic
```

For enhanced output formatting with some commands, install the optional dependencies:

```bash
pip install nomenic[cli]
```

### Development Installation

If you're developing Nomenic, you can install it in development mode:

```bash
# From the project root
pip install -e .
```

### Troubleshooting Installation

If you encounter issues with the CLI entry point not being found, you can run the CLI in several alternative ways:

```bash
# Run using the wrapper script (from project root)
python src/nomenic_cli.py --help

# Run as a module
python -m nomenic.cli.main --help

# Run using the installation helper
python -m nomenic.cli.install
```

If you're experiencing import issues, the CLI includes fallback mechanisms that should handle both absolute and relative imports. If problems persist, please check:

1. Ensure your Python environment is correctly set up
2. Make sure the package is properly installed
3. Verify that the entry point is in your PATH

## Commands

### Debug

Debug and inspect Nomenic documents:

```bash
nomenic debug file.nmc [--mode MODE] [--format FORMAT] [--filter FILTER]
```

Options:
- `--mode`: Debug mode (tokens, errors, styles, ast)
- `--format`: Output format (text, json, rich)
- `--filter`: Filter by token type, error category, or style type

Example:
```bash
# View tokens in the document
nomenic debug mydoc.nmc

# Debug with rich output format
nomenic debug mydoc.nmc --format rich

# Show only header tokens
nomenic debug mydoc.nmc --mode tokens --filter HEADER
```

### Validate

Validate Nomenic documents against the specification:

```bash
nomenic validate file.nmc [--strict] [--format FORMAT]
```

Options:
- `--strict`: Apply strict validation rules
- `--format`: Output format (text, json)

Example:
```bash
# Validate a document 
nomenic validate mydoc.nmc

# Validate with strict mode and JSON output
nomenic validate mydoc.nmc --strict --format json
```

### Render

Render Nomenic documents to other formats:

```bash
nomenic render file.nmc [--format FORMAT] [--output FILE] [--theme THEME]
```

Options:
- `--format`: Output format (html, md, yaml, json)
- `--output`: Output file (default: stdout)
- `--theme`: Theme for HTML output (default, light, dark)

Example:
```bash
# Render document to HTML and send to stdout
nomenic render mydoc.nmc

# Render to HTML with dark theme and save to file
nomenic render mydoc.nmc --format html --theme dark --output mydoc.html
```

### Convert

Convert between document formats:

```bash
nomenic convert file.nmc --to FORMAT [--from FORMAT] [--output FILE]
```

Options:
- `--from`: Source format (nmc, md, yaml, json)
- `--to`: Target format (nmc, md, yaml, json)
- `--output`: Output file (default: stdout)

Example:
```bash
# Convert Nomenic to Markdown
nomenic convert mydoc.nmc --to md --output mydoc.md

# Convert Markdown to Nomenic
nomenic convert README.md --from md --to nmc
```

### Lint

Check Nomenic documents for style and best practices:

```bash
nomenic lint file.nmc [--fix] [--format FORMAT]
```

Options:
- `--fix`: Automatically fix linting issues
- `--format`: Output format (text, json)

Example:
```bash
# Check document for style issues
nomenic lint mydoc.nmc

# Fix style issues automatically
nomenic lint mydoc.nmc --fix
```

## Exit Codes

- `0`: Success
- `1`: Error (invalid arguments, file not found, validation failed, etc.) 