"""Common test fixtures and configurations."""

from pathlib import Path

import pytest


@pytest.fixture
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_nmc_file(test_data_dir: Path) -> Path:
    """Return the path to a sample Nomenic Core file."""
    return test_data_dir / "sample.nmc"


@pytest.fixture
def invalid_nmc_file(test_data_dir: Path) -> Path:
    """Return the path to an invalid Nomenic Core file."""
    return test_data_dir / "invalid.nmc"


@pytest.fixture
def empty_nmc_file(test_data_dir: Path) -> Path:
    """Return the path to an empty Nomenic Core file."""
    return test_data_dir / "empty.nmc"
