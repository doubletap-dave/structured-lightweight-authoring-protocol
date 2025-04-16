"""File operations and context utilities for Nomenic debugging."""

from pathlib import Path
from typing import Dict, List, Union


def read_file(file_path: Union[str, Path]) -> str:
    """
    Read file content safely for debugging purposes.

    Args:
        file_path: Path to the file to read

    Returns:
        File content as a string

    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be read
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    try:
        return file_path.read_text()
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")
    except UnicodeDecodeError:
        raise ValueError(f"Could not decode file as text: {file_path}")


def get_line_context(
    content: str,
    line_number: int,
    context_lines: int = 2,
    highlight: bool = True,
) -> Dict[str, Union[List[str], int]]:
    """
    Get context lines around a specific line in content.

    Args:
        content: The text content
        line_number: The 1-indexed line number to get context for
        context_lines: Number of lines before and after to include
        highlight: Whether to highlight the specified line

    Returns:
        Dictionary with context information

    Raises:
        ValueError: If line_number is out of range
    """
    lines = content.splitlines()

    if not 1 <= line_number <= len(lines):
        raise ValueError(f"Line number {line_number} out of range (1-{len(lines)})")

    # Convert to 0-indexed
    line_idx = line_number - 1

    # Get context lines
    start_idx = max(0, line_idx - context_lines)
    end_idx = min(len(lines), line_idx + context_lines + 1)
    context = lines[start_idx:end_idx]

    # Add line numbers and highlighting
    numbered_context = []
    for i, line in enumerate(context):
        line_num = start_idx + i + 1  # Convert back to 1-indexed
        if line_num == line_number and highlight:
            numbered_context.append(f"-> {line_num}: {line}")
        else:
            numbered_context.append(f"   {line_num}: {line}")

    return {
        "lines": numbered_context,
        "start_line": start_idx + 1,  # Convert back to 1-indexed
        "target_line": line_number,
        "raw_lines": context,
    }


def find_test_fixtures() -> Dict[str, List[Path]]:
    """
    Find test fixture files in the standard test locations.

    Returns:
        Dictionary mapping fixture types to lists of file paths
    """
    fixture_dirs = {
        "sample": Path("tests/fixtures"),
        "unit": Path("tests/unit"),
        "fuzz": Path("tests/fuzz"),
    }

    result = {}

    for fixture_type, directory in fixture_dirs.items():
        if directory.exists() and directory.is_dir():
            # Find files with .nmc extension
            nmc_files = list(directory.glob("**/*.nmc"))

            # Find test files with test_ prefix
            test_files = list(directory.glob("**/test_*.py"))

            # Store in result if any files found
            if nmc_files or test_files:
                result[fixture_type] = {
                    "nmc_files": nmc_files,
                    "test_files": test_files,
                }

    return result


def load_sample(name: str) -> str:
    """
    Load a named sample from the samples directory.

    Args:
        name: The name of the sample to load

    Returns:
        Content of the sample file

    Raises:
        FileNotFoundError: If the sample file does not exist
    """
    # Look in standard locations for sample files
    sample_dirs = [
        Path("tests/fixtures"),
        Path("samples"),
        Path("tests/samples"),
    ]

    # Try each directory
    for directory in sample_dirs:
        if not directory.exists():
            continue

        # Look for exact name match
        sample_path = directory / f"{name}.nmc"
        if sample_path.exists():
            return read_file(sample_path)

        # Look for any file containing the name
        for file_path in directory.glob("*.nmc"):
            if name.lower() in file_path.stem.lower():
                return read_file(file_path)

    raise FileNotFoundError(f"Sample not found: {name}")


def list_fixtures() -> List[Dict[str, Union[str, int]]]:
    """
    List available fixture files with brief descriptions.

    Returns:
        List of fixture information dictionaries
    """
    fixtures = find_test_fixtures()
    result = []

    for fixture_type, fixture_data in fixtures.items():
        for file_type, files in fixture_data.items():
            for file_path in files:
                file_info = {
                    "type": fixture_type,
                    "file_type": file_type,
                    "name": file_path.stem,
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                }

                # Try to extract a description from the file
                try:
                    content = read_file(file_path)
                    lines = content.splitlines()

                    # For Python files, look for docstring
                    if file_path.suffix == ".py" and len(lines) > 1:
                        if lines[0].startswith('"""') or lines[0].startswith("'''"):
                            file_info["description"] = lines[0].strip("\"'")

                    # For NMC files, look for header: or text: in the first 5 lines
                    elif file_path.suffix == ".nmc" and len(lines) > 1:
                        for line in lines[:5]:
                            if line.startswith("header:") or line.startswith("text:"):
                                file_info["description"] = line
                                break
                except:
                    # Ignore errors when trying to extract descriptions
                    pass

                result.append(file_info)

    return result
