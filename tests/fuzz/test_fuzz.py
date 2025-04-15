"""Property-based fuzz testing for Nomenic Core components.

This module uses Hypothesis to generate random but structured input for testing
the lexer and parser's robustness against varied inputs.
"""

import string

from hypothesis import given, settings
from hypothesis import strategies as st
from nomenic.ast import DocumentNode
from nomenic.errors import LexerError, ParserError
from nomenic.lexer import tokenize
from nomenic.parser import Parser, parse

# Define strategies for generating Nomenic document content

# Basic text content strategies
text_content = st.text(
    alphabet=string.ascii_letters + string.digits + string.punctuation + " \t",
    min_size=0,
    max_size=100,
)

# Simple line content
simple_line = st.text(
    alphabet=string.ascii_letters + string.digits + string.punctuation + " \t",
    min_size=0,
    max_size=80,
).filter(lambda s: "\n" not in s)

# Indentation strategy (0, 2, 4, or 6 spaces)
indentation = st.sampled_from(["", "  ", "    ", "      "])

# Block type strategy
block_types = st.sampled_from(
    [
        "meta:",
        "header:",
        "text:",
        "list:",
        "code:",
        "table:",
        "note:",
        "warn:",
        "blockquote:",
        "figure:",
        "def-list:",
        "x-custom:",
    ]
)

# Generate a valid block line


@st.composite
def block_line(draw):
    indent = draw(indentation)
    block_type = draw(block_types)
    content = draw(simple_line)
    return f"{indent}{block_type} {content}"


# Generate a list item


@st.composite
def list_item(draw):
    indent = draw(indentation)
    content = draw(simple_line)
    return f"{indent}- {content}"


# Generate a row item for tables


@st.composite
def row_item(draw):
    indent = draw(indentation)
    content = draw(simple_line)
    return f"{indent}- row: {content}"


# Generate a block with multiple parts


@st.composite
def multi_part_block(draw):
    indent = draw(indentation)
    block_type = draw(st.sampled_from(["def-list:", "figure:"]))
    lines = [f"{indent}{block_type}"]

    # For def-list, add dt and dd pairs
    if block_type == "def-list:":
        for _ in range(draw(st.integers(min_value=1, max_value=3))):
            term = draw(simple_line)
            definition = draw(simple_line)
            lines.append(f"{indent}dt: {term}")
            lines.append(f"{indent}dd: {definition}")

    # For figure, add src and caption
    elif block_type == "figure:":
        src = draw(simple_line)
        caption = draw(simple_line)
        lines.append(f"{indent}  src: {src}")
        lines.append(f"{indent}  caption: {caption}")

    return "\n".join(lines)


# Generate a complete Nomenic document


@st.composite
def nomenic_document(draw):
    # Start with meta block
    doc_parts = [
        "meta: version=1.0.0, author=FuzzTest",
        "header: Generated Test Document",
    ]

    # Add a random number of blocks
    num_blocks = draw(st.integers(min_value=0, max_value=10))
    for _ in range(num_blocks):
        block_choice = draw(st.integers(min_value=0, max_value=5))

        if block_choice == 0:
            # Simple block
            doc_parts.append(draw(block_line()))
        elif block_choice == 1:
            # List block
            block = ["list:"]
            num_items = draw(st.integers(min_value=1, max_value=5))
            for _ in range(num_items):
                block.append(draw(list_item()))
            doc_parts.append("\n".join(block))
        elif block_choice == 2:
            # Table block
            block = ["table:"]
            num_rows = draw(st.integers(min_value=1, max_value=3))
            for _ in range(num_rows):
                block.append(draw(row_item()))
            doc_parts.append("\n".join(block))
        elif block_choice == 3:
            # Multi-line text block
            indent = draw(indentation)
            content = draw(text_content)
            block = [f"{indent}text:", f"{indent}>>>", content, f"{indent}<<<"]
            doc_parts.append("\n".join(block))
        elif block_choice == 4:
            # Code block
            indent = draw(indentation)
            content = draw(text_content)
            # Format content as code with proper indentation
            formatted_content = "\n".join(
                f"{indent}  {line}" for line in content.split("\n")
            )
            block = [f"{indent}code:", formatted_content]
            doc_parts.append("\n".join(block))
        elif block_choice == 5:
            # Complex multi-part block
            doc_parts.append(draw(multi_part_block()))

    return "\n".join(doc_parts)


# Tests
@settings(max_examples=100, deadline=None)
@given(document=nomenic_document())
def test_lexer_parser_with_valid_documents(document):
    """Test that generated valid documents can be lexed and parsed without raising exceptions."""
    try:
        # First tokenize
        tokens = tokenize(document)

        # Then try to parse
        result = parse(tokens)

        # Verify we got a document node
        assert isinstance(result, DocumentNode)

        # Validate the document
        parser = Parser(tokens)
        validation_errors = parser.validate_document(result)

        # We may have validation errors, but lexer and parser should handle them
        # without crashing

    except (LexerError, ParserError) as e:
        # If we get here with a LexerError or ParserError, it should be well-formed
        # i.e., have a message and position information
        assert e.args[0], "Error message should not be empty"

        # This is just a validation test to ensure error handling is robust
        # We don't fail the test on expected errors, just check they're handled properly
        pass


@settings(max_examples=50, deadline=None)
@given(st.text())
def test_lexer_parser_with_arbitrary_text(text):
    """Test that arbitrary text input doesn't crash the lexer or parser."""
    try:
        # Try to tokenize arbitrary text
        tokens = tokenize(text)

        # Try to parse the tokens
        result = parse(tokens)

        # If we get here, make sure we have a DocumentNode
        assert isinstance(result, DocumentNode)

    except (LexerError, ParserError) as e:
        # Even for arbitrary text, errors should be well-formed
        assert e.args[0], "Error message should not be empty"

        # Again, we don't fail the test on expected errors,
        # just check they're handled properly


@settings(max_examples=20, deadline=None)
@given(document=nomenic_document())
def test_ast_normalization_optimization(document):
    """Test that AST normalization and optimization work on generated documents."""
    try:
        # Generate tokens and parse them
        tokens = tokenize(document)
        ast = parse(tokens)

        # Test normalization (should not raise exceptions)
        normalized = ast.normalize()
        assert isinstance(normalized, DocumentNode)

        # Test optimization (should not raise exceptions)
        optimized = normalized.optimize()
        assert isinstance(optimized, DocumentNode)

    except (LexerError, ParserError) as e:
        # Expected errors should be well-formed
        assert e.args[0], "Error message should not be empty"
