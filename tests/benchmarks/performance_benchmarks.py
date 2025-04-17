"""Performance benchmarks for Nomenic Core components.

This module contains benchmarks for measuring the performance of the lexer and parser.
It uses the pytest-benchmark package for timing and statistics.
"""

import os
import random
import string
from pathlib import Path
from typing import Any

import pytest

from nomenic.lexer import tokenize
from nomenic.parser import parse

# Constants - adjusted for more realistic test sizes
SMALL_DOC_SIZE = 500  # ~0.5KB
MEDIUM_DOC_SIZE = 2_000  # ~2KB
LARGE_DOC_SIZE = 5_000  # ~5KB
VERY_LARGE_DOC_SIZE = 10_000  # ~10KB

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
BENCHMARK_DIR = Path(__file__).parent / "benchmark_data"


# Helper functions
def generate_random_text(length: int) -> str:
    """Generate random text of specified length without whitespace characters."""
    allowed = string.ascii_letters + string.digits + ".,!?"  # exclude spaces, tabs, newlines
    return "".join(random.choice(allowed) for _ in range(length))


def generate_nomenic_doc(size: int) -> str:
    """Generate a Nomenic document of approximately the specified size."""
    doc_parts = [
        "meta: version=1.0.0, author=BenchmarkGenerator\n",
        "header: Performance Benchmark Document\n",
        f"text: Generated document with approximately {size} characters\n",
    ]

    # Generate sections with random content to reach the target size
    current_size = sum(len(part) for part in doc_parts)
    section_count = 1

    while current_size < size:
        # Add a section
        section_name = f"Benchmark Section {section_count}"
        doc_parts.append(f"header: {section_name}\n")

        # Add some text content - keep text blocks smaller
        text_size = min(random.randint(50, 200), size - current_size)
        if text_size > 0:
            doc_parts.append("text:\n>>>\n")
            doc_parts.append(generate_random_text(text_size))
            doc_parts.append("\n<<<\n")

        # Add a list - limit list items
        doc_parts.append("list:\n")
        list_items = random.randint(1, 3)
        for i in range(list_items):
            doc_parts.append(f"- List item {i+1} with some text\n")

        # Maybe add a code block
        if random.random() > 0.7:
            doc_parts.append("code:\n")
            doc_parts.append("  def example():\n")
            doc_parts.append("      return 'Hello, world!'\n")

        # Update size tracking
        current_size = sum(len(part) for part in doc_parts)
        section_count += 1

    return "".join(doc_parts)


def ensure_benchmark_dir() -> None:
    """Ensure the benchmark directory exists."""
    os.makedirs(BENCHMARK_DIR, exist_ok=True)


def get_or_create_benchmark_file(size: int) -> str:
    """Generate and return the content of a benchmark file."""
    ensure_benchmark_dir()
    file_path = BENCHMARK_DIR / f"benchmark_{size}.nmc"
    print(f"Generating benchmark file: {file_path}")
    content = generate_nomenic_doc(size)
    file_path.write_text(content)
    return content


# Benchmarks
@pytest.mark.benchmark(group="lexer")
def test_lexer_small(benchmark: Any) -> None:
    """Benchmark the lexer with a small document (~0.5KB)."""
    content = get_or_create_benchmark_file(SMALL_DOC_SIZE)
    benchmark(tokenize, content)


@pytest.mark.benchmark(group="lexer")
def test_lexer_medium(benchmark: Any) -> None:
    """Benchmark the lexer with a medium document (~2KB)."""
    content = get_or_create_benchmark_file(MEDIUM_DOC_SIZE)
    benchmark(tokenize, content)


@pytest.mark.benchmark(group="lexer")
def test_lexer_large(benchmark: Any) -> None:
    """Benchmark the lexer with a large document (~5KB)."""
    content = get_or_create_benchmark_file(LARGE_DOC_SIZE)
    benchmark(tokenize, content)


@pytest.mark.benchmark(group="parser")
def test_parser_small(benchmark: Any) -> None:
    """Benchmark the parser with a small document (~0.5KB)."""
    content = get_or_create_benchmark_file(SMALL_DOC_SIZE)
    tokens = tokenize(content)
    benchmark(parse, tokens)


@pytest.mark.benchmark(group="parser")
def test_parser_medium(benchmark: Any) -> None:
    """Benchmark the parser with a medium document (~2KB)."""
    content = get_or_create_benchmark_file(MEDIUM_DOC_SIZE)
    tokens = tokenize(content)
    benchmark(parse, tokens)


@pytest.mark.benchmark(group="parser")
def test_parser_large(benchmark: Any) -> None:
    """Benchmark the parser with a large document (~5KB)."""
    content = get_or_create_benchmark_file(LARGE_DOC_SIZE)
    tokens = tokenize(content)
    benchmark(parse, tokens)


@pytest.mark.benchmark(group="end-to-end")
def test_end_to_end_small(benchmark: Any) -> None:
    """Benchmark end-to-end processing (lexer + parser) with a small document."""
    content = get_or_create_benchmark_file(SMALL_DOC_SIZE)

    def process_complete() -> None:
        tokens = tokenize(content)
        parse(tokens)

    benchmark(process_complete)


@pytest.mark.benchmark(group="end-to-end")
def test_end_to_end_medium(benchmark: Any) -> None:
    """Benchmark end-to-end processing (lexer + parser) with a medium document."""
    content = get_or_create_benchmark_file(MEDIUM_DOC_SIZE)

    def process_complete() -> None:
        tokens = tokenize(content)
        parse(tokens)

    benchmark(process_complete)


# Memory usage benchmarks
def test_memory_usage() -> None:
    """Test memory usage for processing documents of various sizes."""
    import tracemalloc

    results = []

    for size in [SMALL_DOC_SIZE, MEDIUM_DOC_SIZE, LARGE_DOC_SIZE]:
        content = get_or_create_benchmark_file(size)

        # Measure lexer memory usage
        tracemalloc.start()
        tokens = tokenize(content)
        lexer_current, lexer_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Measure parser memory usage
        tracemalloc.start()
        parse(tokens)
        parser_current, parser_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results.append(
            {
                "size": size,
                "lexer_peak_kb": lexer_peak / 1024,
                "parser_peak_kb": parser_peak / 1024,
                "total_peak_kb": (lexer_peak + parser_peak) / 1024,
            }
        )

    # Print results in a readable format
    print("\nMemory Usage Results:")
    print("=====================")
    print(
        f"{'Size (chars)':<15} {'Lexer Peak (KB)':<20} {'Parser Peak (KB)':<20} {'Total (KB)':<15}"
    )
    for r in results:
        print(
            f"{r['size']:<15} {r['lexer_peak_kb']:<20.2f} {r['parser_peak_kb']:<20.2f} {r['total_peak_kb']:<15.2f}"
        )
