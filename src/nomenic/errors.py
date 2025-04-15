# Nomenic Core - Custom Exceptions

class NomenicError(Exception):
    """Base class for Nomenic parsing/lexing errors."""
    pass

class LexerError(NomenicError):
    """Error during the lexing phase."""
    pass

class ParserError(NomenicError):
    """Error during the parsing phase."""
    pass

class ValidationError(NomenicError):
    """Error raised when content or schema validation fails."""
    pass

class MigrationError(NomenicError):
    """Error raised during migration/version upgrade processes."""
    pass

class ExtensionError(NomenicError):
    """Error raised when handling custom or unsafe extensions."""
    pass 