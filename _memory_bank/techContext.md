---
fileWeight: high
linkedPatterns:
  - python-testing
  - validation-pipelines
confidenceRating: 0.95
triggeredByTick: tick-X1963B583F15
---

# Technical Context

## Project Overview
Nomenic Core is a parser and renderer for Nomenic Document Language (NDL), a structured markup language designed for technical documentation with semantic meaning preservation. The project aims to provide a modern alternative to Markdown and reStructuredText with better support for semantic blocks, metadata, and transformations.

## Architecture
- **Language Processing Pipeline**: Lexer -> Parser -> AST -> Renderer
- **Core Components**:
  - `lexer.py`: Tokenizes NDL input text
  - `tokens.py`: Defines token types and token class
  - `parser.py`: Parses token stream into AST
  - `ast.py`: Abstract Syntax Tree node definitions
  - `validator.py`: Validates NDL documents against schema
  - `renderer.py`: Transforms AST into output formats

## Implementation Details
- **Language**: Python 3.9+
- **Code Organization**: Modular design with clear separation of concerns
- **Error Handling**: Comprehensive error reporting with line/column information
- **Testing**: PyTest with property-based testing via Hypothesis

## Development Status
- **Phase 1**: ✅ Core Lexer Implementation - Complete
- **Phase 2**: ✅ Parser & AST Implementation - Complete
- **Phase 3**: ✅ Testing & Validation - Complete
  - Achieved 90% overall code coverage
  - Implemented comprehensive test suite with:
    - Unit tests for all components
    - Integration tests for end-to-end workflows
    - Property-based tests for edge cases
    - Performance benchmarks
- **Phase 4**: 🔄 Documentation & Delivery - In Progress
  - User documentation
  - API documentation
  - Example templates
  - Release preparation

## Technical Debt & Constraints
- Performance optimizations for large documents needed
- Schema validation system to be expanded
- Custom renderers for additional output formats

## Dependencies
- Core: No external runtime dependencies (standard library only)
- Development:
  - pytest (testing)
  - hypothesis (property-based testing)
  - ruff (linting)
  - black (formatting)
  - pre-commit (git hooks)

## Build & Test Infrastructure
- Continuous Integration: GitHub Actions
- Test Coverage Reporting: pytest-cov
- Static Analysis: ruff, mypy

## Notes
Phase 3 testing and validation is now complete with comprehensive test coverage across all components. The codebase has reached a stable state and is ready for documentation and final release preparation.

header: Tech Stack
  text: Primary implementation is in Python 3.10+ with the following core components:
  list:
    - Lexer: Custom implementation using regex for token recognition
    - Parser: Recursive descent parser with custom AST representation
    - Renderer: Pluggable rendering system (HTML, Markdown, YAML) with extensible architecture
    - CLI: Subcommand-based interface built on Click for document processing
  text: Testing framework utilizes pytest with property-based testing via Hypothesis for fuzz testing and edge case detection.

header: Development Phases
  list:
    - Phase 1: Lexer Development (COMPLETE)
      - Tokenization of NDL syntax elements
      - Comprehensive error handling for malformed input
      - 100% unit test coverage for lexer module
    - Phase 2: Parser & AST (COMPLETE)
      - Abstract Syntax Tree definition
      - Recursive descent parser implementation
      - Visitor pattern for AST traversal
      - Validation rules per NDL specification
      - Error handling with meaningful diagnostics
    - Phase 3: Testing & Validation (COMPLETE)
      - Property-based fuzz testing
      - Edge case testing suite
      - Performance benchmarks
      - Memory usage optimization
      - 90% overall code coverage (lexer: 86%, parser: 90%)
    - Phase 4: CLI Tooling & Basic Conversion (UPCOMING)
      - Command-line interface implementation
      - HTML rendering pipeline
      - Basic format converters (Markdown, YAML)
    - Phase 5: Advanced Features & Optimization
      - Schema validation
      - Custom extension API
      - Performance optimization
      - Documentation generation

header: Code Structure
  text: The project follows a modular architecture with clear separation of concerns:
  code:
    src/
      nomenic/
        __init__.py          # Package initialization
        lexer.py             # Tokenization logic
        tokens.py            # Token definitions
        parser.py            # Recursive descent parser
        ast.py               # Abstract Syntax Tree definitions
        validators.py        # Validation rules
        renderers/
          __init__.py        # Renderer registry
          html.py            # HTML output renderer
          markdown.py        # Markdown conversion
          yaml.py            # YAML serialization
        cli/
          __init__.py        # CLI entry points
          convert.py         # Conversion subcommands
          validate.py        # Validation utilities
          render.py          # Rendering commands
      tests/
        unit/                # Unit tests for each module
        fuzz/                # Property-based fuzz tests
        benchmarks/          # Performance benchmarks

header: Testing Strategy
  text: The project employs a comprehensive testing approach consisting of:
  list:
    - Unit tests for core functionality
    - Integration tests for module interactions
    - Property-based fuzz testing for robust validation
    - Edge case tests for boundary conditions
    - Performance benchmarks to detect regressions
    - Memory usage monitoring
  text: All tests are automated and run in CI pipeline. Current test coverage is 90% across the codebase with 53 unit and fuzz tests passing.

header: Technical Debt & Challenges
  list:
    - Optimization of parser for large documents
    - Handling of complex nested structures
    - Extension mechanism for custom syntax elements
    - Backward compatibility with legacy formats
    - Memory usage for very large documents
  text: These challenges are being addressed in the testing and optimization phases.

header: Core Syntax Elements
  text: Based on a line-oriented structure with indentation (2 spaces, no tabs) for nesting.
  list:
    - `meta:` Document-level metadata (key=value pairs).
    - `header:` Section headings.
    - `text:` Paragraphs/body content. Supports multi-line blocks (`>>>`/`<<<`).
    - `list:` Unordered list items (prefixed with `-`).
    - `code:` Preformatted code blocks.
    - `table:` Defines tabular data (`row:` sub-elements).
    - Inline annotations: `(...)` or `[...]` within a line.
    - Custom directives: `x-*` prefix signals user-defined blocks.
    - Extended block types: Inline key/values `{...}`, callouts (`note:`, `warn:`).

header: Parsing & Implementation
  list:
    - Sequential, line-by-line processing.
    - Indentation strictly determines hierarchy.
    - Parsers should be fault-tolerant, logging errors and attempting recovery.
    - Flexible output targets (HTML, Markdown, JSON, tokens).
    - Short token aliases (`m:`, `h:`, `t:`, etc.) may be supported.
    - Visitor pattern for AST traversal and transformations.
    - AST normalization and optimization for consistent output.
    - Document validation for specification compliance.

header: Error Handling Capabilities
  list:
    - Two-level error handling: record (continue) or report (raise exception)
    - Common error detection: missing content in headers, lists, code blocks
    - Error position tracking with line and column numbers
    - Recovery mechanism using synchronization to statement boundaries
    - Diagnostic information with token context
    - Special handling for unterminated blocks and unexpected delimiters

header: File Extension
  text: `.nmc` 