# Release notes

<!-- do not remove -->

## 1.0.1 - 2026-11-10

This patch release fixes English apostrophe handling so possessive nouns are no longer read as "is".

**Fixed**

- English `'s` is now expanded to "is" after pronouns and wh-words (`he's`, `she's`, `it's`, `that's`, `there's`, `here's`, `what's`, `who's`, `where's`, `when's`, `why's`, `how's`, `which's`, and their `-ever` forms). Indefinite pronouns are ambiguous, so the next word decides: `"someone's at the door"`, `"everyone's ready"` and `"someone's building a house"` become "someone is at the door", "everyone is ready" and "someone is building a house", while `"someone's car"`, `"everyone's happy place"` and `"someone's building"` remain possessive ("someones car", "everyones happy place" and "someones building"). Elsewhere it is treated as a possessive: the apostrophe is dropped and the "s" is kept, so `"John's car"` becomes `"johns car"` and `"Wittgenstein's quote"` becomes `"wittgensteins quote"` instead of `"john is car"` and `"wittgenstein is quote"`.
- English contractions written with a curly apostrophe (`’`) now normalize like straight ones, so `"it’s"` becomes "it is" and `"don’t"` becomes "do not" instead of being split into two words.
- The existing contraction rules still run first, so `"she's been"` remains "she has been", `"let's"` remains "let us", and `"John's got"` becomes "john has got". Both default and `tts_mode` output use the new handling.

**Migrating**

- Re-run stored English baselines or WER references: possessive `'s` and curly-apostrophe contractions now normalize differently.

## 1.0.0 - 2026-10-31

First stable 1.0 release. It adds a stable language-selection API, many more languages, ASR evaluation metrics, and fixes several normalization bugs.

**Breaking changes**

- Python 3.11 or later is now required. Python 3.9 and 3.10 have reached end of life.
- Removed the obsolete `whisper_normalizer.core` module.

**New**

- Added `Normalizer(language, **options)` (also `Normalizer.for_language(language, **options)`) and `supported_languages()` as the recommended entry point. `Normalizer` is callable, exposes `language`, `name`, `tier`, `capabilities`, `options` and `tts_mode`, keeps the selected language normalizer in `.normalizer`, and accepts ISO codes, BCP-47 tags such as `hi-IN` and `zh-Hans`, and English language names. It raises a clear `ValueError` for an unsupported language and for any option the selected normalizer does not accept, such as `tts_mode`, and never falls back silently to a generic normalizer.
- Boolean options such as `tts_mode` now raise `TypeError` when given a non-bool such as `"no"`, instead of being silently accepted.
- The registry covers 101 languages in three tiers (15 dedicated, 4 sharing a script normalizer, 82 conservative generic), with per-language capability metadata.
- Added `tts_mode=True` for French, Spanish, Arabic and Russian, for the generic tier (via `num2words`, installed with `pip install whisper_normalizer[tts]`), and for the Marathi (Devanagari-based) and Assamese normalizers. Chinese, Nepali and Sanskrit have no number words in `num2words` or `indic-numtowords`, so requesting `tts_mode` for them raises `ValueError`.
- Added `tts_mode=True` for `EnglishTextNormalizer` (and `Normalizer("en", tts_mode=True)`): written numbers stay words instead of becoming digits, and digits, ordinals ("21st"), currencies (`$`, `€`, `£`, `¢`; "$0.05" is "five cents"), percentages and decimals are spelled out ("$1,250.75" becomes "one thousand two hundred and fifty dollars seventy five cents"), with `&`, `+`, `=` and `@` spoken as words. Default English behavior is unchanged.
- Added a supported-languages table to the README and docs, generated from the registry and checked by tests against real behavior (`tts_mode` availability and digit spelling for all 101 languages, mark handling for every language except Chinese, which has no combining marks). It states per language whether digits become words always (the Indic family, including Nepali and Sanskrit, which use Hindi number words), only with `tts_mode` (most others) or never, and whether combining marks are kept or stripped (stripped only for English and Arabic). `supported_languages()` entries expose this as `digits_to_words` and `marks`.
- Added `whisper_normalizer.evaluation` with `wer`, `cer`, orthographically-informed WER (`oiwer`, `oiwer_alignment`) and caller-judged `llm_wer`. It runs offline with no API keys or extra dependencies.
- Added a Python usage example script, `examples/hello_world_whisper_normalizer.py`.

**Fixed**

- Punjabi and Telugu `tts_mode`: `$20` is now spoken as a dollar amount; the dollar rule previously never matched.
- Punjabi and Telugu colon-to-visarga correction replaced the preceding character with a control character; Punjabi `do_canonicalize_addak=True` had the same corruption.
- All Indic normalizers: spelling digits as words rewrote digits inside other numbers, so `"1 10"` became `"एक एक0"`. Each number is now converted on its own.
- Hindi and Punjabi raised `ValueError` on decimal numbers such as `"1.5"` in default mode. Each side of the dot is now spelled, for example `"एक.पाँच"`.
- Indic `tts_mode`: `&` was spoken as "or" and is now spoken as "and", and the runs of spaces left around spoken symbols are collapsed (including in the Marathi and other Devanagari-based normalizers).
- Indic normalizers crashed with `KeyError` on numbers written in a script's own digits (for example `५०` or `௫௦`); they are now spelled like the same ASCII number.
- Fixed a `SyntaxWarning` from `BasicTextNormalizer` on newer Python versions.
- French no longer turns the article "un"/"une" into the number `1` (`"un chat"` used to normalize to `"1 chat"`).
- English: a decimal that starts with `1` kept its point, so `"1.5"` now stays `"1.5"` instead of becoming `"one.5"`.
- English: numbers such as `"one thousand million"` now normalize to `1000000000` instead of silently dropping the `million`.
- `BasicTextNormalizer` can be pickled again, so it works with `multiprocessing`-based data pipelines.
- English `tts_mode` now speaks a leading minus sign (`"-5"` is "minus five"), reads phone numbers digit by digit (`"555-1234"`) and spells decades (`"1990s"` is "nineteen nineties").
- French, Spanish and Russian `tts_mode` now speak `€`, `$`, `£` (and `₽` in Russian) instead of dropping the currency symbol.
- `NormalizerI.normalize()` and `BaseNormalizer` subclasses without a TTS lexicon now raise `NotImplementedError` instead of returning `None` or failing with `AttributeError`; the broken `NormalizerI.correct_visarga()` helper was removed, and `get_char_stats()` returns counts instead of printing them.
- Removed the dead `"kK"` entries from `langinfo.SCRIPT_RANGES`/`IE_LANGUAGES`.
- Sample webapp: the `devanagari` option is selectable again (it was an enum alias of `hi` and was silently dropped), and HTTP errors raised for invalid options are no longer re-wrapped.

**Migrating from 0.1.x**

- Use Python 3.11 or later.
- `Normalizer("hi", tts_mode=True)` is the new recommended entry point; the direct classes (`HindiNormalizer`, `EnglishTextNormalizer`, ...) keep working unchanged.
- `whisper_normalizer.core` is gone; it had no public API.
- If you stored Indic baselines or evaluation scores, re-run them: the fixes above change output for numbers containing digits that also appear inside other numbers (`"1 10"`), for colons after Punjabi and Telugu text, for `&` in `tts_mode`, and for decimals in default mode (which used to crash for Hindi and Punjabi).
- Re-run stored baselines for French (the article `un`/`une`), English decimals (`"1.5"`) and `tts_mode` output (signs, phone numbers, decades, currency words), whose normalized text changed.
- Pass real booleans for options such as `tts_mode`.

**Internal**

- The nine Indic normalizers with `tts_mode` now share one pipeline for currencies, decimals, URLs, e-mail addresses, symbols and digit spelling, with each language supplying only its spoken words. Output is unchanged apart from the fixes above; per-language differences such as Hindi reading fractions digit by digit and Punjabi keeping Latin letter case are preserved.
- The English normalizers are checked against OpenAI Whisper's own normalizer test suite (67 assertions), so drift from upstream is caught by the notebook tests. The intentional divergences are pinned separately.
- Release artifacts now include an sdist as well as a wheel.

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
