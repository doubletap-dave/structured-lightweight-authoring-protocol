"""Base converter interface for format converters."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class FormatConverter(ABC):
    """Base interface for format converters.
    
    This abstract class defines the interface that all format converters must implement.
    Format converters provide bidirectional conversion between Nomenic and other formats.
    """
    
    @abstractmethod
    def to_nomenic(self, source: str, **options) -> str:
        """Convert from source format to Nomenic.
        
        Args:
            source: Content in source format
            **options: Additional conversion options
            
        Returns:
            Nomenic-formatted content
        """
        pass
        
    @abstractmethod
    def from_nomenic(self, nomenic: str, **options) -> str:
        """Convert from Nomenic to target format.
        
        Args:
            nomenic: Nomenic-formatted content
            **options: Additional conversion options
            
        Returns:
            Content in target format
        """
        pass
        
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
            return self.from_nomenic(source, **options)
        else:
            return self.to_nomenic(source, **options) 