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