"""
Base classes for the Nomenic extension API.

This module provides the foundation for creating custom extensions that can
enhance Nomenic's functionality with new validators, renderers, and converters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from dataclasses import dataclass
import importlib
import pkgutil
import inspect
from pathlib import Path


@dataclass
class ExtensionMetadata:
    """Metadata for an extension."""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str] = None


class Extension(ABC):
    """Base class for all Nomenic extensions."""

    def __init__(self):
        self.metadata = self.get_metadata()

    @abstractmethod
    def get_metadata(self) -> ExtensionMetadata:
        """Get the extension's metadata."""
        raise NotImplementedError

    def initialize(self) -> None:
        """Initialize the extension.

        This method is called when the extension is loaded. Override it to perform
        any necessary setup, such as registering custom validators or renderers.
        """
        pass

    def cleanup(self) -> None:
        """Clean up the extension.

        This method is called when the extension is unloaded. Override it to perform
        any necessary cleanup, such as unregistering custom components.
        """
        pass


class ValidatorExtension(Extension):
    """Base class for validator extensions."""

    @abstractmethod
    def get_validators(self) -> Dict[str, Type['SchemaValidator']]:
        """Get the custom validators provided by this extension.

        Returns:
            A dictionary mapping validator names to validator classes.
        """
        raise NotImplementedError


class RendererExtension(Extension):
    """Base class for renderer extensions."""

    @abstractmethod
    def get_renderers(self) -> Dict[str, Type['Renderer']]:
        """Get the custom renderers provided by this extension.

        Returns:
            A dictionary mapping renderer names to renderer classes.
        """
        raise NotImplementedError


class ConverterExtension(Extension):
    """Base class for converter extensions."""

    @abstractmethod
    def get_converters(self) -> Dict[str, Type['Converter']]:
        """Get the custom converters provided by this extension.

        Returns:
            A dictionary mapping converter names to converter classes.
        """
        raise NotImplementedError


class ExtensionManager:
    """Manages the loading and unloading of extensions."""

    def __init__(self):
        self.extensions: Dict[str, Extension] = {}
        self.validators: Dict[str, Type['SchemaValidator']] = {}
        self.renderers: Dict[str, Type['Renderer']] = {}
        self.converters: Dict[str, Type['Converter']] = {}

    def load_extension(self, extension: Extension) -> None:
        """Load an extension.

        Args:
            extension: The extension to load.
        """
        if extension.metadata.name in self.extensions:
            raise ValueError(
                f"Extension {extension.metadata.name} is already loaded")

        # Check dependencies
        if extension.metadata.dependencies:
            for dep in extension.metadata.dependencies:
                if dep not in self.extensions:
                    raise ValueError(f"Missing dependency: {dep}")

        # Initialize the extension
        extension.initialize()

        # Register components
        if isinstance(extension, ValidatorExtension):
            self.validators.update(extension.get_validators())
        if isinstance(extension, RendererExtension):
            self.renderers.update(extension.get_renderers())
        if isinstance(extension, ConverterExtension):
            self.converters.update(extension.get_converters())

        self.extensions[extension.metadata.name] = extension

    def unload_extension(self, name: str) -> None:
        """Unload an extension.

        Args:
            name: The name of the extension to unload.
        """
        if name not in self.extensions:
            raise ValueError(f"Extension {name} is not loaded")

        extension = self.extensions[name]

        # Check if other extensions depend on this one
        for ext in self.extensions.values():
            if (ext.metadata.dependencies and
                    name in ext.metadata.dependencies):
                raise ValueError(
                    f"Cannot unload {name}: {ext.metadata.name} depends on it"
                )

        # Clean up the extension
        extension.cleanup()

        # Unregister components
        if isinstance(extension, ValidatorExtension):
            for validator_name in extension.get_validators():
                self.validators.pop(validator_name, None)
        if isinstance(extension, RendererExtension):
            for renderer_name in extension.get_renderers():
                self.renderers.pop(renderer_name, None)
        if isinstance(extension, ConverterExtension):
            for converter_name in extension.get_converters():
                self.converters.pop(converter_name, None)

        del self.extensions[name]

    def get_extension(self, name: str) -> Optional[Extension]:
        """Get a loaded extension by name.

        Args:
            name: The name of the extension.

        Returns:
            The extension, or None if not found.
        """
        return self.extensions.get(name)

    def get_validator(self, name: str) -> Optional[Type['SchemaValidator']]:
        """Get a validator by name.

        Args:
            name: The name of the validator.

        Returns:
            The validator class, or None if not found.
        """
        return self.validators.get(name)

    def get_renderer(self, name: str) -> Optional[Type['Renderer']]:
        """Get a renderer by name.

        Args:
            name: The name of the renderer.

        Returns:
            The renderer class, or None if not found.
        """
        return self.renderers.get(name)

    def get_converter(self, name: str) -> Optional[Type['Converter']]:
        """Get a converter by name.

        Args:
            name: The name of the converter.

        Returns:
            The converter class, or None if not found.
        """
        return self.converters.get(name)

    def discover_extensions(self, package: str = 'nomenic.extensions') -> None:
        """Discover and load all Extension subclasses in the given package."""
        pkg = importlib.import_module(package)
        for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__):
            module_name = f"{package}.{name}"
            mod = importlib.import_module(module_name)
            for attr in dir(mod):
                cls = getattr(mod, attr)
                if inspect.isclass(cls) and issubclass(cls, Extension) and cls is not Extension and not inspect.isabstract(cls):
                    ext = cls()
                    self.load_extension(ext)

    def hot_reload(self, name: str) -> None:
        """Unload and reload the extension by name."""
        ext = self.get_extension(name)
        if not ext:
            raise ValueError(f"Extension {name} is not loaded")
        module_name = ext.__class__.__module__
        self.unload_extension(name)
        mod = importlib.reload(importlib.import_module(module_name))
        cls = getattr(mod, ext.__class__.__name__)
        new_ext = cls()
        self.load_extension(new_ext)
