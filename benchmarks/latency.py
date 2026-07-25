#!/usr/bin/env python3
"""Measure per-call text-normalization latency without dataset or ASR I/O."""

from __future__ import annotations

import argparse
import json
import math
import time
from collections.abc import Callable
from pathlib import Path

from fleurs import normalizers_for


def percentile(samples: list[int], fraction: float) -> float:
    position = (len(samples) - 1) * fraction
    lower, upper = math.floor(position), math.ceil(position)
    value = samples[lower] if lower == upper else samples[lower] + (samples[upper] - samples[lower]) * (position - lower)
    return value / 1_000_000


def measure(normalizers: dict[str, Callable[[str], str]], text: str, iterations: int, warmup: int) -> dict[str, dict[str, float | int]]:
    """Return latency percentiles in milliseconds for each normalizer."""
    report = {}
    for name, normalizer in normalizers.items():
        for _ in range(warmup):
            normalizer(text)
        samples = []
        for _ in range(iterations):
            started = time.perf_counter_ns()
            normalizer(text)
            samples.append(time.perf_counter_ns() - started)
        samples.sort()
        report[name] = {
            "calls": len(samples),
            "p50_ms": percentile(samples, 0.50),
            "p90_ms": percentile(samples, 0.90),
            "p95_ms": percentile(samples, 0.95),
            "p99_ms": percentile(samples, 0.99),
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", required=True, help="FLEURS language config, for example en_us or hi_in")
    parser.add_argument("--text", required=True, help="Representative transcript to normalize")
    parser.add_argument("--iterations", type=int, default=1_000)
    parser.add_argument("--warmup", type=int, default=100)
    parser.add_argument("--output", type=Path, help="Write the JSON report here instead of stdout")
    args = parser.parse_args()
    if args.iterations < 1 or args.warmup < 0:
        parser.error("--iterations must be positive and --warmup must not be negative")
    report = {
        "language": args.language,
        "iterations": args.iterations,
        "warmup": args.warmup,
        "unit": "milliseconds per normalization call",
        "latency": measure(normalizers_for(args.language), args.text, args.iterations, args.warmup),
    }
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
