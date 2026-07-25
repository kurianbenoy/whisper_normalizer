#!/usr/bin/env python3
"""Evaluate ASR transcripts on FLEURS under several normalization policies."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Iterable, Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from whisper_normalizer.basic import BasicTextNormalizer
from whisper_normalizer.english import EnglishTextNormalizer
from whisper_normalizer.indic import (
    BengaliNormalizer,
    DevanagariNormalizer,
    GujaratiNormalizer,
    HindiNormalizer,
    KannadaNormalizer,
    MalayalamNormalizer,
    OdiaNormalizer,
    PunjabiNormalizer,
    TamilNormalizer,
    TeluguNormalizer,
)

Normalizer = Callable[[str], str]
FLEURS_NORMALIZERS = {
    "bn_in": BengaliNormalizer, "gu_in": GujaratiNormalizer,
    "hi_in": HindiNormalizer, "kn_in": KannadaNormalizer,
    "ml_in": MalayalamNormalizer, "mr_in": DevanagariNormalizer,
    "or_in": OdiaNormalizer, "pa_in": PunjabiNormalizer,
    "ta_in": TamilNormalizer, "te_in": TeluguNormalizer,
}


@dataclass
class ErrorCounts:
    substitutions: int = 0
    deletions: int = 0
    insertions: int = 0
    reference_length: int = 0

    @property
    def rate(self) -> float:
        return 0.0 if not self.reference_length else (
            (self.substitutions + self.deletions + self.insertions) / self.reference_length
        )

    def add(self, other: "ErrorCounts") -> None:
        self.substitutions += other.substitutions
        self.deletions += other.deletions
        self.insertions += other.insertions
        self.reference_length += other.reference_length


def edit_counts(reference: list[str], hypothesis: list[str]) -> ErrorCounts:
    """Return Levenshtein substitution, deletion, and insertion counts."""
    matrix = [[ErrorCounts() for _ in range(len(hypothesis) + 1)] for _ in range(len(reference) + 1)]
    for index in range(1, len(reference) + 1):
        matrix[index][0] = ErrorCounts(deletions=index)
    for index in range(1, len(hypothesis) + 1):
        matrix[0][index] = ErrorCounts(insertions=index)
    for ref_index, ref_token in enumerate(reference, 1):
        for hyp_index, hyp_token in enumerate(hypothesis, 1):
            if ref_token == hyp_token:
                matrix[ref_index][hyp_index] = matrix[ref_index - 1][hyp_index - 1]
                continue
            sub = matrix[ref_index - 1][hyp_index - 1]
            delete = matrix[ref_index - 1][hyp_index]
            insert = matrix[ref_index][hyp_index - 1]
            choices = (
                ErrorCounts(sub.substitutions + 1, sub.deletions, sub.insertions),
                ErrorCounts(delete.substitutions, delete.deletions + 1, delete.insertions),
                ErrorCounts(insert.substitutions, insert.deletions, insert.insertions + 1),
            )
            matrix[ref_index][hyp_index] = min(
                choices, key=lambda item: item.substitutions + item.deletions + item.insertions
            )
    result = matrix[-1][-1]
    result.reference_length = len(reference)
    return result


def normalizers_for(language: str) -> dict[str, Normalizer]:
    """Choose policies suitable for a FLEURS language configuration."""
    language = language.lower().replace("-", "_")
    result: dict[str, Normalizer] = {
        "raw": lambda text: text,
        "basic": BasicTextNormalizer(),
        "basic_preserve_marks": BasicTextNormalizer(preserve_marks=True),
    }
    if language == "en_us":
        result["language"] = EnglishTextNormalizer()
    elif language in FLEURS_NORMALIZERS:
        result["language"] = FLEURS_NORMALIZERS[language]()
    return result


def evaluate(records: Iterable[Mapping[str, str]], normalizers: Mapping[str, Normalizer]) -> dict[str, Any]:
    """Calculate corpus WER and CER for records containing reference/prediction."""
    totals = {name: {"wer": ErrorCounts(), "cer": ErrorCounts()} for name in normalizers}
    examples = 0
    for record in records:
        examples += 1
        for name, normalizer in normalizers.items():
            reference = normalizer(record["reference"])
            prediction = normalizer(record["prediction"])
            totals[name]["wer"].add(edit_counts(reference.split(), prediction.split()))
            totals[name]["cer"].add(edit_counts(list(reference), list(prediction)))
    return {
        "examples": examples,
        "metrics": {
            name: {metric: {**asdict(counts), "rate": counts.rate} for metric, counts in values.items()}
            for name, values in totals.items()
        },
    }


def load_predictions(path: Path) -> dict[str, str]:
    """Read JSONL records with required string fields: ``id`` and ``prediction``."""
    predictions: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        if not isinstance(item.get("id"), str) or not isinstance(item.get("prediction"), str):
            raise ValueError(f"{path}:{line_number} requires string fields 'id' and 'prediction'")
        predictions[item["id"]] = item["prediction"]
    return predictions


def fleurs_records(language: str, split: str, predictions: Mapping[str, str]) -> Iterable[dict[str, str]]:
    try:
        from datasets import load_dataset
    except ImportError as error:
        raise RuntimeError("Install datasets with: uv pip install datasets") from error
    dataset = load_dataset("google/fleurs", language, split=split)
    missing = [str(row["id"]) for row in dataset if str(row["id"]) not in predictions]
    if missing:
        raise ValueError(f"Predictions are missing {len(missing)} FLEURS ids (first: {', '.join(missing[:5])})")
    for row in dataset:
        yield {"reference": row["transcription"], "prediction": predictions[str(row["id"])]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", required=True, help="FLEURS config, for example hi_in or en_us")
    parser.add_argument("--predictions", type=Path, required=True, help="JSONL records: {'id': str, 'prediction': str}")
    parser.add_argument("--split", default="test", choices=("train", "validation", "test"))
    parser.add_argument("--output", type=Path, help="Write the JSON report here instead of stdout")
    args = parser.parse_args()
    report = evaluate(fleurs_records(args.language, args.split, load_predictions(args.predictions)), normalizers_for(args.language))
    report.update({"dataset": "google/fleurs", "language": args.language, "split": args.split})
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
