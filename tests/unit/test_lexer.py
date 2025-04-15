"""Tests for the Nomenic Core lexer."""

import pytest

from src.nomenic.errors import LexerError
from src.nomenic.lexer import Lexer
from src.nomenic.tokens import TokenType

# Constants for magic numbers
EXPECTED_MIN_LIST_ITEMS = 3
EXPECTED_MIN_CALLOUT_TOKENS = 3
EXPECTED_MIN_CUSTOM_TOKENS = 2
EXPECTED_MIN_STYLE_TOKENS = 4
EOF_TOKEN_COUNT = 1


def test_lexer_initialization():
    """Test that the lexer can be initialized."""
    lexer = Lexer("")
    assert lexer is not None
    assert lexer.content == ""
    assert lexer.lines == []
    assert lexer.line_idx == 0
    assert lexer.col_idx == 0


def test_lexer_tokenizes_meta(sample_nmc_file):
    """Test that the lexer correctly tokenizes meta information."""
    with open(sample_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Find meta tokens
    meta_tokens = [t for t in tokens if t.type == TokenType.META]
    assert len(meta_tokens) > 0
    assert any(t.value == "meta:" for t in meta_tokens)


def test_lexer_tokenizes_header(sample_nmc_file):
    """Test that the lexer correctly tokenizes headers."""
    with open(sample_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Find header tokens
    header_tokens = [t for t in tokens if t.type == TokenType.HEADER]
    assert len(header_tokens) > 0
    assert any(t.value == "header:" for t in header_tokens)


def test_lexer_tokenizes_list_items(sample_nmc_file):
    """Test that the lexer correctly tokenizes list items."""
    with open(sample_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Find list item tokens
    list_items = [t for t in tokens if t.type == TokenType.LIST_ITEM]
    assert len(list_items) >= EXPECTED_MIN_LIST_ITEMS
    assert any(t.value == "- " for t in list_items)


def test_lexer_tokenizes_code_blocks(sample_nmc_file):
    """Test that the lexer correctly tokenizes code blocks."""
    with open(sample_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Find code tokens
    code_tokens = [t for t in tokens if t.type == TokenType.CODE]
    assert len(code_tokens) > 0
    assert any("def hello_world():" in t.value for t in code_tokens)


def test_lexer_tokenizes_callouts(sample_nmc_file):
    """Test that the lexer correctly tokenizes callouts."""
    with open(sample_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Find callout tokens
    callout_tokens = [t for t in tokens if t.type == TokenType.CALLOUT]
    assert len(callout_tokens) >= EXPECTED_MIN_CALLOUT_TOKENS
    assert any(t.value == "note:" for t in callout_tokens)
    assert any(t.value == "warn:" for t in callout_tokens)
    assert any(t.value == "tip:" for t in callout_tokens)


def test_lexer_tokenizes_custom_directives(sample_nmc_file):
    """Test that the lexer correctly tokenizes custom directives."""
    with open(sample_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Find custom directive tokens
    custom_tokens = [t for t in tokens if t.type == TokenType.CUSTOM_DIRECTIVE]
    assert len(custom_tokens) >= EXPECTED_MIN_CUSTOM_TOKENS
    assert any(t.value == "x-custom:" for t in custom_tokens)
    assert any(t.value == "x-another:" for t in custom_tokens)


def test_lexer_tokenizes_inline_styles(sample_nmc_file):
    """Test that the lexer correctly tokenizes inline styles."""
    with open(sample_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    tokens = list(lexer.tokenize())

    # Find style tokens
    style_tokens = [
        t
        for t in tokens
        if t.type
        in (
            TokenType.STYLE_BOLD,
            TokenType.STYLE_ITALIC,
            TokenType.STYLE_CODE,
            TokenType.STYLE_LINK,
        )
    ]
    assert len(style_tokens) >= EXPECTED_MIN_STYLE_TOKENS
    assert any(t.type == TokenType.STYLE_BOLD for t in style_tokens)
    assert any(t.type == TokenType.STYLE_ITALIC for t in style_tokens)
    assert any(t.type == TokenType.STYLE_CODE for t in style_tokens)
    assert any(t.type == TokenType.STYLE_LINK for t in style_tokens)


def test_lexer_handles_invalid_indentation(invalid_nmc_file):
    """Test that the lexer correctly handles invalid indentation."""
    with open(invalid_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    with pytest.raises(LexerError, match="Invalid indentation"):
        list(lexer.tokenize())


def test_lexer_handles_invalid_list_syntax(invalid_nmc_file):
    """Test that the lexer correctly handles invalid list syntax."""
    # NOTE: This test might need adjustment based on how the lexer
    # handles list errors after refactoring.
    with open(invalid_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    with pytest.raises(LexerError):
        list(lexer.tokenize())


def test_lexer_handles_invalid_custom_directives(invalid_nmc_file):
    """Test that the lexer correctly handles invalid custom directives."""
    # NOTE: This test might need adjustment based on how the lexer
    # handles custom directive errors after refactoring.
    with open(invalid_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    with pytest.raises(LexerError):
        list(lexer.tokenize())


def test_lexer_handles_invalid_inline_styles(invalid_nmc_file):
    """Test that the lexer correctly handles invalid inline styles."""
    # NOTE: This test might need adjustment based on how the lexer
    # handles inline style errors after refactoring.
    with open(invalid_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    with pytest.raises(LexerError):
        list(lexer.tokenize())


def test_lexer_handles_empty_file(empty_nmc_file):
    """Test that the lexer correctly handles empty files."""
    with open(empty_nmc_file) as f:
        content = f.read()

    lexer = Lexer(content)
    tokens = list(lexer.tokenize())
    assert len(tokens) == EOF_TOKEN_COUNT  # Only EOF token
    assert tokens[0].type == TokenType.EOF
