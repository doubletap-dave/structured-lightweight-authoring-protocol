---
fileWeight: high
linkedPatterns: []
confidenceRating: 0.95
triggeredByTick: tick-000000000C
---

header: System Patterns Registry
  text: This file tracks recognized and reusable patterns within the Nomenic Core project and its ecosystem.

header: Pattern: nomenic-core-syntax
  meta: version=1.0.0, status=defined
  text: Defines the fundamental syntax structure of the Nomenic Core format as specified in v1.0.0.
  list:
    - Core Tokens: `meta`, `header`, `text`, `list`, `code`, `table`
    - Structural Elements: Indentation (2 spaces), line-orientation
    - Features: Inline annotations, multi-line text, custom `x-` directives, extended blocks (`note:`, `warn:`, inline `{}`)
  reference: `SPECIFICATION.md`, `_memory_bank/techContext.md` 