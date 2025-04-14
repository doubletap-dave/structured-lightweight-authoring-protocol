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
  ```

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

- **Purpose:** Extend functionality.
- **Syntax:**
  ```
  x-table:
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

