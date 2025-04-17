"""Tests for the schema validation system."""

import pytest
from typing import Any, Dict, List, Optional, Type
from nomenic.validation.schema import (
    Schema,
    SchemaValidator,
    TypeValidator,
    RequiredFieldValidator,
    ValidationLevel,
    ValidationResult,
    PatternValidator,
    ArrayValidator
)


def test_type_validator():
    """Test the TypeValidator class."""
    validator = TypeValidator(str)

    # Valid case
    assert validator.validate("test") == []

    # Invalid case
    results = validator.validate(123)
    assert len(results) == 1
    assert results[0].level == ValidationLevel.ERROR
    assert "Expected type str" in results[0].message


def test_required_field_validator():
    """Test the RequiredFieldValidator class."""
    validator = RequiredFieldValidator(["title", "author"])

    # Valid case
    assert validator.validate({"title": "Test", "author": "Me"}) == []

    # Missing one field
    results = validator.validate({"title": "Test"})
    assert len(results) == 1
    assert results[0].level == ValidationLevel.ERROR
    assert "Missing required field: author" in results[0].message

    # Missing both fields
    results = validator.validate({})
    assert len(results) == 2
    assert all(r.level == ValidationLevel.ERROR for r in results)
    assert any("Missing required field: title" in r.message for r in results)
    assert any("Missing required field: author" in r.message for r in results)


def test_schema_validation():
    """Test the Schema class with multiple validators."""
    schema = Schema()
    schema.add_validator(TypeValidator(dict))
    schema.add_rule("metadata", RequiredFieldValidator(["title", "author"]))
    schema.add_rule("metadata.title", TypeValidator(str))

    # Valid document
    valid_doc = {
        "metadata": {
            "title": "Test Document",
            "author": "Test Author"
        }
    }
    assert schema.validate(valid_doc) == []

    # Invalid document - wrong type
    invalid_type = "not a dict"
    results = schema.validate(invalid_type)
    assert len(results) == 1
    assert results[0].level == ValidationLevel.ERROR
    assert "Expected type dict" in results[0].message

    # Invalid document - missing required field
    missing_field = {
        "metadata": {
            "title": "Test Document"
        }
    }
    results = schema.validate(missing_field)
    assert len(results) == 1
    assert results[0].level == ValidationLevel.ERROR
    assert "Missing required field: author" in results[0].message

    # Invalid document - wrong field type
    wrong_type = {
        "metadata": {
            "title": 123,
            "author": "Test Author"
        }
    }
    results = schema.validate(wrong_type)
    assert len(results) == 1
    assert results[0].level == ValidationLevel.ERROR
    assert "Expected type str" in results[0].message


def test_schema_path_validation():
    """Test schema validation with nested paths."""
    schema = Schema()
    schema.add_rule("metadata.tags", TypeValidator(list))
    schema.add_rule("metadata.tags.*", TypeValidator(str))

    # Valid document
    valid_doc = {
        "metadata": {
            "tags": ["tag1", "tag2"]
        }
    }
    assert schema.validate(valid_doc) == []

    # Invalid document - wrong type at path
    invalid_type = {
        "metadata": {
            "tags": "not a list"
        }
    }
    results = schema.validate(invalid_type)
    assert len(results) == 1
    assert results[0].level == ValidationLevel.ERROR
    assert "Expected type list" in results[0].message

    # Invalid document - wrong type in list
    invalid_list = {
        "metadata": {
            "tags": ["tag1", 123]
        }
    }
    results = schema.validate(invalid_list)
    assert len(results) == 1
    assert results[0].level == ValidationLevel.ERROR
    assert "Expected type str" in results[0].message


def test_schema_validation_context():
    """Test that validation results include proper context."""
    validator = TypeValidator(str)
    results = validator.validate(123)
    assert len(results) == 1
    assert results[0].context is None  # Context is optional

    # Test with custom validator that includes context
    class ContextValidator(SchemaValidator):
        def validate(self, node: Any) -> List[ValidationResult]:
            return [ValidationResult(
                ValidationLevel.WARNING,
                "Test warning",
                [],
                {"value": node}
            )]

    validator = ContextValidator()
    results = validator.validate("test")
    assert len(results) == 1
    assert results[0].context == {"value": "test"}


def test_pattern_validator():
    """Test the PatternValidator class."""
    validator = PatternValidator(r"^\d{3}-\d{2}-\d{4}$")
    # Valid case
    assert validator.validate("123-45-6789") == []
    # Invalid case
    results = validator.validate("ABC")
    assert len(results) == 1
    assert results[0].level == ValidationLevel.ERROR
    assert "does not match pattern" in results[0].message


def test_array_validator():
    """Test the ArrayValidator class."""
    element_validator = TypeValidator(int)
    validator = ArrayValidator(element_validator)
    # Valid list
    assert validator.validate([1, 2, 3]) == []
    # Not a list
    results = validator.validate("not a list")
    assert len(results) == 1
    assert "Expected list" in results[0].message
    # Invalid element in list
    results = validator.validate([1, "a", 3])
    assert len(results) == 1
    assert results[0].path == ["1"]
    assert results[0].level == ValidationLevel.ERROR


def test_validation_result_to_dict():
    """Test ValidationResult.to_dict returns correct dict."""
    result = ValidationResult(ValidationLevel.WARNING, "msg", ["a", "b"], {"k": "v"})
    d = result.to_dict()
    assert d == {
        "level": "WARNING",
        "message": "msg",
        "path": ["a", "b"],
        "context": {"k": "v"}
    }
