# Nomenic Core

<p align="center"><strong>Structure Everything: A Modern Document Format for Humans and Machines</strong></p>

<p align="center">
  <em>Version 1.0.0 — 2025-04-14</em>
</p>

---

## 🚀 Overview

**Nomenic Core** is a structured document format designed for both human readability and machine parsing, bridging the gap between Markdown's simplicity and YAML's structure. It offers a clean, hierarchical syntax that preserves semantic meaning while remaining easy to author.

Born from the need for documentation that serves both human readers and AI/ML systems, Nomenic provides explicit structure, consistent patterns, and robust error handling.

## ✨ Key Features

- **Explicit Structure** - Clear token markers eliminate ambiguity
- **Human Readable** - Intuitive syntax designed for both writing and reading
- **Token Efficient** - Optimized for LLMs and parsers with minimal overhead
- **Error Tolerant** - Comprehensive error detection, reporting, and recovery
- **Extensible** - User-defined directives and metadata support
- **Hierarchical** - Indentation-based nesting for logical organization

## 🔧 Core Components

```
header: Project Status
  text: Phase 3 (Testing & Validation) complete!
  list:
    - Robust parser implementation ✅
    - Comprehensive error handling ✅
    - Test suite with 90% coverage ✅
    - Performance benchmarks ✅
  text: Now moving to Phase 4: CLI tools and conversion utilities.
```

## 📋 Project Status

Nomenic Core has completed 3 of 6 planned phases:

- **✅ Phase 1: Core Specification** - Format design, token schema, grammar rules
- **✅ Phase 2: Parser Implementation** - Lexer, parser, AST, validation, error handling
- **✅ Phase 3: Testing & Validation** - Unit tests, fuzz testing, benchmarks, edge cases
- **🔄 Phase 4: CLI Tooling & Conversion** - Currently in progress
- **⏱️ Phase 5: Documentation & Examples** - Upcoming
- **⏱️ Phase 6: Refinement & Extensibility** - Upcoming

## 📚 Documentation

- **[Specification](spec/NOMENIC-CORE.md)** - Full syntax and behavior documentation
- **[Grammar Rules](spec/GRAMMAR.md)** - Formal EBNF grammar definition
- **[Token Schema](spec/TOKEN-SCHEMA.nmc)** - Token definitions and structure

## 🛠️ Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/nomenic/nomenic-core.git
cd nomenic-core

# Set up development environment
python -m pip install -e .
python -m pip install -r requirements-dev.txt
```

### Usage (Python Library)

```python
from nomenic import lexer, parser

# Parse a Nomenic document
with open("example.nmc", "r") as f:
    content = f.read()
    
tokens = lexer.tokenize(content)
ast = parser.parse(tokens)

# Work with the AST
for node in ast.children:
    print(f"Node type: {node.type}")
```

### CLI Usage

Nomenic Core includes a command-line interface (CLI) for working with Nomenic documents.

```bash
# Install the package with CLI support
python -m pip install -e .

# Show CLI help
nomenic --help

# Debug and inspect a document
nomenic debug path/to/document.nmc

# Validate a document
nomenic validate path/to/document.nmc

# Render a document to HTML
nomenic render path/to/document.nmc --format html

# Render to HTML and save to file
nomenic render path/to/document.nmc --format html --output output.html
```

If the CLI is not in your PATH, you can run it directly using:

```bash
# Run from project root
python src/nomenic_cli.py --help

# Or as a module
python -m nomenic.cli.main --help
```

### Requirements

- Python 3.9+
- No external runtime dependencies

## 🧪 Development 

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src

# Format code
black src tests

# Lint
ruff src tests
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the BSD 3-Clause - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <em>Nomenic: Because we deserve better than markdown spaghetti.</em>
</p> 