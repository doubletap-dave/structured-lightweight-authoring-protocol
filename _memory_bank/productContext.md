---
fileWeight: medium
linkedPatterns: []
confidenceRating: 0.85
triggeredByTick: tick-000000000E
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
  text: "Phase 2: Core Parser Implementation" - Specification is complete. Lexer is fully implemented with all tests passing. Parser is under active development with robust error handling. Pre-commit hooks, test infrastructure, and documentation are continuously improving. 