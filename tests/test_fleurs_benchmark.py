"""Tests for the dependency-light FLEURS benchmark helpers."""

import importlib.util
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("fleurs_benchmark", Path(__file__).parents[1] / "benchmarks" / "fleurs.py")
assert SPEC and SPEC.loader
fleurs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fleurs)


def test_evaluate_reports_corpus_error_rates():
    report = fleurs.evaluate(
        [{"reference": "Hello world", "prediction": "hello brave world"}], {"lower": str.lower}
    )
    wer = report["metrics"]["lower"]["wer"]
    assert report["examples"] == 1
    assert wer["insertions"] == 1
    assert wer["reference_length"] == 2
    assert wer["rate"] == 0.5


def test_language_policy_preserves_marks_and_uses_indic_normalizer():
    policies = fleurs.normalizers_for("hi-IN")
    assert set(policies) == {"raw", "basic", "basic_preserve_marks", "language"}
    assert policies["basic_preserve_marks"]("किताब") == "किताब"
