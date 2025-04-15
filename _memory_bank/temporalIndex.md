header: Temporal Index (Recent Ticks)
  text: Tracks recent memory-impacting events. Older events are moved to `temporalArchive.md`.

table:
  - row: tick | event | files | causality | mood | note
  - row: 0000000001 | /nmb | projectBrief.md, productContext.md, techContext.md, systemPatterns.md, activeContext.md, progress.md, lessonsLearned.md, .cursorrules | --- | ✨ | Initial Memory Bank creation
  - row: 0000000002 | /umb | .cursorrules, activeContext.md, temporalIndex.md | <-0000000001 | 🏗️ | Project structure setup per spec
  - row: 0000000003 | /plan | projectBrief.md | <-0000000002 | 🗺️ | Generated Development Roadmap
  - row: 0000000004 | /umb | spec/TOKEN-SCHEMA.nmc, activeContext.md, temporalIndex.md, .cursorrules | <-0000000003 | 💾 | Session update: Plan & Token Schema Refinement 