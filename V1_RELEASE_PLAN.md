# whisper_normalizer 1.0 plan

## Release intent

`whisper_normalizer` 1.0 means that choosing and using a supported text
normalizer is predictable. It is not a claim to support every language,
normalization convention, or Whisper feature.

The 1.0 promise is:

> A stable, explicit API for normalizing text in documented languages, with
> clear behavior and no silent language fallback.

This follows three design principles:

1. **Be explicit, not magical.** A caller chooses a language; the library does
   not guess it or quietly substitute a generic normalizer.
2. **Provide one canonical path.** New users should not need to know the
   package's internal module layout to select a normalizer.
3. **Keep the core small.** Language-specific behavior belongs in language
   normalizers; a general-purpose selector should not become a configuration
   framework.

## 1.0 public contract

Add a small, documented selection API as the recommended entry point:

```python
from whisper_normalizer import get_normalizer

normalizer = get_normalizer("hi", tts_mode=True)
result = normalizer("...")
```

The API should:

- accept documented language codes and aliases;
- expose `supported_languages()` or equivalent metadata;
- raise a clear error for an unsupported language;
- validate options such as `tts_mode` against the selected normalizer;
- retain direct normalizer classes as supported advanced APIs.

The documentation must include a capability table for every supported language:
language code, normalizer class, number handling, mark/diacritic policy, and
whether `tts_mode` is available.

## Scope

### In scope

- English and `BasicTextNormalizer`.
- Existing Indic normalizers, including their documented TTS support.
- French, Spanish, Arabic, Chinese, and Russian normalizers.
- Stable language selection, clear errors, regression tests, and release
  automation.

### Explicitly out of scope

- Supporting every Whisper language before 1.0.
- Automatic language detection or implicit fallback to `BasicTextNormalizer`.
- A CLI, HTTP service, or plugin system.
- Claiming universal linguistic correctness; normalization remains a
  language-specific comparison policy.

## Work plan

### Milestone 1 — settle the interface

1. Decide the exact factory name, accepted codes, aliases, and error types.
2. Implement the registry/factory and top-level exports.
3. Document direct-class imports and define them as stable APIs.
4. Remove or make private accidental public surface such as `core.foo`.

**Exit criteria:** one short quickstart can select every supported normalizer;
unsupported input fails loudly and helpfully.

### Milestone 2 — make language behavior a promise

1. Add a capability table and a concise behavior page for each normalizer.
2. Add regression fixtures for punctuation, Unicode normalization, marks,
   numbers, mixed scripts, and malformed input for each supported language.
3. Add a regression test whenever a reported normalization disagreement is
   resolved.
4. Clearly label conservative and language-specific transformations.

**Exit criteria:** every documented behavior has a test, and every supported
language has examples authored or reviewed by a fluent speaker where possible.

### Milestone 3 — make distribution trustworthy

1. Test every Python version advertised in package metadata, or reduce that
   advertised range.
2. Build an sdist and wheel in CI; run package metadata validation and a
   clean-environment import smoke test.
3. Add tag-triggered GitHub Release and PyPI Trusted Publishing.
4. Keep release tags, package version, changelog, and PyPI release aligned.
5. Replace placeholder content in `SECURITY.md` with the actual supported
   version policy and a private reporting process.

**Exit criteria:** a release tag produces installable artifacts without a
manual local upload, and `pip install whisper_normalizer==1.0.0` works from a
clean environment.

### Milestone 4 — release candidate and launch

1. Publish `1.0.0rc1` with migration notes from the 0.x API.
2. Ask users and language contributors to test their normalizers against real
   ASR evaluation data.
3. Fix release-candidate regressions only; defer new language additions.
4. Publish `1.0.0`, a GitHub Release, and a short announcement.

## Definition of done

Ship 1.0.0 when all of the following are true:

- The selection API, direct normalizer classes, and supported options are
  documented as stable.
- No supported-language path silently falls back to a generic normalizer.
- Documentation accurately lists all supported languages and modes.
- Notebook tests and the supported Python-version matrix pass.
- Wheel and source distributions are verified and published from the release
  tag.
- The changelog contains user-facing 1.0 release notes and a migration guide
  covers any breaking changes.

## Post-1.0 direction

Add new languages only when they meet the same bar: a documented policy,
regression fixtures, native-language review where available, and a registry
entry. This lets the project expand without making the core API harder to
understand or less predictable.

## ASR evaluation support

Evaluation is a v1.0 feature, but it remains separate from the normalizer's
core runtime. The base install must remain offline and free of API keys and LLM
dependencies; evaluators ship as an optional integration.

The evaluation input schema should include `id`, `reference`, `hypothesis`, and
`language`, with optional `audio_file` and `context`. A versioned report must
preserve the raw and normalized text, evaluator version/configuration,
per-utterance scores, aggregate scores, and evaluator explanations.

The first integrations are:

- **AI4Bharat OIWER**: call or wrap the upstream reference implementation;
  do not duplicate its orthographic-variation logic.
- **Sarvam LLM evaluation**: support LLM-WER/CER and, when context is
  available, intent and entity preservation. This is an explicit opt-in call
  because it needs credentials and may incur LLM cost.

Reports should compare raw WER/CER, WER/CER after the selected normalizer,
OIWER, and Sarvam results for the same utterances. CI uses fixtures and fake
evaluators only; network calls, secrets, and paid evaluation are never release
requirements.
