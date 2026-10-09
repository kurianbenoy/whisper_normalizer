# Release notes

<!-- do not remove -->

## 1.0.0a1 - 2026-10-09

First 1.0 alpha. It adds a stable language-selection API, many more languages, ASR evaluation metrics, and fixes several Indic normalization bugs.

**Breaking changes**

- Python 3.11 or later is now required. Python 3.9 and 3.10 have reached end of life.
- Removed the obsolete `whisper_normalizer.core` module.

**New**

- Added `get_normalizer(language, **options)` and `supported_languages()` as the recommended entry point. `get_normalizer` accepts ISO codes, BCP-47 tags such as `hi-IN` and `zh-Hans`, and English language names. It raises a clear `ValueError` for an unsupported language and for any option the selected normalizer does not accept, such as `tts_mode`, and never falls back silently to a generic normalizer.
- The registry covers 101 languages in three tiers (15 dedicated, 4 sharing a script normalizer, 82 conservative generic), with per-language capability metadata.
- Added `tts_mode=True` for French, Spanish, Arabic, Chinese and Russian, for the generic tier (via `num2words`, installed with `pip install whisper_normalizer[tts]`), and for the Devanagari-based (Marathi, Nepali) and Assamese normalizers. Requesting `tts_mode` for a language `num2words` does not cover raises `ValueError`.
- Added `whisper_normalizer.evaluation` with `wer`, `cer`, orthographically-informed WER (`oiwer`, `oiwer_alignment`) and caller-judged `llm_wer`. It runs offline with no API keys or extra dependencies.
- Added a Python usage example script, `examples/hello_world_whisper_normalizer.py`.

**Fixed**

- Punjabi and Telugu `tts_mode`: `$20` is now spoken as a dollar amount; the dollar rule previously never matched.
- Punjabi and Telugu colon-to-visarga correction replaced the preceding character with a control character; Punjabi `do_canonicalize_addak=True` had the same corruption.
- All Indic normalizers: spelling digits as words rewrote digits inside other numbers, so `"1 10"` became `"एक एक0"`. Each number is now converted on its own.
- Hindi and Punjabi raised `ValueError` on decimal numbers such as `"1.5"` in default mode. Each side of the dot is now spelled, for example `"एक.पाँच"`.
- Fixed a `SyntaxWarning` from `BasicTextNormalizer` on newer Python versions.

**Internal**

- The nine Indic normalizers with `tts_mode` now share one pipeline for currencies, decimals, URLs, e-mail addresses, symbols and digit spelling, with each language supplying only its spoken words. Output is unchanged apart from the fixes above; per-language differences such as Hindi reading fractions digit by digit and Punjabi keeping Latin letter case are preserved.
- Release builds now produce an sdist as well as a wheel, and the release workflow fails unless the tag, package version and changelog entry agree.

## 0.1.15 - 2026-07-26

- Added text normalizers for French, Spanish, Arabic, Chinese, and Russian.
- Added French and Spanish written-number conversion, localized decimal and thousands-separator handling, and accent-preserving punctuation cleanup.
- Added Arabic diacritic and tatweel removal, orthographic-variant normalization, and Arabic-Indic digit conversion.
- Added Chinese written-numeral conversion and whitespace-free punctuation normalization.
- Added Russian `ё`/`е` normalization and localized numeric-separator handling.

## 0.1.14 - 2026-07-17

- Documented the `preserve_marks=True` option for retaining Unicode Mark characters in `BasicTextNormalizer`, including its intended use for scripts where marks are meaningful.

## 0.1.13 - 2026-07-16

- Added `preserve_marks=True` to `BasicTextNormalizer` so Unicode Mark characters can be retained.
- Migrated the project to nbdev v3.

## 0.1.12 - 2025-06-06

- Fixed English spelling-data loading for Python 3.9 compatibility (#23).

## 0.1.11 - 2025-05-08

- Restored and corrected the Hindi normalizer and related Indic TTS normalization behavior.

## 0.1.10 - 2025-05-08

- Corrected regressions in the Indic normalizers introduced by the previous release.

## 0.1.9 - 2025-05-07

- Added acronym expansion for Indic TTS mode.
- Fixed website normalization in Indic TTS mode.

## 0.1.8 - 2025-05-06

- Improved spoken URL and bare-domain normalization in Indic TTS mode.

## 0.1.7 - 2025-05-06

- Added `HindiNormalizer` with TTS-mode support.

## 0.1.6 - 2025-05-06

- Updated package metadata for modern Python packaging.

## 0.1.5 - 2025-05-06

- Removed the obsolete generated `indic_normalizer` module from the package.

## 0.1.4 - 2025-05-05

- Added `tts_mode` across the supported Indic normalizers, including spoken forms for currencies, decimals, email addresses, URLs, and special symbols.

## 0.1.3 - 2025-05-04

- Added `PunjabiNormalizer`.
- Switched Indic number-to-words support to AI4Bharat's `indic-numtowords` package.

## 0.1.2 - 2025-04-26

- Expanded English text-normalization spellings and improvements contributed by @qiisziilbash.

## 0.1.1 - 2025-04-19

- Added common informal English contractions (#22).
- Migrated build metadata to `pyproject.toml`.

## 0.1.0 - 2025-03-02

- Added Indic number normalization through `indic-num2words`.
- Removed the network call from `EnglishTextNormalizer`.

## 0.0.10 - 2024-06-09

- Fixed `HindiNormalizer` inheritance from `DevanagariNormalizer` (#18).

## 0.0.9 - 2024-06-05

- Added `HindiNormalizer`.
- Updated Devanagari and Telugu normalizer styling.
- Removed `UrduNormalizer` and `IndicNormalizerFactory`.

## 0.0.8 - 2024-02-10

- Integrated Malayalam normalization improvements contributed by @kavyamanohar.
- Updated Indic normalizers to follow the Whisper normalizer interface and fixed #10.

## 0.0.7 - 2024-02-08

- Fixed Malayalam normalization to match the Whisper normalizer interface (#8).

## 0.0.6 - 2024-02-06

- Added Indic language normalizers derived from `indic-nlp-library`.
- Added attribution for the upstream libraries and improved documentation.
- Fixed `BasicTextNormalizer` behavior for non-English scripts.

## 0.0.4 - 2024-02-03

- Added Malayalam text normalization.

## 0.0.3 - 2024-02-03

- Updated the package for the 2024 Q1 Whisper normalization changes.

## 0.0.2 - 2023-03-22

- Added module descriptions and expanded installation, usage, and project documentation.
- Closed #1 and #2.

## 0.0.1 - 2023-03-21

- Initial release.
