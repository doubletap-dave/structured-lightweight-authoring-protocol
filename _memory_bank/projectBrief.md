---
fileWeight: high
linkedPatterns: []
confidenceRating: 0.95
triggeredByTick: tick-X1963B3F7485
---

header: Project Brief: Nomenic Core
  text: Nomenic Core is a structured document format designed for both human readability and machine parsing, bridging the gap between Markdown's simplicity and YAML's structure. This project delivers a complete specification and reference implementation in Python.

header: Project Vision
  text: Create a modern document format optimized for both human authors and AI/ML processing that supports rich semantic structures while maintaining readability.

header: Core Requirements
  list:
    - Complete specification with grammar rules and examples
    - Python reference implementation with lexer, parser, validator
    - Conversion utilities (to/from Markdown, YAML)
    - Documentation and migration guides for adopters
    - Support for common use-cases: technical docs, configs, structured notes

header: Completed Milestones
  list:
    - Phase 1: Core Specification Defined
      - ✅ NOMENIC-CORE.md created with token definitions
      - ✅ TOKEN-SCHEMA.nmc defining standard tokens
      - ✅ GRAMMAR.md with formal EBNF grammar
    - Phase 2: Parser Implementation
      - ✅ Token and TokenType classes defined
      - ✅ Lexer implementation completed
      - ✅ Basic AST node structure defined
      - ✅ Parser stub with documentation
      - ✅ Robust error handling with detection, reporting, and recovery
      - ✅ Complete parser implementation
      - ✅ AST optimization and normalization
      - ✅ Document validation functionality
    - Phase 3: Testing & Validation (in progress)
      - ✅ Basic test suite with pytest
      - ✅ Test fixtures for valid/invalid documents
      - ✅ Pre-commit hooks for quality
      - ✅ Error handling test suite
      - ✅ Parser validation test suite
      - ❌ Code coverage targets met
      - ❌ Documentation tests
      - ❌ Fuzz/property-based testing

header: Current Development Roadmap
  list:
    - Phase 2: Core Parser Implementation ✅
      - [✅] 2.1: Define Token classes and interfaces
      - [✅] 2.2: Implement Lexer tokenization
      - [✅] 2.3: Define AST node structure
      - [✅] 2.4: Implement Parser (AST generation)
        - [✅] 2.4.1: Parser stub with documentation
        - [✅] 2.4.2: Error handling infrastructure
        - [✅] 2.4.3: Header, list and text block parsing
        - [✅] 2.4.4: Comprehensive error reporting, recording, and recovery
        - [✅] 2.4.5: Implement remaining block types
        - [✅] 2.4.6: Implement validation rules
        - [✅] 2.4.7: AST optimization and normalization
      - [✅] 2.5: Document format validation
      - [✅] 2.6: Visitor pattern implementation

    - Phase 3: Testing & Validation
      - [✅] 3.1: Basic test infrastructure setup (pytest, coverage)
      - [✅] 3.2: Core token/lexer tests
      - [✅] 3.3: Parser error handling tests
      - [✅] 3.4: AST verification tests
      - [ ] 3.5: Edge case & stress tests
      - [ ] 3.6: Performance benchmarks

    - Phase 4: CLI Tooling & Basic Conversion
      - [ ] 4.1: CLI structure and subcommands
      - [ ] 4.2: Rendering to HTML
      - [ ] 4.3: Converting from/to Markdown
      - [ ] 4.4: Converting from/to YAML
      - [ ] 4.5: Validation command

    - Phase 5: Documentation & Examples
      - [ ] 5.1: User guide
      - [ ] 5.2: API documentation
      - [ ] 5.3: Example documents
      - [ ] 5.4: Migration guides

    - Phase 6: Refinement & Extensibility
      - [ ] 6.1: Performance optimization
      - [ ] 6.2: Extension mechanism
      - [ ] 6.3: Plugin infrastructure
      - [ ] 6.4: Integration examples

header: Current Focus Areas
  list:
    - Continue with Phase 3: Expand test suite with edge cases and complex documents
    - Implement performance benchmarks for parser and lexer
    - Prepare for CLI tooling implementation in Phase 4
    - Plan documentation updates for completed parser components 