# Contributing to neopool-modbus

Thank you for your interest in contributing! 🙌
This is the protocol layer behind the [Home Assistant `neopool` integration](https://github.com/svasek/homeassistant-neopool-modbus); changes here propagate to every consumer of the library.

## Before You Start

- Please open an issue first via [GitHub Issues](https://github.com/svasek/python-neopool-modbus/issues/new/choose)
  → This allows discussion of the change, validation of the idea, and agreement on the scope before coding.
- All pull requests should relate to an existing issue.

## Pull Request Guidelines

- ✅ Use [Conventional Commits](https://www.conventionalcommits.org/) + gitmoji for commit messages and the PR title (`<type>(<scope>): <gitmoji> <description>`).
- ✅ Keep pull requests focused and minimal — avoid combining unrelated changes.
- ✅ Update or add documentation if applicable (`README.md`, docstrings, examples).
- ✅ **Public API changes** (anything exported from `neopool_modbus`, `neopool_modbus.registers`, `neopool_modbus.decoders`, `neopool_modbus.status_mask`) must be flagged in the PR description; breaking changes require a SemVer major bump.

Include a line in your PR description like this:

Resolves #42

This ensures the corresponding issue will be closed automatically once the PR is merged.

## Local Checks

Before submitting, please verify locally:

```bash
ruff check                         # linting
ruff format --check                # formatting
basedpyright                       # type-check (0 errors)
mypy                               # type-check (0 errors, strict)
pytest --cov                       # tests + coverage (≥ current baseline)
```

CI runs the same checks on every PR.

## Code Style

- Python ≥ 3.13.
- Strict type hints (`py.typed` shipped); both `basedpyright` and `mypy --strict` must pass with 0 errors.
- 100 % unit-test coverage is the project goal — new code should be covered.
- Prefer clarity over cleverness; readable code is maintainable code.

---

Thanks again for contributing to the project! 🎉
