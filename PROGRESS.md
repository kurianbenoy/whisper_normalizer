# whisper_normalizer — Progress Log

Day-by-day record of the project from the first commit (Day 1, 2023-03-21)
through the latest commit (Day 38, 2026-08-11), derived from git history,
tags, and `CHANGELOG.md`.

- Repository: `github.com/kurianbenoy/whisper_normalizer`
- Current version: `0.1.15`
- Goal: a Python implementation of OpenAI Whisper's text
  standardization/normalization approach, extended to Indic and, later,
  international languages.

## Release timeline

| Version | Date | Highlight | Tag commit |
|---------|------|-----------|------------|
| 0.0.1 | 2023-03-21 | Initial release (Whisper `BasicTextNormalizer` + `EnglishTextNormalizer`) | `f65fe64` |
| 0.0.2 | 2023-03-22 | Module docs, installation/usage documentation | `085bcf3` |
| 0.0.3 | 2024-02-04 | 2024 Q1 Whisper normalization update | `0695292` |
| 0.0.4 | 2024-02-04 | Malayalam text normalization | `2d46103` |
| 0.0.6 | 2024-02-06 | Indic normalizers derived from `indic-nlp-library` | `3687499` |
| 0.0.7 | 2024-02-08 | Malayalam normalization aligned to Whisper interface (#8) | `58363ac` |
| 0.0.8 | 2024-02-10 | Malayalam improvements by @kavyamanohar; Whisper interface fixed (#10) | `d9f25d4` |
| 0.0.9 | 2024-06-05 | `HindiNormalizer`; Devanagari/Telugu styling; drop Urdu + factory | `453ee2e` |
| 0.0.10 | 2024-06-09 | Fix Hindi inheritance from `DevanagariNormalizer` (#18) | `6c4f5f5` |
| 0.1.0 | 2025-03-02 | Indic number normalization via `indic-num2words`; offline English normalizer | `e363736` |
| 0.1.1 | 2025-04-19 | Informal English contractions (#22); `pyproject.toml` migration | `9864e5a` |
| 0.1.2 | 2025-04-26 | English spelling-data expansion by @qiisziilbash | `364b0c7` |
| 0.1.3 | 2025-05-04 | `PunjabiNormalizer`; switch to AI4Bharat `indic-numtowords` | `5ffb12e` |
| 0.1.4 | 2025-05-05 | `tts_mode` across Indic normalizers | `73f1971` |
| 0.1.5 | 2025-05-06 | Remove obsolete generated `indic_normalizer` module | `25610cf` |
| 0.1.6 | 2025-05-06 | Modern Python packaging metadata | `f5a5dfb` |
| 0.1.7 | 2025-05-06 | `HindiNormalizer` with TTS support | `aef5146` |
| 0.1.8 | 2025-05-06 | Better spoken URL/bare-domain normalization | `7100b52` |
| 0.1.9 | 2025-05-07 | Indic TTS acronym expansion; website fix | `04d2d73` |
| 0.1.10 | 2025-05-08 | Correct Indic regressions | `f9218bb` |
| 0.1.11 | 2025-05-08 | Restore/fix Hindi + Indic TTS behavior | `7f26747` |
| 0.1.12 | 2025-06-07 | Python 3.9 spelling-data loading fix (#23) | `39d45c7` |
| 0.1.13 | 2026-07-16 | `preserve_marks=True` (#25); nbdev v3 migration | `0bcb607` |
| 0.1.14 | 2026-07-17 | Document `preserve_marks=True` | `4a02c0c` |
| 0.1.15 | 2026-07-26 | French, Spanish, Arabic, Chinese, Russian normalizers | `a20de36` |

> Note: git tags are not perfectly aligned with the changelog version numbers
> (for example, tag `0.0.5` points at the 0.0.4 Malayalam release, and
> `v0.1.13` is the only `v`-prefixed tag). The table above follows
> `CHANGELOG.md`.

## Day-by-day log

### Day 1 — 2023-03-21
First code lands: `Initial commit` (`ed3e61c`), nbdev scaffolding with `nbs/`
and `settings.ini` (`5d8a724`, `69b0420`, `c47942d`), and the initial port of
Whisper's `BasicTextNormalizer` + `EnglishTextNormalizer` (`f65fe64`). Tagged
**0.0.1**.

### Day 2 — 2023-03-22
Documentation and release hardening: index page, module docs for `basic`,
`english`, and `langinfo`, README, initial `CHANGELOG.md`, version bump, and
release (`085bcf3`) → **0.0.2**. Closed issues #1 and #2.

### Day 3 — 2024-02-04
Updated normalization to match Whisper's 2024 Q1 changes (`2cdfe2b`),
released **0.0.3** (`0695292`), then added Malayalam normalization
(`0ded881`) and released **0.0.4** (`2d46103`).

### Day 4 — 2024-02-06
Added attribution to the OpenAI Whisper repo, added
`IndicTextNormalizer`/Indic normalizers derived from `indic-nlp-library`,
fixed `BasicTextNormalizer` for non-English scripts, cleaned up comments
(`577a984` … `8c90245`), and released **0.0.6** (`3687499`).

### Day 5 — 2024-02-08
Reworked Malayalam normalization to the Whisper normalizer format (#8),
refreshed docs, and iterated through releases ending at tag `0.0.7`
(`3d8c15a` … `58363ac`).

### Day 6 — 2024-02-09 (@kavyamanohar)
Added Malayalam unit tests and moved tests outside the package directory
(`827ea3f`, `18023f3`), expanded test cases (`793e796`), updated the README
with test instructions (`36255e3`, `a47c00b`), and added Samvruthokaram
normalization (`ebdfedb`).

### Day 7 — 2024-02-10
Merged PR #11 (`ml-improvement`, `88167eb`), renamed notebooks, aligned the
indic-nlp normalizer with the Whisper interface (`af3e44e`), fixed #10
(`e466f27`), updated CI, and released **0.0.8** (`d9f25d4`).

### Day 8 — 2024-02-14
Added GitHub issue templates (`ec84817`).

### Day 9 — 2024-03-09
Added and iterated on `FUNDING.yml` (`95dfe74`, `6641254`).

### Day 10 — 2024-03-12
Added README badges, ran `format code` (Black), and polished docs
(`ff866f9` … `ead9253`).

### Day 11 — 2024-03-19
Two more `FUNDING.yml` updates (`1d18214`, `7751f5a`).

### Day 12 — 2024-04-15
`FUNDING.yml` update (`812c6af`).

### Day 13 — 2024-06-05
Added `HindiNormalizer`, made Devanagari/Telugu style changes, removed
`UrduNormalizer` and `IndicNormalizerFactory`, updated docs, and added the
`v0.9` changelog entry (`cb854a6` … `453ee2e`) → **0.0.9**.

### Day 14 — 2024-06-10
Bumped the version for **0.0.10** and updated the README (`df8f776`,
`6c4f5f5`, `457d8da`).

### Day 15 — 2024-07-05 (@Nishant Bhansali)
Fixed Hindi normalizer inheritance from `DevanagariNormalizer` (#18,
`09861ac`).

### Day 16 — 2024-11-26 (@LucunJi)
Fixed a broken citation link in the docs (#20, `21d1b08`).

### Day 17 — 2025-03-02
Updated the normalizer module (`6533d89`), prepared and released **0.1.0**
(`83d9669`, `e363736`): Indic number normalization via `indic-num2words` and
removal of the network call from `EnglishTextNormalizer`. Removed
`.github/FUNDING.yml` (`f1ffb7f`).

### Day 18 — 2025-04-16 (@Mario Shafiei)
Added common informal English contractions (#22, `14a12f3`).

### Day 19 — 2025-04-19
Migrated build metadata to `pyproject.toml` and bumped to **0.1.1**
(`af8aabb`, `9864e5a`), moved explicitly written Malayalam tests into
notebooks (`7f893ee`), added dev requirements (`e5e17cd`), updated CI
(`3371047`), and updated `settings.ini` (`5c82175`).

### Day 20 — 2025-04-26
Re-added @qiisziilbash's spelling-data changes (`364b0c7`) and cleaned the
notebook (`ee1ce9e`) → **0.1.2**.

### Day 21 — 2025-05-04
Switched Indic number support to AI4Bharat's `num2words` (`55662ff`) and
added `PunjabiNormalizer` (`5ffb12e`) → **0.1.3**.

### Day 22 — 2025-05-05
Blackified the code (`3e0e543`), added `tts_mode` to all ten Indic languages
covering currencies, decimals, URLs, emails, and special symbols (`394bd4f`),
bumped to **0.1.4** (`73f1971`), and updated notebooks (`ef5383c`).

### Day 23 — 2025-05-06
Rapid release day: **0.1.5** removed the obsolete generated
`indic_normalizer` module (`25610cf`); **0.1.6** modernized packaging
(`f5a5dfb`); `HindiNormalizer` added (`e44b620`) with **0.1.7** (`aef5146`);
spoken URL/bare-domain handling improved (`7100b52`) with **0.1.8**; changelog
updated (`258e8af`).

### Day 24 — 2025-05-07
Added `expand_acronyms` and fixed website bugs in the Indic TTS normalizers
(`04d2d73`) → **0.1.9**.

### Day 25 — 2025-05-08
Fixed bugs and CI (`7f26747`, `f9218bb`, `23cf561`) → **0.1.10** and
**0.1.11**.

### Day 26 — 2025-06-07 (@BakerBunker)
Made spelling-data loading Python 3.9 compatible via `files("module")` (#23,
`c296e65`); released **0.1.12** and set the minimum Python version to 3.9
(`39d45c7`, `1f93b29`).

### Day 27 — 2025-06-16 (@chakka-guna-sekhar-venkata-chennaiah)
Added REST API / Dockerisation support for the sample webapp (#24, `038ec6b`)
and uploaded assets (`2294952`).

### Day 28 — 2025-08-15
Formatted code and updated the README (`eb08f24`, `52b7096`, `871a32a`).

### Day 29 — 2025-09-20
Updated README (`db8ec7c`).

### Day 30 — 2025-09-22
Created `SECURITY.md` and revised it (`26a34a1`, `347f471`, `7288203`).

### Day 31 — 2025-10-02
Pinned `requirements.txt` for `sample_webapp` (`1fef180`).

### Day 32 — 2025-10-06
Added `humans.txt` (`d2ffe3d`), removed `CHANGELOG.bak` (`ef42591`), and
updated the README (`756f0a5`).

### Day 33 — 2026-07-16
Added `AGENTS.md` (`a2d4014`), migrated to nbdev v3 (`9b1f22a`), added
`preserve_marks=True` to `BasicTextNormalizer` (thanks to #25 from
Gazzara-lab, `1364e90`), and bumped to **0.1.13** (`0bcb607`).

### Day 34 — 2026-07-17
Added UN6 languages, OI-WER evaluation utilities, and documented the
preserve-marks feature (`6ab5687`, `65ecca3`, `16159aa`, `8a69218`); vendored
then switched to the published `indic-numtowords` package (`89c44c5`,
`02a3273`); consolidated all prior history into the changelog (`257856d`);
released **0.1.14** (`4a02c0c`); fixed CI/CD (`8423269`); added UN6 languages
again after the packaging change (`98e0b71`).

### Day 35 — 2026-07-26
Added French, Spanish, Arabic, Chinese, and Russian normalizers (`c62f42e`),
bumped and released **0.1.15** (`9a1a5e3`, `a20de36`), updated and expanded
the changelog and release-note guidance (`6500b53`, `15cfc3f`, `a31b780`),
removed the obsolete `core` module (`70b5efa`), added `V1_RELEASE_PLAN.md`
(`91c6b65`), and merged `feature/oiwer-evaluation` (`82140d8`).

### Day 36 — 2026-08-01
Refactored the multilingual text normalizer and language support
(`db1362a`), fixed `tts_mode` initialization in `BengaliNormalizer`
(`1b76003`), updated top-level imports/`__all__` (`42cee8f`) and `_modidx.py`
references (`1cce443`), and uploaded assets (`42da401`).

### Day 37 — 2026-08-10
Updated the testing workflow (`a51dbb1`), the security policy (`5059501`),
the release CI workflow (`5ec9bc9`), and the README (`d429312`).

### Day 38 — 2026-08-11
Uploaded documentation/assets (`9183422`, `cc371a5`, `211caac`) — latest
commits in the repository.

## Contributors

- @kurianbenoy (project lead) — development, docs, releases.
- @kavyamanohar — Malayalam unit tests and normalization improvements.
- @Nishant Bhansali — Hindi normalizer inheritance fix.
- @LucunJi — citation link fix.
- @Mario Shafiei — informal English contractions.
- @BakerBunker — Python 3.9 compatibility.
- @chakka-guna-sekhar-venkata-chennaiah — REST API / Dockerisation.

## Current state (Day 38, 2026-08-11)

- Package version `0.1.15`; generated modules: `basic`, `english`, `indic`,
  `international`, `multilingual`, `evaluation`, `langinfo`.
- Public API includes `get_normalizer`, `supported_languages`, and
  `__version__`; normalizer classes remain stable advanced APIs.
- Languages covered: English + Basic, ten Indic TTS-capable normalizers (plus
  script-tier Assamese/Marathi/Nepali/Sanskrit), five international languages,
  and a generic multilingual tier.
- Active roadmap in `V1_RELEASE_PLAN.md` targeting 1.0 with a stable selection
  API, TTS mode across supported languages, regression fixtures, trusted
  publishing, and optional ASR evaluation (WER/CER, OIWER, LLM-WER).
