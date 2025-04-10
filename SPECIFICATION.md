# Structured Lightweight Authoring Protocol (SLAP) Specification

**Version:** 1.2  
**Date:** 2025-04-10  
**Tagline:** SLAP: Finally, a spec that won’t make your parser cry.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Design Goals](#design-goals)
3. [General Syntax](#general-syntax)
   1. [Line-Oriented Structure](#line-oriented-structure)
   2. [Indentation and Nesting](#indentation-and-nesting)
4. [Reserved Tokens](#reserved-tokens)
   1. [meta:](#meta)
   2. [header:](#header)
   3. [text:](#text)
   4. [list:](#list)
   5. [code:](#code)
5. [Additional Features and Enhancements](#additional-features-and-enhancements)
   1. [Inline Annotations](#inline-annotations)
   2. [Multi-Line Text Blocks](#multi-line-text-blocks)
   3. [Custom Directives](#custom-directives)
   4. [Extended Block Types](#extended-block-types)
6. [Error Handling & Recovery](#error-handling--recovery)
7. [Parsing and Rendering Guidelines](#parsing-and-rendering-guidelines)
8. [Implementation Guidelines](#implementation-guidelines)
9. [Versioning and Extensibility](#versioning-and-extensibility)
10. [License and Contribution](#license-and-contribution)

---

## 1. Introduction

Structured Lightweight Authoring Protocol (SLAP) is a no-nonsense markup language built for clean, structured documentation. It balances human readability with machine efficiency, especially when used with AI systems. SLAP minimizes token bloat while preserving hierarchy, clarity, and extensibility.

---

## 2. Design Goals

- **Minimal Syntax Overhead:**  
  Only the essentials. No extra fluff. Token count stays low without compromising structure.

- **Human Readability:**  
  SLAP reads like plain text, not an incantation. Easy to write, easier to scan.

- **Efficient Token Usage:**  
  Designed with AI processing in mind, every character counts. Compact without being cryptic.

- **Clear Structure and Hierarchy:**  
  Indentation and line-by-line formatting enforce a predictable and maintainable document flow.

- **Extensibility:**  
  Custom directives and reserved namespaces let SLAP grow without breaking existing documents.

---

## 3. General Syntax

### 3.1 Line-Oriented Structure

- **One Unit per Line:**  
  Each line = a logical unit. Tokens lead the line, structure follows.

- **Token Positioning:**  
  Reserved tokens must start each line, right after any indentation.

### 3.2 Indentation and Nesting

- **Spaces Only:**  
  Tabs are banned. Two spaces per level is the gentle recommendation.

- **Nested Logic:**  
  Child blocks must be indented consistently beneath their parent token.

---

## 4. Reserved Tokens

The building blocks of SLAP. These keywords define structure:

### meta:

- **Purpose:** Document-level metadata.
- **Syntax:**
  ```
  meta: key1=value1, key2=value2
  ```
  - Place at the beginning of the document.

### header:

- **Purpose:** Section headers.
- **Syntax:**
  ```
  header: Title Goes Here
  ```
  - All indented content beneath belongs to this section.

### text:

- **Purpose:** Narrative or paragraph content.
- **Syntax:**
  ```
  text: This is a sentence.
  ```
  - For long blocks, use multi-line delimiters (see 5.2).

### list:

- **Purpose:** Lists of stuff.
- **Syntax:**
  ```
  list:
    - First item
    - Second item
  ```
  - Each `-` must be on an indented line.

### code:

- **Purpose:** Code snippets or preformatted text.
- **Syntax:**
  ```
  code:
    def hello():
        return "world"
  ```
  - Ends when indentation stops or a new reserved token starts.

---

## 5. Additional Features and Enhancements

### 5.1 Inline Annotations

- **Purpose:** Add metadata without breaking flow.
- **Examples:**
  ```
  text: This is inline (note: test it).
  text: This is inline [note: recommended].
  ```
- **Recommendation:** Use brackets for clarity in AI contexts.

### 5.2 Multi-Line Text Blocks

- **Purpose:** Write full paragraphs without newlines after every sentence.
- **Syntax:**
  ```
  text:
    >>>
    This is a long paragraph.
    With multiple lines.
    <<<
  ```
- **Note:** `>>>` and `<<<` are default delimiters.

### 5.3 Custom Directives

- **Purpose:** Add new behaviors or block types (tables, citations, unicorns).
- **Syntax:**
  ```
  x-table:
    - row: Cell1, Cell2
    - row: Data1, Data2
  ```
- **Rule:** All custom directives must start with `x-`.

### 5.4 Extended Block Types

- **Inline key/value pairs:**
  ```
  text: User info {id=42, role=admin}
  ```

- **Callouts:**
  ```
  note: This is important.
  warn: This is a problem.
  ```

---

## 6. Error Handling & Recovery

- **Don’t die on the first bug:**
  - Log context, block type, and line number.
  - Skip to the next top-level token.

- **Fallback Output:**
  - Provide summaries with actionable detail.

- **Logging:**
  - Make logs human-readable. Help users help themselves.

---

## 7. Parsing and Rendering Guidelines

- **Sequential Processing:**  
  One line at a time. Respect indentation and tokens.

- **Track Nesting:**  
  Use indentation to know where you are.

- **Render Clearly:**  
  Translate to HTML, Markdown, or plain text while preserving intent.

- **Catch Mistakes:**  
  Validate token use and spacing. Warn users when stuff looks off.

---

## 8. Implementation Guidelines

- **Build Parsers:**  
  Python, JS—start there. The world will follow.

- **CLI Tools:**  
  Make it easy for users to validate and render `.slap` files.

- **Test Everything:**  
  From basic tokens to cursed nesting scenarios.

- **Automate Sanity:**  
  Use CI to catch regressions and prevent chaos.

---

## 9. Versioning and Extensibility

- **Declare Versions:**  
  Always include a version in `meta:`.

- **Namespace the New Stuff:**  
  All future tokens go under `x-` unless promoted to core.

- **Handle Unknowns Gracefully:**  
  Skip or warn—don’t crash.

---

## 10. License and Contribution

- **License:**  
  Released under the BSD 3-Clause. See [`LICENSE`](LICENSE).

- **Contribute:**  
  Fork it, file issues, make it better. Follow the rules, earn the glory.

- **Community:**  
  Feedback drives evolution. You know where to find us.

---

Thanks for using SLAP. Now go write something structured and beautiful.

