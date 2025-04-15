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