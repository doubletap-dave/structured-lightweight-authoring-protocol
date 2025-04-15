import pytest
from src.nomenic.errors import NomenicError, LexerError, ParserError, ValidationError, MigrationError, ExtensionError

def test_nomenic_error_inheritance():
    assert issubclass(LexerError, NomenicError)
    assert issubclass(ParserError, NomenicError)
    assert issubclass(ValidationError, NomenicError)
    assert issubclass(MigrationError, NomenicError)
    assert issubclass(ExtensionError, NomenicError)

def test_error_instantiation():
    assert str(LexerError("msg")) == "msg"
    assert str(ParserError("msg")) == "msg"
    assert str(ValidationError("msg")) == "msg"
    assert str(MigrationError("msg")) == "msg"
    assert str(ExtensionError("msg")) == "msg" 