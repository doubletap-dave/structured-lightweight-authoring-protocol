---
fileWeight: low
linkedPatterns: []
confidenceRating: 0.92
triggeredByTick: tick-X1963B3F7485
---

header: Lessons Learned
  text: A log of insights, challenges, and discoveries during the Nomenic Core project.

header: Code Quality & Maintenance
  list:
    - Modern typing annotations (PEP 585): Using built-in generics (list[], tuple[]) instead of imports (List, Tuple) improves readability and future-proofs the code
    - Constants over magic numbers: Using named constants in tests clarifies intent and makes future test updates easier
    - Line length management: Breaking long comments and strings across multiple lines improves readability
    - Linter configuration: Selectively suppressing certain checks (B101/B105) where appropriate, while enforcing most rules strictly
    - Git synchronization: Regularly merging from main prevents divergence and integration headaches
    - Test driven development: Writing tests first clarifies requirements and ensures robust implementation

header: Specification Improvements (For Phase 5/6)
  list:
    - Add more explicit validation rules for parsers beyond syntax (Phase 6)
    - Include more examples throughout specifications for common use cases (Phase 5)
    - Create visual syntax diagrams to complement EBNF grammar (Phase 5)
    - Add compatibility notes comparing Nomenic to Markdown/YAML/XML for users transitioning (Phase 5)

header: Parser Implementation
  list:
    - Error recording vs. error reporting: Having two separate mechanisms (record vs raise) provides flexibility
    - Recovery with synchronization: Advancing to statement boundaries after errors allows for more complete parsing
    - Error token context: Storing the token with each error message provides invaluable position information
    - Testing error scenarios separately: Specialized test files for error handling ensure robustness
    - Diagnostic tools: Creating simple tools for error detection streamlines debugging
    - Error categories: Grouping errors by type (header, list, code, multiline) aids in documentation and testing
    - Progressive enhancements: Adding error handling incrementally prevents regression in core functionality
    - Visitor pattern: Implementing the visitor pattern for AST traversal provides flexible processing options
    - Document validation: Post-parsing validation ensures specification compliance beyond syntax
    - AST optimization: Merging adjacent similar nodes improves performance and simplifies output

header: Design Patterns
  list:
    - Visitor pattern: Powerful for separating algorithms from object structures in the AST
    - Normalization/optimization separation: Keeping normalization (structural improvement) separate from optimization (performance improvement) improves maintainability
    - Protocol interfaces: Using Python's Protocol types for interfaces improves static type checking
    - Immutable data with transformation: Returning new instances from transformations (like normalize/optimize) preserves data integrity 