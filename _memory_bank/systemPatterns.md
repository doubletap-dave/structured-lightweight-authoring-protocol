---
fileWeight: medium
linkedPatterns: []
confidenceRating: 0.8
triggeredByTick: tick-000000000E
---

header: System Patterns Registry
  text: This file tracks recognized and reusable patterns within the Nomenic Core project and its ecosystem.

header: Core Design Patterns
  list:
    - **Pipeline Architecture**: Sequential lexer → parser → processor → renderer pipeline.
    - **Token Stream**: Unified token representation independent of source format.
    - **Visitor Pattern**: Traversing AST nodes for transformations and rendering.
    - **Factory Methods**: Standardized node creation/instantiation.
    - **Observer Pattern**: Notification of state changes during parsing.

header: Error Handling Patterns
  list:
    - **Dual Error Modes**: Both recording (non-fatal) and reporting (exception-raising) modes.
    - **Error Context Capture**: Storing token positions and context with each error.
    - **Synchronization Points**: Defining statement boundaries for error recovery.
    - **Progressive Degradation**: Continuing to parse as much as possible despite errors.
    - **Category-Based Organization**: Grouping errors by type (syntax, semantic, etc.)
    - **Diagnostic Tooling**: Purpose-built tools for error analysis.
    - **Test-First Validation**: Comprehensive test suite for error scenarios.

header: Pattern: nomenic-core-syntax
  description: Base syntax rules and conventions for Nomenic Core documents
  status: stable
  version: 1.0.0
  components:
    - Line-oriented structure with explicit tokens
    - Indentation-based nesting (2 spaces)
    - Block-level elements with clear delimiters
    - Inline annotations for metadata
  implementation: src/nomenic/lexer.py, src/nomenic/parser.py
  reference: `SPECIFICATION.md`, `_memory_bank/techContext.md` 