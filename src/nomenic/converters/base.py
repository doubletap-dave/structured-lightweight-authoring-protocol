"""Base converter class for transforming between Nomenic and other formats."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .. import Lexer, Parser
from ..ast import ASTNode


class FormatConverter(ABC):
    """Base class for format converters.

    This class defines the interface for converting between Nomenic format
    and other document formats. All converters must implement these methods.
    """

    @abstractmethod
    def to_nomenic(self, source: str, **options) -> str:
        """Convert from source format to Nomenic.

        Args:
            source: Source document in the target format
            **options: Additional conversion options

        Returns:
            Nomenic document as a string
        """
        pass

    @abstractmethod
    def from_nomenic(self, nomenic: str, **options) -> str:
        """Convert from Nomenic to target format.

        Args:
            nomenic: Nomenic document as a string
            **options: Additional conversion options

        Returns:
            Document in the target format
        """
        pass

    def _parse_nomenic(self, content: str) -> ASTNode:
        """Parse Nomenic content into an AST.

        This is a helper method that converters can use to parse Nomenic
        content into an AST for processing.

        Args:
            content: Nomenic document as a string

        Returns:
            ASTNode representing the parsed document
        """
        lexer = Lexer(content)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def _detect_format(self, content: str) -> Optional[str]:
        """Detect the format of a document based on its content.

        This is a helper method that converters can use to detect the
        format of a document based on its content. This is useful when
        the format is not explicitly specified.

        Args:
            content: Document content as a string

        Returns:
            Detected format as a string, or None if format cannot be determined
        """
        # Check for common format markers
        if content.startswith("---\n") and "\n---\n" in content:
            return "yaml"  # YAML frontmatter
        elif content.startswith("{"):
            return "json"  # JSON object
        elif any(marker in content for marker in ["# ", "## ", "### "]):
            return "md"  # Markdown headers
        return None

    def extract_metadata(self, source: str) -> Dict[str, Any]:
        """Extract metadata from source content.

        Args:
            source: Source content

        Returns:
            Dictionary of metadata
        """
        # Default implementation returns empty metadata
        return {}

    def apply_metadata(self, content: str, metadata: Dict[str, Any]) -> str:
        """Apply metadata to content.

        Args:
            content: Target content
            metadata: Metadata to apply

        Returns:
            Content with metadata applied
        """
        # Default implementation returns unmodified content
        return content

    def partial_convert(self,
                        source: str,
                        section: Optional[str] = None,
                        from_nomenic: bool = False,
                        **options) -> str:
        """Convert a section of content.

        Args:
            source: Source content
            section: Section identifier to convert (if None, convert all)
            from_nomenic: If True, convert from Nomenic to target format
            **options: Additional conversion options

        Returns:
            Converted content
        """
        # Default implementation converts the entire content
        if from_nomenic:
            return self.from_nomenic(source)
        else:
            return self.to_nomenic(source)
