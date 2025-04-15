header: Temporal Index (Recent Ticks)
  text: Tracks recent memory-impacting events. Older events are moved to `temporalArchive.md`.

table:
  - row: tick | event | files | causality | mood | note
  - row: 0000000001 | /nmb | projectBrief.md, productContext.md, techContext.md, systemPatterns.md, activeContext.md, progress.md, lessonsLearned.md, .cursorrules | --- | ✨ | Initial Memory Bank creation
  - row: 0000000002 | /umb | .cursorrules, activeContext.md, temporalIndex.md | <-0000000001 | 🏗️ | Project structure setup per spec
  - row: 0000000003 | /plan | projectBrief.md | <-0000000002 | 🗺️ | Generated Development Roadmap
  - row: 0000000004 | /umb | spec/TOKEN-SCHEMA.nmc, activeContext.md, temporalIndex.md, .cursorrules | <-0000000003 | 💾 | Session update: Plan & Token Schema Refinement 
  - row: 0000000005 | /umb | spec/GRAMMAR.md, spec/NOMENIC-CORE.md, _memory_bank/activeContext.md, _memory_bank/progress.md, .cursorrules | <-0000000004 | ⚙️ | Session update: Created & refined EBNF Grammar, aligned spec docs 
  - row: 0000000006 | /umb | src/nomenic/*, _memory_bank/activeContext.md, .cursorrules | <-0000000005 | 🏗️ | Session update: Confirmed Python, created initial src/nomenic structure
  - row: 0000000007 | /umb | _memory_bank/lessonsLearned.md, temporalIndex.md | <-0000000006 | 📝 | Added spec improvement notes for Phase 5/6
  - row: 0000000008 | /umb | src/nomenic/tokens.py, src/nomenic/lexer.py, src/nomenic/__init__.py, _memory_bank/activeContext.md, _memory_bank/progress.md, temporalIndex.md | <-0000000007 | 🧩 | Implemented Token definitions and Lexer for Nomenic Core
  - row: 0000000009 | /umb | _memory_bank/temporalIndex.md | <-0000000008 | 💾 | Session update: Lexer implementation complete
  - row: 000000000A | /umb | requirements-dev.txt, pyproject.toml, .pre-commit-config.yaml, tests/unit/test_errors.py, _memory_bank/activeContext.md, _memory_bank/progress.md, _memory_bank/projectBrief.md, _memory_bank/temporalIndex.md | <-0000000009 | 🛠️ | Dev container, pre-commit, ruff, bandit, black, isort, pytest integrated; roadmap realigned; error handling and parser scaffolding in progress
  - row: 000000000B | /rmb | src/nomenic/lexer.py, _memory_bank/activeContext.md, _memory_bank/progress.md, _memory_bank/temporalIndex.md | <-000000000A | 🐛 | Fixed all 12 lexer test failures: regex escaping, optional whitespace, indented block tokens, code blocks, inline styles
  - row: 000000000C | /umb | projectBrief.md, productContext.md, techContext.md, systemPatterns.md, activeContext.md, progress.md, lessonsLearned.md, temporalIndex.md | <-000000000B | 💾 | Session update: Bandit fully suppressed, ruff clean, Memory Bank sync.
  - row: 000000000D | /umb | projectBrief.md, productContext.md, techContext.md, systemPatterns.md, activeContext.md, progress.md, lessonsLearned.md, temporalIndex.md | <-000000000C | 💾 | Session update: Parser, tests, and Memory Bank fully synced.
  - row: 000000000E | /umb | src/nomenic/parser.py, tests/unit/test_parser_errors.py, debug_parser.py, _memory_bank/activeContext.md, _memory_bank/progress.md, _memory_bank/temporalIndex.md, _memory_bank/lessonsLearned.md | <-000000000D | 🛡️ | Implemented robust parser error handling, detection, reporting, and recovery with comprehensive test suite.
  - row: X1963B2BCA42 | /umb | src/nomenic/ast.py, src/nomenic/parser.py, tests/unit/test_parser.py, tests/unit/test_parser_errors.py, debug_parser.py, _memory_bank/activeContext.md, _memory_bank/progress.md, _memory_bank/temporalIndex.md | <-000000000E | 🧹 | Fixed linting issues, improved typing annotations, merged with main branch.