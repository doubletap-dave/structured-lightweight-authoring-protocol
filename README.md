# Structured Lightweight Authoring Protocol (SLAP)

**Version:** 1.2  
**Date:** 2025-04-10  
**Tagline:** SLAP: Finally, a spec that won’t make your parser cry.

## Overview

SLAP is a minimalistic markup language designed for clear, structured documentation. It is optimized for human readability and efficient processing by AI agents—delivering low token overhead without sacrificing essential structure. SLAP is our evolution of Compact Structured Markup (CSM) with enhanced inline annotation rules, improved error recovery, and support for multi-line text blocks.

## Key Features

- **Minimal Syntax & Clear Structure:**  
  Uses only essential reserved tokens and consistent indentation to define document structure in a line-oriented manner.

- **Optimized for Token Efficiency:**  
  Designed to reduce unnecessary tokens, making it ideal for integration with AI agents and large-scale documentation.

- **Enhanced Inline Annotations:**  
  Supports in-line notes using both parentheses and brackets—with brackets recommended to avoid ambiguity in AI processing.
  - *Example:*  
    ```
    text: This is a sentence [note: do not delete the database again].
    ```

- **Multi-Line Text Blocks:**  
  Support for open/close delimiters (e.g., `>>>` and `<<<`) allows long-form paragraphs to be written naturally without forced line breaks.
  - *Example:*
    ```
    text:
      >>>
      This is a long paragraph spanning multiple lines.
      It allows for more natural narrative flow.
      <<<
    ```

- **Robust Error Handling & Recovery:**  
  Guidelines ensure that parsing errors are logged with context and processing continues with the next logical block, improving resilience for complex documents.

- **Extensible & Customizable:**  
  Built-in support for custom directives (using the `x-` prefix) and extended block types ensures that SLAP can evolve to meet future needs while preserving backward compatibility.

## Specification

The full SLAP specification is detailed in [SPECIFICATION.md](SPECIFICATION.md). It covers:

- Design goals and general syntax guidelines.
- Reserved tokens for core document structure (meta, header, text, list, code).
- Enhancements including inline annotations, multi-line text blocks, custom directives, and extended block types.
- In-depth error handling and recovery, along with parsing and rendering best practices.
- Implementation guidelines with recommendations for parser libraries, tooling, and testing.

## Getting Started

### Installation

Clone this repository to explore the SLAP specification:

```bash
git clone https://github.com/your-username/structured-lightweight-authoring-protocol.git
cd structured-lightweight-authoring-protocol
```

### Usage

1. **Writing SLAP Documents:**  
   Create a file with a `.slap` extension (e.g., `example.slap`) and follow the guidelines in the specification.
2. **Parsing Tools:**  
   Sample parser libraries and CLI tools in various languages (e.g., Python, JavaScript) are provided in the `/parsers` directory.
3. **Contributing and Extensions:**  
   Contributions to enhance SLAP and to build tooling around it are welcome. Please see the contribution guidelines for further details.

## Contributing

- **Issues:** Open issues for any features, bug reports, or enhancement suggestions.
- **Pull Requests:** Submit PRs with clear, focused changes along with a description of your modifications.
- **Community Feedback:** Engage with the community to help evolve SLAP for broader usage.

## License

📜 This project is released under the BSD 3-Clause. See the [LICENSE](LICENSE) file for details.

---

Happy documenting with SLAP!
