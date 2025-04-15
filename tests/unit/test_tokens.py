"""Tests for the Nomenic Core tokens module."""

from src.nomenic.tokens import Token, TokenType

# Constants for magic numbers
TEST_LINE_NUMBER = 5
TEST_COLUMN_NUMBER = 10


def test_token_creation():
    """Test that tokens can be created with correct values."""
    token = Token(TokenType.HEADER, "Test Header", 1, 0)
    assert token.type == TokenType.HEADER
    assert token.value == "Test Header"
    assert token.line == 1
    assert token.column == 0


def test_token_str_representation():
    """Test the string representation of tokens."""
    token = Token(TokenType.HEADER, "Test Header", 1, 0)
    expected_str = (
        "Token(type=TokenType.HEADER, value='Test Header', line=1, column=0, "
        "indent_level=0, metadata=None)"
    )
    assert str(token) == expected_str


def test_token_equality():
    """Test token equality comparison."""
    token1 = Token(TokenType.HEADER, "Test Header", 1, 0)
    token2 = Token(TokenType.HEADER, "Test Header", 1, 0)
    token3 = Token(TokenType.TEXT, "Test Header", 1, 0)

    assert token1 == token2
    assert token1 != token3


def test_token_type_enum():
    """Test that all expected token types exist."""
    actual_types = set(TokenType.__members__.keys())
    assert len(actual_types) > 0
    assert "HEADER" in actual_types
    assert "EOF" in actual_types
    assert "LIST_ITEM" in actual_types


def test_token_position():
    """Test that token positions are correctly tracked."""
    token = Token(TokenType.HEADER, "Test Header", TEST_LINE_NUMBER, TEST_COLUMN_NUMBER)
    assert token.line == TEST_LINE_NUMBER
    assert token.column == TEST_COLUMN_NUMBER


def test_token_value_types():
    """Test that tokens can handle different value types."""
    # String value
    str_token = Token(TokenType.TEXT, "string value", 1, 0)
    assert isinstance(str_token.value, str)

    # List value (Metadata can hold complex values, using META type as example)
    list_val = ["item1", "item2"]
    list_token = Token(TokenType.META, list_val, 1, 0)
    assert isinstance(list_token.value, list)

    # Dict value (Metadata can hold complex values, using META type as example)
    dict_val = {"key": "value"}
    dict_token = Token(TokenType.META, dict_val, 1, 0)
    assert isinstance(dict_token.value, dict)

    # None value (EOF has None value)
    none_token = Token(TokenType.EOF, None, 1, 0)
    assert none_token.value is None
