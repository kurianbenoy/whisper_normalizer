# Repository Guidelines

## Project Structure & Module Organization

- `nbs/` is the source of truth. This is an nbdev project: edit notebooks here before regenerating Python modules.
- `whisper_normalizer/` contains generated package modules (`basic.py`, `english.py`, `indic.py`, and `langinfo.py`) plus the English spelling data in `normalizers/english.json`.
- `examples/sample_webapp/` is an optional FastAPI example; its dependencies and Dockerfile are local to that example.
- `_docs/`, `build/`, and `dist/` are generated outputs. Do not hand-edit them.

## Build, Test, and Development Commands

Use `uv` and the repository virtual environment:

```bash
uv pip install --python .venv/bin/python -e .
.venv/bin/nbdev_export   # regenerate whisper_normalizer/ from nbs/
.venv/bin/nbdev_test     # execute notebook tests
.venv/bin/python -m build --wheel --no-isolation
```

Run `nbdev_export` after notebook changes and include the resulting generated-module changes in the same commit. The sample web app can be run from the repository root with `uvicorn app:app --app-dir examples/sample_webapp` after installing its requirements.

## Coding Style & Naming Conventions

Use four-space indentation, `snake_case` for functions and variables, and `PascalCase` for normalizer classes (for example, `EnglishTextNormalizer`). Keep public code in `# | export` notebook cells and place executable assertions in non-export test cells. The project lists Black as a development formatter; preserve Black-compatible formatting.

## Testing Guidelines

Tests are notebook assertions, run by `nbdev_test`; add or update an assertion alongside every behavior change. Exercise affected language normalizers and both default and `tts_mode=True` where applicable. Before release, build a wheel and smoke-test package imports in a clean environment.

## Commit & Pull Request Guidelines

Recent history uses short, imperative subjects such as `update README`, `format code`, and `Pin requirements.txt for sample_web_app`. Keep commits focused and use that style. Pull requests should explain the user-visible change, list validation commands run, link relevant issues, and include screenshots for documentation or sample-webapp UI changes.

## Security & Dependencies

Report vulnerabilities through the process in `SECURITY.md`. Keep runtime dependencies in `settings.ini`; do not add generated environments, caches, or build artifacts to commits.
