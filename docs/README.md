# Nomenic Core
<p align="center"><strong>The structured format that won’t make your parser cry.</strong></p>

<p align="center">
  <em>Version 1.0.0 — 2025-04-14</em>
</p>

---

## 🚀 Overview

**Nomenic Core** is a structured authoring format engineered for clarity, AI efficiency, and machine-readable precision. It’s the antidote to bloated markdown, brittle YAML, and human-hostile XML. Nomenic keeps your docs clean, your tokens lean, and your structure fully intact.

Born from the frustrations of maintaining both human-readable and machine-consumable documentation, Nomenic is built to unify writing, parsing, and reasoning under one extensible format.

---

## ✨ Key Features

- **Minimal Syntax, Max Clarity**  
  Reserved tokens, indentation-based hierarchy, and zero ambiguity.

- **Token-Efficient by Design**  
  Friendly to LLMs and structured parsers. Compact where it counts.

- **Smarter Inline Annotations**  
  Embedded notes that don’t pollute the prose:

  ```nmc
  text: This is inline [note: keep it clean].
  ```

- **Multi-Line Paragraph Blocks**  
  Write real text. Get real formatting.

  ```nmc
  text:
    >>>
    This is a full paragraph
    spanning multiple lines
    with no markdown shame.
    <<<
  ```

- **Custom Directives**  
  Need a table? A callout? A magical block? Use `x-` and go wild.

- **Built for Error Recovery**  
  Parsers log and recover. The spec doesn’t assume you’re perfect.

---

## 📚 Full Specification

If you like your structure documented, you'll love [`SPECIFICATION.md`](SPECIFICATION.md).

Covers:
- Core tokens like `meta`, `header`, `text`, `list`, and `code`
- Annotations, callouts, multiline formatting, and extensions
- Parser expectations, rendering pipelines, and CLI conventions
- Implementation notes and error-handling policies

---

## 🛠️ Getting Started

### Install

```bash
git clone https://github.com/your-org/nomenic-core.git
cd nomenic-core
```

### Usage

1. **Write with Structure**  
   Create a file like `example.nmc` and write using the Nomenic format.

2. **Parse and Render**  
   Use the starter parsers in `/parsers` to validate and transform.

3. **Extend**  
   Add your own directives using `x-` prefixed tokens. It’s your playground.

> Full CLI support coming soon.

---

## 🤝 Contributing

We welcome contributions from structured beings of all kinds:
- File an issue if something breaks your brain
- Fork it and fix it if you're feeling brave
- Add docs, specs, or demos if you're feeling inspired

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to participate responsibly.

---

## 📄 License

BSD 3-Clause. Clean, permissive, and boring enough for your boss to approve it. See [`LICENSE`](LICENSE).

---

> Nomenic: Because we deserve better than markdown spaghetti.
