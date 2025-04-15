---
fileWeight: high
linkedPatterns:
  - nomenic-core-syntax
confidenceRating: 0.9
triggeredByTick: tick-000000000E
---

header: Technical Context: Nomenic Core v1.0.0
  text: This document summarizes the core technical details based on `SPECIFICATION.md`.

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