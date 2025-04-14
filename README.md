# Nomenic Core
<p align="center"><strong>Finally, a spec that won’t make your parser cry.</strong></p>

<p align="center">
  <em>Version 1.2 — 2025-04-10</em>
</p>

## 🚀 Overview

**SLAP** is a minimalist markup language designed for clean, structured documentation. It keeps your syntax tight, your tokens lean, and your indentation holy. SLAP is made for humans and machines who like their docs fast, readable, and just a little judgmental.

Originally evolved from Compact Structured Markup (CSM), SLAP is smarter, snappier, and intentionally built to thrive in AI-integrated environments.

---

## ✨ Key Features

- **Minimal Syntax, Max Clarity**\
  Reserved tokens, clean indentation, and zero tolerance for clutter.

- **Token-Efficient by Design**\
  Built with language models and compact processing in mind.

- **Smarter Inline Annotations**\
  Keep your notes structured and unobtrusive:

  ```slap
  text: This is inline [note: keep it clean].
  ```

- **Multi-Line Text Blocks (finally)**\
  Write real paragraphs like a grown-up:

  ```slap
  text:
    >>>
    This is a beautiful, flowing paragraph
    with no line-break guilt.
    <<<
  ```

- **Custom Directives**\
  Add tables, weird blocks, or custom magic using `x-` directives.

- **Error Tolerance Built-In**\
  SLAP parsers log, recover, and keep moving. No more crashing on syntax sadness.

---

## 📚 Full Specification

You want the deep cuts? Head over to [`SPECIFICATION.md`](SPECIFICATION.md) for:

- Core tokens (`meta`, `header`, `text`, `list`, `code`)
- Annotations, block delimiters, and custom directive usage
- Error handling, rendering rules, and parser structure
- Implementation advice for building SLAP-aware tools

---

## 🛠️ Getting Started

### Install

```bash
git clone https://github.com/your-username/structured-lightweight-authoring-protocol.git
cd structured-lightweight-authoring-protocol
```

### Usage

1. **Write in SLAP**\
   Create a file like `example.slap` and structure it using the core syntax.

2. **Parse It**\
   Use the sample parsers in `/parsers` (Python, JS, etc.) to validate and render.

   TODO TODO TODO TODO TODO TODO

3. **Extend It**\
   Add your own `x-whatever:` blocks. SLAP won’t complain.

---

## 🤝 Contributing

- Open an issue if something feels wrong.
- Fork and PR if you have something better.
- Use SLAP in the wild and share what you build.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for actual rules and etiquette.

---

## 📄 License

This project is licensed under the BSD 3-Clause. See [`LICENSE`](LICENSE) for the legal boilerplate.

---

> SLAP: Because Markdown's been getting away with too much for too long.
