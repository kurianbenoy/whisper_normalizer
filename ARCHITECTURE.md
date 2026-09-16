# whisper_normalizer — Architecture

## Overview

`whisper_normalizer` turns raw ASR transcripts into a normalized comparison form.
It started as a port of OpenAI Whisper's normalization code (`BasicTextNormalizer`
and `EnglishTextNormalizer`) and grew an Indic layer, an international layer, a
language-selection API, and ASR evaluation metrics.

**Source of truth is notebooks.** This is an nbdev project: `nbs/*.ipynb` is
edited first, `nbdev_export` generates `whisper_normalizer/*.py`, and
`nbdev_docs` publishes `_docs/` with Quarto. Generated modules must not be
hand-edited. Configuration lives in `pyproject.toml` and `nbs/nbdev.yml`.

## Module layout

| Layer | File | Role |
|---|---|---|
| Base (Whisper port) | `basic.py` | `BasicTextNormalizer`, `remove_symbols*`, `preserve_marks` |
| English | `english.py` | `EnglishTextNormalizer` + spelling map in `normalizers/english.json` |
| Indic | `indic.py`, `langinfo.py` | `NormalizerI`/`BaseNormalizer` port of indic-nlp-library, 10 language subclasses, per-script offset arithmetic, TTS mode via `indic-numtowords` |
| International | `international.py` | `_LatinTextNormalizer` (fr/es via `text2num`) and `_NonLatinTextNormalizer` (ar/zh/ru, optional `num2words`) |
| Selection | `multilingual.py` | `LANGUAGE_REGISTRY` (102 languages), `LANGUAGE_ALIASES`, `LanguageSupport`, `get_normalizer()`, `supported_languages()` |
| Evaluation | `evaluation.py` | Self-contained WER/CER/OIWER/LLM-WER on one Levenshtein alignment core |

`whisper_normalizer/__init__.py` exports `get_normalizer`,
`supported_languages`, and `__version__`. Direct normalizer-class imports remain
supported as advanced APIs.

## Normalization pipeline

A normalizer is a callable `str -> str`. Across the tiers the pipeline is:

1. Unicode normalization — NFC for accent-preserving Latin/Generic, NFKC for
   others.
2. Bracket/parenthesis content removal.
3. Script- or language-specific rewrites (Indic script rules, Arabic diacritics,
   Russian `ё`/`е`, Chinese numerals, locale separators).
4. Optional number-to-words conversion (`tts_mode`).
5. Punctuation/symbol replacement and whitespace collapse.

`langinfo.py` stores Indic script tables and addresses characters by
code-point offset relative to a script base, which lets `BaseNormalizer`
share nasal/chandra/vowel-ending logic across scripts.

## Design patterns

- **Registry + factory.** `LANGUAGE_REGISTRY` maps ISO codes to a
  `LanguageSupport` entry; `get_normalizer()` resolves BCP-47 tags, aliases, and
  English names, validates options against the target factory, and returns a
  fresh instance.
- **Tiering.** `dedicated` classes, `script` reuse via `functools.partial` (for
  example Marathi on `DevanagariNormalizer`), and `generic` conservative
  fallback. There is no silent language guessing.
- **Duck-typed callables.** No common base class across tiers; selection only
  requires the callable interface.
- **Lazy optional dependency.** `num2words` is imported only when `tts_mode` is
  requested and ships as the `[tts]` extra.
- **Self-contained evaluation.** WER/CER/OIWER/LLM-WER are implemented from
  scratch; no network calls, API keys, or LLM dependencies in the base install.

## Packaging and CI

- `pyproject.toml` uses setuptools with a dynamic version read from
  `whisper_normalizer.__version__`. Runtime dependencies: `more_itertools`,
  `regex`, `indic-numtowords`, `text2num`. Extras: `dev`, `tts`.
- `test.yaml` runs `nbdev-test` on Python 3.10 and 3.13, builds a wheel, runs
  `twine check`, and imports the wheel in a clean virtual environment.
- `release.yaml` runs on `v*` tags: build, GitHub Release, and PyPI trusted
  publishing.
- `deploy.yaml` publishes the notebook docs.

## Improvement opportunities

Prioritized, highest impact first.

1. **De-duplicate `indic.py`.** Ten subclasses repeat the same `__call__`
   skeleton (nukta decomposition, pipe-to-danda, visarga correction, TTS block);
   Hindi and Devanagari have already drifted. Extract a template method or hooks
   in `BaseNormalizer` (`_script_rewrites()`, `_tts_replacements()`).
2. **Add a pytest suite.** Tests today are notebook cells only. Cover
   invariants: every alias resolves, declared `capabilities` match actual
   constructor support, `tts_mode` is claimed only where a converter exists,
   `normalize(normalize(x)) == normalize(x)`, golden fixtures per language, and
   property-based Unicode fuzzing. CI currently does not test pushes to `new`.
3. **Single-source capability metadata.** The registry tuples,
   `NUM2WORDS_SUPPORTED_LANGS`, and constructor checks are three hand-maintained
   lists that can drift. Declare capabilities on classes or validate them at
   import.
4. **Types and lint.** Define a `Normalizer` protocol, type the registry and
   factory, and add `ruff` plus `pyright`/`mypy`. Explicit metadata can replace
   the `inspect.signature`/`partial.keywords` introspection in
   `get_normalizer()`.
5. **Release hygiene.** Version, tag, and changelog are manual and have
   drifted (tag `0.0.5` marks the 0.0.4 release; lone `v0.1.13` prefix). Add a
   CI check that the tag equals `__version__` and reconcile `main` with `new`
   (18 commits only on `new`, one CI commit only on `main`).
6. **Lighten packaging.** Import `indic-numtowords` and `text2num` lazily and
   split extras (`[indic]`, `[international]`, `[tts]`). Cache
   `normalizers/english.json` once instead of reading it per instance.
7. **Align CI with advertised support.** Classifiers claim Python 3.9–3.14 but
   CI tests 3.10 and 3.13.
8. **Evaluation performance.** The Levenshtein core builds a full backtrace
   matrix; plain `wer`/`cer` only need distances. Keep alignment for
   `llm_wer`/`oiwer` and consider an optional `rapidfuzz` accelerator. The V1
   report schema/CLI is the next usability step.
9. **Smaller polish.** `_digits_to_words` swallows all exceptions silently;
   document that normalizer instances are stateless and reusable; add
   `CONTRIBUTING.md`; avoid cross-module imports of private helpers; refresh
   README links to old notebook paths.

See `V1_RELEASE_PLAN.md` for the 1.0 contract and milestones, and
`CHANGELOG.md` for release history.
