# Compact Structured Markup (CSM)

**Version:** 1.0  
**Date:** 2025-04-10

## Overview

Compact Structured Markup (CSM) is a lightweight markup language designed to strike a balance between human readability and machine-efficient token usage. Inspired by the need for minimal overhead in AI communications and documentation, CSM provides a clear and structured syntax without the verbosity of traditional markup formats.

## Key Features

- **Minimal Syntax:**  
  CSM uses a handful of reserved tokens and indentation to clearly define structure, reducing token count for efficient parsing.
  
- **Human-Readable:**  
  The format maintains a natural flow and clarity that makes it easy for users to write and understand, even as it incorporates structured data.

- **Structured Data Support:**  
  Easily manage metadata, hierarchical sections, plain text, lists, and code blocks with a few simple rules.

- **Ease of Parsing:**  
  Designed with AI and parsing in mind, CSM allows for straightforward conversion into other formats like Markdown or HTML.

## Specification Summary

CSM documents are organized line-by-line with reserved tokens indicating their role. Indentation is used to nest elements, and reserved tokens such as `meta:`, `header:`, `text:`, `list:`, and `code:` define the type of content.

Here’s a quick example:

```csm
meta: title=Project Update, date=2025-04-10, author=Alex
header: Introduction
  text: This document provides a brief update on the project.
  list:
    - Define scope
    - Assign tasks
    - Set milestones
header: Details
  text: The project has been progressing steadily.
  code:
    def greet():
        return "Hello, World!"
```

## Getting Started

### Installation

You can begin experimenting with CSM immediately. Clone this repository:

```bash
git clone https://github.com/your-username/compact-structured-markup.git
cd compact-structured-markup
```

### Usage

1. **Writing CSM Documents:**  
   Create a new text file (e.g., `example.csm`) using the structure illustrated above.

2. **Parsing Tools:**  
   Use the provided parsing libraries (or develop your own) to convert CSM documents into your desired output formats. (See the `/parsers` directory for sample implementations.)

3. **Contributing Converters:**  
   If you have converters or renderers (e.g., to Markdown, HTML, JSON) that work with CSM, feel free to open a pull request.

## Contributing

I welcome contributions from developers and enthusiasts interested in minimal markup languages. Please follow these guidelines when contributing:

- **Issues:**  
  Open an issue first to discuss any significant changes.

- **Pull Requests:**  
  Keep your pull requests focused and include clear descriptions of your changes.

- **Coding Style:**  
  Aim for clarity, efficiency, and consistency with the principles of CSM.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

I appreciate the inspiration from existing lightweight markup languages such as reStructuredText, AsciiDoc, and YAML. Their balance of readability and structure helped shape the vision for CSM.

---

Happy documenting!

---

Feel free to modify any part of this content to better fit your vision for CSM. Let me know if you need any further changes or additional sections!
