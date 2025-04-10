# Structured Lightweight Authoring Protocol (SLAP) Specification

**Version:** 1.2  
**Date:** 2025-04-10  
**Tagline:** SLAP: Finally, a spec that won’t make your parser cry.

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
5. [Additional Features and Enhancements](#additional-features-and-enhancements)
   1. [Inline Annotations](#inline-annotations)
   2. [Multi-Line Text Blocks](#multi-line-text-blocks)
   3. [Custom Directives](#custom-directives)
   4. [Extended Block Types](#extended-block-types)
6. [Error Handling & Recovery](#error-handling--recovery)
7. [Parsing and Rendering Guidelines](#parsing-and-rendering-guidelines)
8. [Implementation Guidelines](#implementation-guidelines)
9. [Versioning and Extensibility](#versioning-and-extensibility)
10. [License and Contribution](#license-and-contribution)

---

## 1. Introduction

Structured Lightweight Authoring Protocol (SLAP) is a minimalistic markup language designed for clear, structured documentation. SLAP is optimized both for human readability and for efficient processing by AI agents, with a strong focus on reducing unnecessary token usage without sacrificing essential structure.

---

## 2. Design Goals

- **Minimal Syntax Overhead:**  
  SLAP employs only the necessary tokens to define structure and data, reducing verbosity and computational token cost.

- **Human Readability:**  
  The protocol is crafted to maintain an accessible, natural language flow that remains easy to author and understand.

- **Efficient Token Usage:**  
  By reducing extraneous tokens, SLAP minimizes the payload for both storage and AI processing.

- **Clear Structure and Hierarchy:**  
  A line-oriented approach coupled with uniform indentation ensures that the document's logical structure is immediately clear.

- **Extensibility:**  
  Future enhancements are facilitated via reserved namespaces and custom directives while keeping backward compatibility intact.

---

## 3. General Syntax

### 3.1 Line-Oriented Structure

- **One Logical Unit per Line:**  
  Each line represents a complete unit—whether metadata, headers, or text—typically beginning with a reserved token.

- **Reserved Token Positioning:**  
  Reserved tokens must start the line, right after any indentation used to indicate nesting.

### 3.2 Indentation and Nesting

- **Indentation:**  
  Use spaces only (recommended: 2 spaces per level) for indentation. This defines nested blocks clearly.
  
- **Nesting:**  
  Blocks indented relative to a parent token are considered part of that block (e.g., a list under a header).

---

## 4. Reserved Tokens

These tokens provide the fundamental structure for SLAP documents:

### meta:

- **Purpose:**  
  Store document-level metadata.
  
- **Syntax:**  
  ```
  meta: key1=value1, key2=value2, ...
  ```
  - Commas separate key-value pairs.
  - The meta token should appear at the document's start.

### header:

- **Purpose:**  
  Define a new section.
  
- **Syntax:**  
  ```
  header: Section Title
  ```
  - Text following the token is the header title.
  - Content under a header must be uniformly indented.

### text:

- **Purpose:**  
  Represent narrative or descriptive text.
  
- **Syntax:**  
  ```
  text: This is a paragraph of text.
  ```
  - Multi-line text can be written as a single line OR, for long-form paragraphs, use open/close delimiters (see Multi-Line Text Blocks below).

### list:

- **Purpose:**  
  Introduce a list of items.
  
- **Syntax:**  
  ```
  list:
    - Item 1
    - Item 2
  ```
  - A hyphen (`-`) on indented lines marks each list item.

### code:

- **Purpose:**  
  Delimit preformatted or code blocks.
  
- **Syntax:**  
  ```
  code:
    def example():
        return "code block"
  ```
  - All indented lines until the next non-indented line or reserved token belong to the code block.

---

## 5. Additional Features and Enhancements

### 5.1 Inline Annotations

- **Purpose:**  
  Allow in-line annotations without disrupting narrative flow.
  
- **Standard Syntax (Parentheses):**  
  ```
  text: This is a sentence (note: do not delete the database again).
  ```
  
- **Alternate (Recommended for AI Clarity):**  
  ```
  text: This is a sentence [note: do not delete the database again].
  ```
- **Guideline:**  
  Parsers should treat bracketed annotations as structured metadata, ensuring they do not blend with the surrounding text.

### 5.2 Multi-Line Text Blocks

- **Purpose:**  
  Facilitate long-form paragraphs without forced line breaks.
  
- **Delimiter-Based Syntax:**  
  Use custom open/close delimiters to encapsulate multi-line text.
  
- **Example:**  
  ```
  text:
    >>>
    This is a long paragraph spanning multiple lines.
    It allows for natural narrative flow without awkward line-by-line concatenation.
    <<<
  ```
- **Note:**  
  The delimiters `>>>` and `<<<` are recommended; implementations may allow alternative custom markers.

### 5.3 Custom Directives

- **Purpose:**  
  Extend SLAP functionality for specialized content (e.g., tables, images, citations).
  
- **Syntax:**  
  Custom directives must use the reserved prefix `x-`.
  
  **Example:**  
  ```
  x-table:
    - row: Cell1, Cell2, Cell3
    - row: Data1, Data2, Data3
  ```
- **Guideline:**  
  Unknown custom directives should be ignored gracefully by parsers.

### 5.4 Extended Block Types

- **Inline Key/Value Pairs:**  
  Embed structured data within text using braces.  
  **Example:**  
  ```
  text: User info {id=123, role=admin}
  ```
  
- **Callouts/Notes:**  
  Reserved tokens like `note:` or `warn:` can highlight critical information.  
  **Example:**  
  ```
  note: Critical update required before deployment.
  ```

---

## 6. Error Handling & Recovery

- **Preservation of Context:**  
  Upon encountering an error, the parser should:
  - Capture and log the current block header and the first few lines of the block.
  - Continue processing the next top-level token block instead of aborting entirely.
  
- **Fallback Behavior:**  
  For unrecoverable errors, output an error summary that includes the context and suggested location of the error.
  
- **Robust Logging:**  
  All errors should be logged with sufficient detail so that developers can identify and correct issues without needing to reprocess the entire document.

---

## 7. Parsing and Rendering Guidelines

- **Line-by-Line Processing:**  
  Process the document sequentially, with reserved tokens and indentation guiding block boundaries.
  
- **State Management:**  
  Maintain context for nested blocks via consistent tracking of indentation levels.
  
- **Rendering:**  
  Convert SLAP documents into user-friendly formats (e.g., Markdown, HTML) without inserting extra tokens. The renderer must preserve the logical hierarchy defined by SLAP.
  
- **Consistency Checks:**  
  Validate token placement and indentation; issue warnings for inconsistencies to aid in debugging.

---

## 8. Implementation Guidelines

- **Parser Libraries:**  
  Develop and maintain libraries in popular languages (Python, JavaScript) to support SLAP.
  
- **Tooling:**  
  Provide command-line tools and example projects to ease the adoption of SLAP.
  
- **Testing:**  
  Create robust test suites covering all aspects of token recognition, nesting, error recovery, and custom directive handling.
  
- **Continuous Integration:**  
  Ensure ongoing compatibility with automated CI pipelines to catch regressions and maintain stability.

---

## 9. Versioning and Extensibility

- **Version Declarations:**  
  Each SLAP document should include a version (as specified in meta) to signal compatibility.
  
- **Future Extensions:**  
  New tokens should be introduced under reserved namespaces (e.g., `x-`) to ensure backward compatibility.
  
- **Graceful Degradation:**  
  Parsers should ignore unknown tokens while processing recognized tokens without failure.

---

## 10. License and Contribution

- **License:**  
  This specification is released under the MIT License. See the LICENSE file for details.
  
- **Contribution Guidelines:**  
  Contributions, bug fixes, and enhancements are welcome. Please follow the standard issue and pull request processes.
  
- **Community Feedback:**  
  Continuous improvements are driven by the SLAP community. Please submit issues or feature requests on the repository.

---

*Thank you for using SLAP – Structured Lightweight Authoring Protocol. We look forward to your feedback and contributions as we continue to make documentation leaner, clearer, and more robust.*
