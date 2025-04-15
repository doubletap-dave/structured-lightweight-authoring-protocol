---
fileWeight: high
linkedPatterns: []
confidenceRating: 0.8
triggeredByTick: tick-000000000C
---

header: Product Context: Nomenic Core v1.0.0
  text: The primary product is the Nomenic Core specification itself, defining a structured authoring format. It targets developers, technical writers, and AI systems needing a balance between human readability and machine parseability.

header: Key Features (as defined in spec)
  list:
    - Minimal Syntax (Reserved tokens, indentation-based hierarchy)
    - Token-Efficiency (Designed for LLMs and parsers)
    - Inline Annotations (`[note: ...]`, `(note: ...)`)
    - Multi-Line Text Blocks (`>>> ... <<<`)
    - Custom Directives (`x-` prefix for extensibility)
    - Error Recovery focus for parsers

header: Target Audience
  list:
    - Developers creating or consuming structured data/docs.
    - Technical writers needing a precise format.
    - AI/ML engineers working with structured text generation or parsing.

header: Current Status
  text: Specification Version 1.0.0 released (as of 2025-04-14). 