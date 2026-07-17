# Release notes

<!-- do not remove -->
## 0.1.14

- Prevent distribution of the obsolete `whisper_normalizer.indic_normalizer` module; use `whisper_normalizer.indic` for Indic normalizers.
- Document `BasicTextNormalizer(preserve_marks=True)` for scripts that use Unicode Mark characters.
- Install `indic-numtowords` from the AI4Bharat Git repository.

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
