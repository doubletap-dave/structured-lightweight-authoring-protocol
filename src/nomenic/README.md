# Nomenic Core Library

This directory contains the core implementation of the Nomenic Document Language (NDL) parser and related components.

## Package Structure

- **__init__.py** - Package initialization and public exports
- **tokens.py** - Token definitions and token class implementations
- **lexer.py** - Tokenization logic to convert raw text into token streams
- **parser.py** - Parse token streams into an Abstract Syntax Tree (AST)
- **ast.py** - AST node definitions and visitor pattern implementation
- **errors.py** - Custom exception classes for error handling

## Processing Pipeline

The Nomenic processing pipeline follows these steps:

1. **Lexing**: Converting raw text into a stream of tokens
   ```python
   from nomenic import tokenize
   tokens = tokenize("header: My Document")
   ```

2. **Parsing**: Converting tokens into an Abstract Syntax Tree
   ```python
   from nomenic import Lexer, parser
   lexer = Lexer("header: My Document")
   ast = parser.parse(lexer.tokenize())
   ```

3. **Validation**: Ensuring the document follows NDL specifications
   ```python
   # Validation is integrated into the parser
   ast = parser.parse(tokens, validate=True)
   ```

## Error Handling

Nomenic provides robust error handling with detailed error messages:

```python
from nomenic import Lexer, parser, LexerError, ParserError

try:
    lexer = Lexer(document_text)
    tokens = lexer.tokenize()
    ast = parser.parse(tokens)
except LexerError as e:
    print(f"Lexer error at line {e.line}, column {e.column}: {e.message}")
except ParserError as e:
    print(f"Parser error: {e}")
```

The parser also supports a non-exception error recording mode:

```python
from nomenic import Lexer, parser

lexer = Lexer(document_text)
tokens = lexer.tokenize()
ast = parser.parse(tokens, record_errors=True)

if ast.errors:
    for error in ast.errors:
        print(f"Error at {error.position}: {error.message}")
```

## AST Visitor Pattern

The AST nodes support the visitor pattern for traversal and transformation:

```python
from nomenic import ast

class MyVisitor(ast.Visitor):
    def visit_header(self, node):
        print(f"Found header: {node.content}")
        self.visit_children(node)

visitor = MyVisitor()
visitor.visit(document_ast)
```

## Development Status

The core components (lexer, parser, AST) are fully implemented and tested. Error handling, validation, and visitor pattern functionality are complete. The package is currently in Phase 3 (Testing & Validation) with 90% code coverage. 