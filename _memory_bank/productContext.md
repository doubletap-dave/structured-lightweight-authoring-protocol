---
fileWeight: medium
linkedPatterns: []
confidenceRating: 0.85
triggeredByTick: tick-X1963B3F7485
---

header: Product Context
  text: Nomenic Core is a modern, line-oriented structured document format designed for both human readability and machine parsing. It seeks a middle ground between Markdown's simplicity and YAML's structure.

header: Target Users
  list:
    - **Technical Writers**: Documentation teams needing structured but readable formats
    - **Developers**: For configuration, code documentation, and semantic information
    - **Content Teams**: Mixed technical/non-technical environments needing structure
    - **API Documentation**: Explicit structure with embedded code examples
    - **Knowledge Bases**: Highly structured information repositories

header: Key Differentiators
  list:
    - **Explicit Structure**: No ambiguity through clear token markers
    - **Uniform Syntax**: Consistent patterns with minimal special cases
    - **Extensible**: Custom directives and metadata support
    - **Migration-Friendly**: Clear upgrade paths and compatibility design
    - **Robustness**: Comprehensive error detection, reporting, and recovery
    - **Developer Experience**: Detailed error messages with position information
    - **Fault Tolerance**: Ability to process partial documents even with errors

header: Use Cases
  list:
    - **Technical Documentation**: With nested structure, code blocks, and callouts
    - **Configuration Files**: With strict validation and clear errors
    - **Knowledge Repositories**: With semantic structure and rich metadata
    - **Structured Notes**: Personal or team knowledge management
    - **API Specifications**: Structured endpoint and parameter documentation

header: Current Status
  text: "Phase 3: Testing & Validation" - Specification is complete. Lexer is fully implemented with all tests passing. Parser implementation is complete with all block types, robust error handling, AST optimization, document validation, and visitor pattern implementation. All 42 tests are passing with clean linting. Current focus is on expanding test coverage with edge cases and complex documents, implementing performance benchmarks, and planning for CLI tooling in Phase 4. 