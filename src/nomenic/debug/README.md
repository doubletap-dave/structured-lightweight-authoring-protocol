# Nomenic Debug Module

The Nomenic Debug module provides comprehensive debugging and inspection capabilities for Nomenic documents. It offers various tools for examining tokens, analyzing parser errors, inspecting styles, and visualizing document structure.

## Features

- **Token Inspection**: Analyze and filter tokens in Nomenic documents
- **Error Analysis**: Examine parser errors with context and categorization
- **Style Token Inspection**: Examine styles and inline formatting in documents
- **File Utilities**: Handle file operations with proper error handling
- **Multiple Output Formats**: Text, JSON, and Rich (with the rich library)

## Usage

### Basic Usage

```python
from nomenic.debug import debug

# Analyze tokens
tokens = debug(content, mode="tokens")

# Analyze errors
errors = debug(content, mode="errors")

# Inspect styles
styles = debug(content, mode="styles")

# Visualize AST structure
ast = debug(content, mode="ast")
```

### Filtering and Options

```python
# Filter tokens by type
header_tokens = debug(content, mode="tokens", token_type="HEADER")

# Get detailed token information with context
detailed_tokens = debug(content, mode="tokens", detailed=True)

# Get JSON output
json_result = debug(content, mode="tokens", output_format="json")

# Filter styles by type
bold_styles = debug(content, mode="styles", style_type="bold")
```

## Module Components

### `core.py`

Provides the central `debug()` function that serves as the main entry point for all debugging operations.

### `token_utils.py`

Contains utilities for token analysis:
- `analyze_tokens()`: Inspect tokens with filtering and detail options
- `check_token_patterns()`: Test regex patterns against content
- `visualize_ast()`: Basic visualization of the AST structure

### `parser_utils.py`

Provides error analysis capabilities:
- `analyze_errors()`: Analyze parser errors with context
- `check_expected_errors()`: Check for expected error types
- `validate_sample()`: Test predefined error samples

### `style_utils.py`

Utilities for style token inspection:
- `analyze_styles()`: Analyze style tokens with filtering
- `find_style_in_lines()`: Find lines with style markers
- `_check_style_patterns()`: Test style regex patterns

### `file_utils.py`

File operation utilities:
- `read_file()`: Safely read file content
- `get_line_context()`: Get context around a specific line
- `find_test_fixtures()`: Find test fixture files
- `load_sample()`: Load sample content
- `list_fixtures()`: List available fixture files

## Output Formats

The debug module supports multiple output formats:

- **Text** (default): Returns structured data objects
- **JSON**: Returns JSON-compatible dictionaries
- **Rich**: Formatted output using the rich library (requires installing the rich package) 