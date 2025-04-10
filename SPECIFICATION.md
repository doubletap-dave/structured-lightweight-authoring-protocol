# Compact Structured Markup (CSM) Specification

**Version:** 1.1  
**Date:** 2025-04-10

---

## Table of Contents

1. [Introduction](#introduction)
2. [Design Goals](#design-goals)
3. [General Syntax](#general-syntax)
   1. [Line-Oriented Structure](#line-oriented-structure)
   2. [Indentation and Nesting](#indentation-and-nesting)
4. [Reserved Tokens](#reserved-tokens)
   1. [meta:](#meta)
   2. [header:](#header)
   3. [text:](#text)
   4. [list:](#list)
   5. [code:](#code)
5. [Additional Features](#additional-features)
   1. [Inline Annotations](#inline-annotations)
   2. [Custom Directives](#custom-directives)
   3. [Extended Block Types](#extended-block-types)
6. [Parsing and Rendering Guidelines](#parsing-and-rendering-guidelines)
7. [Implementation Guidelines](#implementation-guidelines)
8. [Example Document](#example-document)
9. [Versioning and Extensibility](#versioning-and-extensibility)
10. [License and Contribution](#license-and-contribution)

---

## 1. Introduction

Compact Structured Markup (CSM) is a minimalistic markup language designed for clear, concise documentation. It is optimized to reduce unnecessary tokens while preserving structure and human readability. CSM is intended for projects where efficient AI processing is as important as ease-of-use by human authors.

---

## 2. Design Goals

- **Minimal Syntax Overhead:**  
  Use the fewest possible symbols and keywords to define document structure.

- **Human Readability:**  
  Maintain a natural, accessible flow of text without excessive formatting clutter.

- **Efficient Token Usage:**  
  Reduce extraneous tokens to minimize processing cost for AI agents, enabling faster parsing and lower overhead.

- **Clear Structure and Hierarchy:**  
  Define a consistent, line-based syntax with well-defined nesting through indentation.

- **Extensibility:**  
  Allow for future enhancements through reserved namespaces and custom directives while preserving backward compatibility.

---

## 3. General Syntax

### 3.1 Line-Oriented Structure

- **Single Logical Unit per Line:**  
  Each line in a CSM document represents a complete logical unit (e.g., metadata, header, text).
  
- **Token Placement:**  
  Reserved tokens, when used, must appear at the beginning of a line (after any indentation that indicates nesting).

### 3.2 Indentation and Nesting

- **Indentation:**  
  Use spaces (not tabs) for indentation. A uniform indentation (suggested: 2 spaces) defines child elements nested within a parent element.
  
- **Nesting Convention:**  
  A line indented relative to its parent is considered part of that parent’s block (for example, text or list items inside a `header:` section).

---

## 4. Reserved Tokens

The following tokens are reserved and provide the structural framework for CSM documents. They are designed to be minimal yet powerful.

### meta:

- **Purpose:**  
  Provide document-level metadata.
  
- **Syntax:**  
  ```
  meta: key1=value1, key2=value2, ...
  ```
  - Use commas to separate key-value pairs.
  - Place the `meta:` line at the beginning of the document.

### header:

- **Purpose:**  
  Define a new document section.
  
- **Syntax:**  
  ```
  header: Section Title
  ```
  - Any content following the token on the same line is considered the header title.
  - Child elements under this header must be indented consistently.

### text:

- **Purpose:**  
  Introduce a paragraph or continuous block of narrative text.
  
- **Syntax:**  
  ```
  text: This is a paragraph of text that provides description or narrative.
  ```
  - Multi-line text blocks must retain consistent indentation throughout.

### list:

- **Purpose:**  
  Define a list of items.
  
- **Syntax:**  
  ```
  list:
    - Item 1
    - Item 2
    - Item 3
  ```
  - A hyphen (`-`) marks individual list items, placed on lines indented under the `list:` token.

### code:

- **Purpose:**  
  Introduce a code block or preformatted text.
  
- **Syntax:**  
  ```
  code:
    def example():
        return "code block"
  ```
  - All following lines that are indented form part of the code block until the indentation is reduced or another reserved token is encountered.

---

## 5. Additional Features

To further enhance the language while keeping token usage low, the following optional features are defined.

### 5.1 Inline Annotations

- **Purpose:**  
  Allow brief, inline notes or annotations without breaking the flow of text.
  
- **Syntax:**  
  Append annotations in parentheses directly after the content.  
  *Example:*  
  ```
  text: This is a paragraph (note: additional context).
  ```
- **Guideline:**  
  Use inline annotations sparingly to maintain brevity.

### 5.2 Custom Directives

- **Purpose:**  
  Extend the core language for specialized scenarios (e.g., tables, images, citations).
  
- **Syntax:**  
  Custom directives start with a reserved namespace, using `x-` as a prefix.  
  *Example:*  
  ```
  x-table:
    - row: Cell1, Cell2, Cell3
    - row: Data1, Data2, Data3
  ```
- **Guideline:**  
  Parsers should ignore unknown custom directives gracefully, ensuring backward compatibility.

### 5.3 Extended Block Types

- **Inline Key/Value Pairs:**  
  For compact in-text structured data, allow inline key/value notation using braces.  
  *Example:*  
  ```
  text: User data {id=123, role=admin}
  ```
- **Callouts/Notes:**  
  Special callouts can be defined with a simple token such as `note:` or `warn:` for low-overhead emphasis.  
  *Example:*  
  ```
  note: This is an important note that should be highlighted.
  ```
  (These tokens follow the same placement and indentation rules as standard tokens.)

---

## 6. Parsing and Rendering Guidelines

### 6.1 Parsing

- **Line-by-Line Processing:**  
  A CSM parser processes the document line by line, determining block types based on reserved tokens and indentation levels.
  
- **State Management:**  
  The parser should maintain state for nested blocks, switching contexts when encountering changes in indentation.
  
- **Error Handling:**  
  Parsers must provide clear error messages if syntax rules (such as inconsistent indentation or unexpected tokens) are violated.

### 6.2 Rendering

- **Human-Friendly Output:**  
  A renderer converts CSM documents into human-readable formats (e.g., formatted plain text, HTML, Markdown) while preserving the original logical structure.
  
- **Token Minimization:**  
  The rendering process should not add extra tokens; it should faithfully reflect the minimal syntax defined in the document.

---

## 7. Implementation Guidelines

### 7.1 Development

- **Language Support:**  
  Develop parser libraries in common languages (such as Python, JavaScript, etc.) to allow widespread usage.
  
- **Tooling:**  
  Provide command-line tools, documentation, and examples to facilitate adoption and testing of CSM.

### 7.2 Testing

- **Unit Tests:**  
  Create comprehensive test cases covering all token types, nesting scenarios, error conditions, and custom directives.
  
- **Continuous Integration:**  
  Use CI/CD pipelines to ensure ongoing compatibility and early detection of issues with new format extensions.

---

## 8. Example Document

Below is an illustrative CSM document combining core and extended features:

```
meta: title=Project Update, date=2025-04-10, author=Alex
header: Introduction
  text: This document provides a brief update on the project.
  note: Ensure all team members review the updated scope.
  list:
    - Define scope
    - Assign tasks
    - Set milestones
header: Technical Details
  text: The project is running smoothly; see the code sample below.
  code:
    def greet():
        return "Hello, World!"
  text: Refer to external libraries {lib=example-lib, version=1.2.3}.
x-table:
  - row: Column1, Column2, Column3
  - row: Data1, Data2, Data3
```

---

## 9. Versioning and Extensibility

- **Version Declaration:**  
  Each CSM document should declare its version in the metadata if backward-incompatible changes occur.
  
- **Future Tokens:**  
  New reserved tokens should be defined within a reserved namespace (e.g., `x-`) to avoid conflicts with core functionality.
  
- **Graceful Degradation:**  
  Parsers must ignore or provide warnings for unknown tokens to ensure documents remain processable across different versions.

---

## 10. License and Contribution

- **License:**  
  The CSM format is released under the MIT License. See the LICENSE file in the repository.
  
- **Contribution Guidelines:**  
  Contributions, improvements, and suggestions are welcome. Please follow the issue and pull request guidelines to propose changes.

---

## Conclusion

The **Compact Structured Markup (CSM)** format is designed to provide a clear, minimal, and extendable approach to structured documentation—optimizing token usage while remaining friendly to human readers. This specification is intended as the baseline for further development and refinement. Contributions and community feedback are encouraged to evolve the standard to meet future needs.