"""Tests for the Nomenic extension API."""

import pytest
from typing import Any, Dict, List, Type
from nomenic.extensions.base import (
    Extension,
    ExtensionMetadata,
    ValidatorExtension,
    RendererExtension,
    ConverterExtension,
    ExtensionManager
)
from nomenic.validation.schema import SchemaValidator


class TestValidator(SchemaValidator):
    """Test validator for testing the extension API."""

    def validate(self, node: Any) -> List[Any]:
        return []


class TestRenderer:
    """Test renderer for testing the extension API."""
    pass


class TestConverter:
    """Test converter for testing the extension API."""
    pass


class TestValidatorExtension(ValidatorExtension):
    """Test validator extension."""

    def get_metadata(self) -> ExtensionMetadata:
        return ExtensionMetadata(
            name="test-validator",
            version="1.0.0",
            description="Test validator extension",
            author="Test Author"
        )

    def get_validators(self) -> Dict[str, Type[SchemaValidator]]:
        return {"test_validator": TestValidator}


class TestRendererExtension(RendererExtension):
    """Test renderer extension."""

    def get_metadata(self) -> ExtensionMetadata:
        return ExtensionMetadata(
            name="test-renderer",
            version="1.0.0",
            description="Test renderer extension",
            author="Test Author"
        )

    def get_renderers(self) -> Dict[str, Type[TestRenderer]]:
        return {"test_renderer": TestRenderer}


class TestConverterExtension(ConverterExtension):
    """Test converter extension."""

    def get_metadata(self) -> ExtensionMetadata:
        return ExtensionMetadata(
            name="test-converter",
            version="1.0.0",
            description="Test converter extension",
            author="Test Author"
        )

    def get_converters(self) -> Dict[str, Type[TestConverter]]:
        return {"test_converter": TestConverter}


class TestDependentExtension(ValidatorExtension):
    """Test extension with dependencies."""

    def get_metadata(self) -> ExtensionMetadata:
        return ExtensionMetadata(
            name="test-dependent",
            version="1.0.0",
            description="Test dependent extension",
            author="Test Author",
            dependencies=["test-validator"]
        )

    def get_validators(self) -> Dict[str, Type[SchemaValidator]]:
        return {"dependent_validator": TestValidator}


def test_extension_metadata():
    """Test the ExtensionMetadata class."""
    metadata = ExtensionMetadata(
        name="test",
        version="1.0.0",
        description="Test extension",
        author="Test Author"
    )

    assert metadata.name == "test"
    assert metadata.version == "1.0.0"
    assert metadata.description == "Test extension"
    assert metadata.author == "Test Author"
    assert metadata.dependencies is None


def test_extension_manager():
    """Test the ExtensionManager class."""
    manager = ExtensionManager()

    # Test loading extensions
    validator_ext = TestValidatorExtension()
    renderer_ext = TestRendererExtension()
    converter_ext = TestConverterExtension()

    manager.load_extension(validator_ext)
    manager.load_extension(renderer_ext)
    manager.load_extension(converter_ext)

    assert len(manager.extensions) == 3
    assert len(manager.validators) == 1
    assert len(manager.renderers) == 1
    assert len(manager.converters) == 1

    # Test getting components
    assert manager.get_validator("test_validator") == TestValidator
    assert manager.get_renderer("test_renderer") == TestRenderer
    assert manager.get_converter("test_converter") == TestConverter

    # Test unloading extensions
    manager.unload_extension("test-validator")
    assert len(manager.extensions) == 2
    assert len(manager.validators) == 0

    # Test getting non-existent components
    assert manager.get_validator("test_validator") is None


def test_extension_dependencies():
    """Test extension dependency handling."""
    manager = ExtensionManager()

    # Test loading dependent extension without dependency
    dependent_ext = TestDependentExtension()
    with pytest.raises(ValueError) as excinfo:
        manager.load_extension(dependent_ext)
    assert "Missing dependency: test-validator" in str(excinfo.value)

    # Test loading with dependency
    validator_ext = TestValidatorExtension()
    manager.load_extension(validator_ext)
    manager.load_extension(dependent_ext)

    assert len(manager.extensions) == 2
    assert len(manager.validators) == 2

    # Test unloading dependency while dependent is loaded
    with pytest.raises(ValueError) as excinfo:
        manager.unload_extension("test-validator")
    assert "Cannot unload test-validator: test-dependent depends on it" in str(
        excinfo.value)

    # Test unloading dependent first
    manager.unload_extension("test-dependent")
    manager.unload_extension("test-validator")
    assert len(manager.extensions) == 0
    assert len(manager.validators) == 0


def test_extension_initialization():
    """Test extension initialization and cleanup."""
    class TestInitExtension(Extension):
        def __init__(self):
            self.initialized = False
            self.cleaned_up = False
            super().__init__()

        def get_metadata(self) -> ExtensionMetadata:
            return ExtensionMetadata(
                name="test-init",
                version="1.0.0",
                description="Test initialization extension",
                author="Test Author"
            )

        def initialize(self) -> None:
            self.initialized = True

        def cleanup(self) -> None:
            self.cleaned_up = True

    manager = ExtensionManager()
    ext = TestInitExtension()

    assert not ext.initialized
    assert not ext.cleaned_up

    manager.load_extension(ext)
    assert ext.initialized
    assert not ext.cleaned_up

    manager.unload_extension("test-init")
    assert ext.initialized
    assert ext.cleaned_up
