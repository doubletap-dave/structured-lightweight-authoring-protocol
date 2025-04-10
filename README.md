# Compact Structured Markup (CSM)

**Version:** 1.1  
**Date:** 2025-04-10

## Overview

Compact Structured Markup (CSM) is a minimal markup language designed for clear and structured documentation. It is optimized for both human readability and efficient processing by AI agents, with a focus on reducing token usage without compromising structure.

## Key Features

- **Minimal Syntax:**  
  A small set of reserved tokens and consistent indentation are used to define the document structure without verbose markup.

- **Human Readability:**  
  The format is designed to be easy to read and write, preserving a natural language flow while still conveying structure.

- **Efficient Token Usage:**  
  The lightweight syntax minimizes extraneous characters, making CSM particularly useful for AI integrations where token costs matter.

- **Extensibility:**  
  Additional functionality (custom directives, inline annotations, callouts, etc.) can be added via reserved namespaces (`x-`), ensuring backward compatibility with the core spec.

## Specification

The full specification for CSM is provided in [SPECIFICATION.md](SPECIFICATION.md). It covers:

- **Design Goals & General Syntax:**  
  An explanation of the token-minimal approach, with line-oriented structure and indentation-based nesting.

- **Reserved Tokens:**  
  Detailed definitions for core tokens such as `meta:`, `header:`, `text:`, `list:`, and `code:`.

- **Additional Features:**  
  Options for inline annotations, custom directives, and extended block types while keeping the markup compact.

- **Parsing & Rendering Guidelines:**  
  Best practices for building parsers and renderers that convert CSM into human-friendly and machine-friendly formats.

- **Implementation Recommendations:**  
  Guidance on developing parser libraries, tooling, and testing strategies.

## Getting Started

### Installation

Clone this repository to start using CSM:

```bash
git clone https://github.com/your-username/compact-structured-markup.git
cd compact-structured-markup
```

### Writing CSM Documents

Create a file with a `.csm` extension (e.g., `example.csm`) and follow the documented structure. Here’s a quick example:

```csm
meta: title=Project Update, date=2025-04-10, author=Alex
header: Introduction
  text: This document provides a brief update on the project.
  list:
    - Define scope
    - Assign tasks
    - Set milestones
header: Technical Details
  text: The project is running smoothly.
  code:
    def greet():
        return "Hello, World!"
```

### Tools and Converters

- **Parser Libraries:**  
  Sample implementations in Python and JavaScript are available in the `/parsers` directory to help you parse and render CSM documents.

- **Conversion Utilities:**  
  Tools to convert CSM into formats like Markdown or HTML are under development and will be available soon.

## Contributing

Contributions are welcome! If you have improvements, bug fixes, or additional features to propose:
- Open an issue to discuss major changes.
- Submit pull requests that include clear explanations of your modifications.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

CSM builds on ideas from existing lightweight markup languages such as reStructuredText, AsciiDoc, and YAML. Thank you to those communities for their inspiration and contributions.

---

Happy documenting with CSM!