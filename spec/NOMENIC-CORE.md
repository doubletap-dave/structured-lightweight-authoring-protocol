# Nomenic Core Specification

**Version:** 1.0.0  
**Date:** 2025-04-14  
**Tagline:** Nomenic: Structure Everything.

> **File Extension:** Nomenic Core files use the `.nmc` extension.

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

**Nomenic** is a structured authoring format designed to balance semantic clarity, human readability, and AI efficiency. It offers a token-efficient alternative to markdown while preserving logical structure, extensibility, and precision. Whether you're documenting systems, writing specs, or generating machine-optimized content, Nomenic enables clean, consistent, and structured writing that scales.

---

## 2. Design Goals

- **Minimal Syntax Overhead:**  
  Only the essentials. Token-light and signal-rich.

- **Human Readability:**  
  Documents should look like what they mean. Easy to write, easier to scan.

- **Efficient Token Usage:**  
  Designed with LLMs and parsers in mind. Every character does work.

- **Clear Structure and Hierarchy:**  
  Based on indentation and explicit tokens. Predictable and declarative.

- **Extensibility:**  
  Future-proofed via namespacing (`x-` directives) and dynamic metadata.

---

## 3. General Syntax

### 3.1 Line-Oriented Structure

- **One Unit per Line:**  
  Each line represents a single instruction or token. Simple.

- **Token Positioning:**  
  Reserved tokens must start the line. Leading indentation defines scope.

### 3.2 Indentation and Nesting

- **Spaces Only:**  
  Tabs are illegal. 2-space indent is the norm.

- **Nested Logic:**  
  Sub-blocks must be indented beneath their parent token.

---

## 4. Reserved Tokens

The core primitives of Nomenic documents:

### table:

- **Purpose:** Define structured tabular data.
- **Syntax:**
  ```
  table:
    - row: Header1, Header2
    - row: Value1, Value2
  ```
  - Tables are rendered as `<table>`, with each `row:` treated as a `<tr>`.
### meta:

- **Purpose:** Top-level document metadata.
- **Syntax:**
  ```
  meta: key1=value1, key2=value2
  ```

### header:

- **Purpose:** Section headings.
- **Syntax:**
  ```
  header: Descriptive Section Title
  ```

### text:

- **Purpose:** Paragraphs and body content.
- **Syntax:**
  ```
  text: Single-line content here.
  ```
  - For multiline, see section 5.2

### list:

- **Purpose:** List structures.
- **Syntax:**
  ```
  list:
    - item one
    - item two
    1. ordered item one
    a. ordered item two
  ```
- **Note:** Supports both unordered (`-`) and ordered (`1.`, `a.`, `i.`, etc.) list item markers followed by a space.

### code:

- **Purpose:** Code snippets or preformatted content.
- **Syntax:**
  ```
  code:
    def hello():
        return "world"
  ```

---

## 5. Additional Features and Enhancements

### 5.1 Inline Annotations

- **Purpose:** Add context or notes within a line.
- **Examples:**
  ```
  text: This is inline (note: test it).
  text: This is inline [note: recommended].
  ```

### 5.2 Multi-Line Text Blocks

- **Purpose:** Block paragraphs without explicit line breaks.
- **Syntax:**
  ```
  text:
    >>>
    This is a paragraph.
    It spans multiple lines.
    <<<
  ```

### 5.3 Custom Directives

- **Purpose:** Extend functionality through user-defined tokens.

- **Syntax:**
  ```
  x-quote:
    >>>
    This is a custom directive block.
    It renders according to its definition.
    <<<
  ```

- **Behavior:**
  Parsers encountering a token prefixed with `x-` must:
  1. Treat it as a valid block token.
  2. Attempt to resolve its behavior using a Token Definition Schema (see `TOKEN-SCHEMA.nmc`).
  3. If no rule exists, fall back to generic rendering (e.g., as a `<div class="x-quote">` with preformatted content).

- **Goal:** Allow new block types without changing the parser core. Useful for experimentation, plugins, and community-defined extensions.** Extend functionality.
- **Syntax:**
  ```
  table:
    - row: Cell1, Cell2
    - row: Value1, Value2
  ```
  - All custom tokens must be prefixed with `x-`

### 5.4 Extended Block Types

- **Inline key/values:**
  ```
  text: User data {id=3, role=admin}
  ```

- **Callouts:**
  ```
  note: This is important.
  warn: This is a warning.
  ```

---

## 6. Error Handling & Recovery

- **Fault-Tolerant Parsing:**
  - Log token, context, and line number on failure.
  - Continue to next valid block.

- **Fallback Output:**
  - Should produce a minimal valid version.

- **Logging:**
  - Errors must be human-readable. No cryptic stack traces.

---

## 7. Parsing and Rendering Guidelines

- **Sequential Processing:**  
  Read top to bottom. One line at a time.

- **Respect Nesting:**  
  Use indentation to determine block hierarchy.

- **Flexible Output Targets:**  
  Render to HTML, Markdown fallback, JSON, or tokens.

- **Validation:**  
  Warn for incorrect tokens, indentation, or block misuse.

### 🔤 Short Token Aliases

For convenience, parsers may support the following short forms:

| Long Token | Short Alias |
|------------|-------------|
| `meta:`    | `m:`        |
| `header:`  | `h:`        |
| `text:`    | `t:`        |
| `list:`    | `l:`        |
| `code:`    | `c:`        |
| `table:`   | `tb:`       |
| `note:`    | `n:`        |
| `warn:`    | `w:`        |

These are optional but encouraged for faster authoring. The spec will continue to use full tokens for clarity.  
  Read top to bottom. One line at a time.

- **Respect Nesting:**  
  Use indentation to determine block hierarchy.

- **Flexible Output Targets:**  
  Render to HTML, Markdown fallback, JSON, or tokens.

- **Validation:**  
  Warn for incorrect tokens, indentation, or block misuse.

---

## 8. Implementation Guidelines

- **Parser First:**  
  Python or JS recommended. Formal grammar optional.

- **Command Line Tools:**  
  Include `nomenic lint`, `nomenic render`, `nomenic parse`.

- **Testing:**  
  Validate on malformed input, deep nesting, edge cases.

- **CI Friendly:**  
  Make linting and transformation tools integrable with GitHub Actions.

### 📁 Suggested Project Structure

```
nomenic/
├── spec/                        # Formal specifications
│   ├── NOMENIC-CORE.md          # Core spec (this file)
│   ├── TOKEN-SCHEMA.nmc         # Token definition registry
│   ├── meta-parser.md           # How to parse with dynamic schemas
│   └── extensions.md            # Optional extensions (e.g., quote, diagram)
│
├── cli/                         # The CLI toolchain
│   ├── main.py    # Entry point
│   └── commands/                # Lint, render, parse, etc.
│       ├── lint.py
│       ├── render.py
│       ├── parse.py
│
├── playground/                  # Web-based editor + preview
│   └── web-renderer/            # HTML + CSS + JS playground
│
├── docs/                        # Human-facing documentation
│   ├── README.md                # Intro to the ecosystem
│   ├── quickstart.md            # TL;DR usage
│   ├── developer-guide.md       # Build your own parser, renderer, etc.
│   └── migration-guide.md       # From Markdown to Nomenic
│
├── .github/                     # GitHub Actions and config
│   └── workflows/
│       └── render.yml           # Render .nmc → HTML on push
│
├── site/                        # Static site generator input
│   └── nomenic.com              # Landing page content
│
├── examples/                    # Sample `.nmc` files
│   └── overview.nmc
│   └── nested-logic.nmc
│
└── test/                        # Test cases and schemas
    ├── syntax-errors.nmc
    ├── expected-output.json
    └── render-tests/
```
**  
  Python or JS recommended. Formal grammar optional.

- **Command Line Tools:**  
  Include `nomenic lint`, `nomenic render`, `nomenic parse`.

- **Testing:**  
  Validate on malformed input, deep nesting, edge cases.

- **CI Friendly:**  
  Make linting and transformation tools integrable with GitHub Actions.

---

## 9. Versioning and Extensibility

- **Meta Version Required:**
  - Always declare `meta: version=1.0.0`

- **Namespace Future Additions:**
  - New blocks should start with `x-`

- **Forward Compatibility:**
  - Parsers must gracefully skip unknown tokens.

---

## 10. License and Contribution

- **License:**  
  BSD 3-Clause. See [`LICENSE`](LICENSE).

- **Contribute:**  
  Fork, file issues, submit PRs.

- **Community:**  
  Open. Transparent. You know where to find us.

---

Thanks for choosing Nomenic. Now go structure something elegant.

