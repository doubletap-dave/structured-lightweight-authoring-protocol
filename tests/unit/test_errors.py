from src.nomenic.errors import (
    ExtensionError,
    LexerError,
    MigrationError,
    NomenicError,
    ParserError,
    ValidationError,
)


def test_nomenic_error_inheritance():
    assert issubclass(LexerError, NomenicError)  # nosec B101
    assert issubclass(ParserError, NomenicError)  # nosec B101
    assert issubclass(ValidationError, NomenicError)  # nosec B101
    assert issubclass(MigrationError, NomenicError)  # nosec B101
    assert issubclass(ExtensionError, NomenicError)  # nosec B101


def test_error_instantiation():
    assert str(LexerError("msg")) == "msg"  # nosec B101
    assert str(ParserError("msg")) == "msg"  # nosec B101
    assert str(ValidationError("msg")) == "msg"  # nosec B101
    assert str(MigrationError("msg")) == "msg"  # nosec B101
    assert str(ExtensionError("msg")) == "msg"  # nosec B101
