---
fileWeight: low
linkedPatterns: []
confidenceRating: 0.85
triggeredByTick: tick-000000000E
---

header: Lessons Learned
  text: A log of insights, challenges, and discoveries during the Nomenic Core project.

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