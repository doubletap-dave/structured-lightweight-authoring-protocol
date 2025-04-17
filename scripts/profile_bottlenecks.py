#!/usr/bin/env python3
"""
Script to profile the end-to-end lexer+parser processing for a medium-sized document.
Generates profiling stats for the top cumulative functions.
"""
import cProfile
import pstats
import io
import importlib.util
import pathlib

from nomenic.lexer import tokenize
from nomenic.parser import parse

# Dynamically load benchmarking utilities from tests
bench_path = pathlib.Path(__file__).parent.parent / 'tests' / 'benchmarks' / 'performance_benchmarks.py'
spec = importlib.util.spec_from_file_location('perf_mod', str(bench_path))
perf_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(perf_mod)
generate_nomenic_doc = perf_mod.generate_nomenic_doc
MEDIUM_DOC_SIZE = perf_mod.MEDIUM_DOC_SIZE


def main():
    # Generate content for profiling
    content = generate_nomenic_doc(MEDIUM_DOC_SIZE)

    def process():
        tokens = tokenize(content)
        parse(tokens)

    # Profile end-to-end process
    profiler = cProfile.Profile()
    profiler.runcall(process)

    # Sort and print top 20 cumulative functions
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats('cumulative')
    stats.print_stats(20)
    print(stream.getvalue())


if __name__ == '__main__':
    main()
