# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- Create CHANGELOG.md and draft initial entries
- Expand unit tests for YAMLConverter and MarkdownConverter
- Add integration tests for CLI commands (convert, render, validate, debug, lint)
- Set up CI workflow (GitHub Actions) for tests and benchmarks
- Bump package version to 1.1.0 and draft release notes

## [1.0.0] - 2025-04-14

- Initial release (v1.0.0) on 2025-04-14
  - Core specification, lexer, parser, AST, validation, error formatting
  - Extension hot-reloading, custom error formatting, array validation support
  - Performance benchmarking for lexer, parser, and end-to-end
  - Testing frameworks and coverage setup (pytest, pytest-benchmark, pytest-cov)
