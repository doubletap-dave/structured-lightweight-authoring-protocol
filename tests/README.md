# Nomenic Testing Suite

This directory contains the comprehensive test suite for the Nomenic Core project, with over 50 tests and 90% code coverage.

## Test Structure

- **unit/** - Unit tests for individual components
  - `test_tokens.py` - Tests for token definitions and behavior
  - `test_lexer.py` - Tests for the lexer and tokenization logic
  - `test_parser.py` - Core parser functionality tests
  - `test_parser_errors.py` - Tests for parser error handling capabilities
  - `test_parser_validation.py` - Tests for document validation functionality 
  - `test_parser_edge_cases.py` - Tests for complex edge cases and corner cases
  - `test_errors.py` - Tests for error classes and error handling behavior
  
- **fuzz/** - Property-based fuzz testing
  - `test_fuzz.py` - Hypothesis-based property testing to discover edge cases

- **fixtures/** - Test data and fixtures
  - Contains sample Nomenic documents for testing

- **benchmarks/** - Performance benchmarking tests
  - `performance_benchmarks.py` - Performance tests for parser and lexer
  - `benchmark_data/` - Sample documents of varying sizes for benchmarking

- **integration/** - End-to-end integration tests

## Running Tests

### Basic Test Run

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/unit/test_lexer.py
pytest tests/unit/test_parser.py

# Run tests with a specific name pattern
pytest -k "test_header"
```

### Coverage Reports

```bash
# Run tests with coverage
pytest --cov=src

# Generate HTML coverage report
pytest --cov=src --cov-report=html
```

### Benchmarks

```bash
# Run performance benchmarks
pytest tests/benchmarks/performance_benchmarks.py
```

### Fuzz Tests

```bash
# Run property-based tests
pytest tests/fuzz/test_fuzz.py
```

## Test Structure Overview

1. **Unit Tests**: Module-specific tests with minimal dependencies
2. **Error Handling Tests**: Specific tests for error scenarios
3. **Validation Tests**: Tests for document structure validity
4. **Edge Case Tests**: Tests for complex and unusual document structures
5. **Fuzz Tests**: Property-based tests that generate random input
6. **Benchmarks**: Performance and memory usage tests

## Test Coverage

Current test coverage is 90% across the codebase:
- Lexer: 86% coverage
- Parser: 90% coverage
- AST: 97% coverage

All tests are passing, with 53 unit and fuzz tests in total. 