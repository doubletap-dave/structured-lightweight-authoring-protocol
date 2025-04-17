"""
Schema validation system for Nomenic documents.

This module provides a flexible and extensible schema validation system that allows
users to define and enforce document structure rules.
"""

from typing import Any, Dict, List, Optional, Type, Union
from dataclasses import dataclass
from enum import Enum, auto
import re  # for pattern validation


class ValidationLevel(Enum):
    """Levels of validation strictness."""
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


@dataclass
class ValidationResult:
    """Result of a validation check."""
    level: ValidationLevel
    message: str
    path: List[str]
    context: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        path_str = ".".join(self.path) if self.path else "<root>"
        return f"{self.level.name}: {self.message} at {path_str}"
    
    def __repr__(self) -> str:
        return str(self)

    def to_dict(self) -> Dict[str, Any]:
        """Return the validation result as a dictionary for custom formatting."""
        return {
            "level": self.level.name,
            "message": self.message,
            "path": self.path,
            "context": self.context
        }


class SchemaValidator:
    """Base class for schema validators."""

    def validate(self, node: Any) -> List[ValidationResult]:
        """Validate a node against the schema rules."""
        raise NotImplementedError


class TypeValidator(SchemaValidator):
    """Validates node types."""

    def __init__(self, expected_type: Type):
        self.expected_type = expected_type

    def validate(self, node: Any) -> List[ValidationResult]:
        if not isinstance(node, self.expected_type):
            return [ValidationResult(
                ValidationLevel.ERROR,
                f"Expected type {self.expected_type.__name__}, got {type(node).__name__}",
                []
            )]
        return []


class RequiredFieldValidator(SchemaValidator):
    """Validates required fields in a node."""

    def __init__(self, required_fields: List[str]):
        self.required_fields = required_fields

    def validate(self, node: Dict) -> List[ValidationResult]:
        results = []
        for field in self.required_fields:
            if field not in node:
                results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Missing required field: {field}",
                    []
                ))
        return results


class PatternValidator(SchemaValidator):
    """Validates that a value matches a given regular expression pattern."""

    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def validate(self, node: Any) -> List[ValidationResult]:
        if not isinstance(node, str) or not self.pattern.fullmatch(node):
            return [ValidationResult(
                ValidationLevel.ERROR,
                f"Value '{node}' does not match pattern '{self.pattern.pattern}'",
                []
            )]
        return []


class ArrayValidator(SchemaValidator):
    """Validates each element in a list using a provided validator."""

    def __init__(self, element_validator: SchemaValidator):
        self.element_validator = element_validator

    def validate(self, node: Any) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        if not isinstance(node, list):
            return [ValidationResult(
                ValidationLevel.ERROR,
                f"Expected list, got {type(node).__name__}",
                []
            )]
        for index, item in enumerate(node):
            sub_results = self.element_validator.validate(item)
            for res in sub_results:
                # prepend index to the error path
                res.path.insert(0, str(index))
                results.append(res)
        return results


class Schema:
    """Main schema definition class."""

    def __init__(self):
        self.validators: List[SchemaValidator] = []
        self.rules: Dict[str, List[SchemaValidator]] = {}

    def add_validator(self, validator: SchemaValidator) -> None:
        """Add a global validator to the schema."""
        self.validators.append(validator)

    def add_rule(self, path: str, validator: SchemaValidator) -> None:
        """Add a validator for a specific path in the document."""
        if path not in self.rules:
            self.rules[path] = []
        self.rules[path].append(validator)

    def validate(self, document: Any) -> List[ValidationResult]:
        """Validate a document against the schema."""
        results = []

        # Apply global validators
        for validator in self.validators:
            results.extend(validator.validate(document))

        # Apply path-specific validators (supports wildcard '*' for lists)
        for path, validators in self.rules.items():
            if '*' in path:
                prefix = path.split('.*')[0] if '.*' in path else path.split('*')[0].rstrip('.')
                list_node = self._get_node_at_path(document, prefix)
                if isinstance(list_node, list):
                    for idx, item in enumerate(list_node):
                        for validator in validators:
                            sub = validator.validate(item)
                            for res in sub:
                                # prepend index in the error path
                                res.path.insert(0, str(idx))
                                results.append(res)
            else:
                node = self._get_node_at_path(document, path)
                if node is not None:
                    for validator in validators:
                        results.extend(validator.validate(node))

        return results

    def _get_node_at_path(self, document: Any, path: str) -> Optional[Any]:
        """Get a node at a specific path in the document."""
        parts = path.split('.')
        current = document

        for part in parts:
            if isinstance(current, dict):
                if part not in current:
                    return None
                current = current[part]
            elif isinstance(current, list):
                try:
                    index = int(part)
                    if 0 <= index < len(current):
                        current = current[index]
                    else:
                        return None
                except ValueError:
                    return None
            else:
                return None

        return current


# Example usage:
"""
schema = Schema()
schema.add_validator(TypeValidator(dict))
schema.add_rule("metadata", RequiredFieldValidator(["title", "author"]))
schema.add_rule("metadata.title", TypeValidator(str))

results = schema.validate(document)
for result in results:
    print(f"{result.level.name}: {result.message} at {'.'.join(result.path)}")
"""
