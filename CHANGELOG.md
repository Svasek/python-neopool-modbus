# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0](https://github.com/Svasek/python-neopool-modbus/compare/v0.2.0...v1.0.0) (2026-06-06)


### ⚠ BREAKING CHANGES

* async_write_aux_relay() now raises ValueError when relay_index is outside 1-4, where the previous version returned None and logged an error. Callers that relied on the silent no-op must validate the index themselves or wrap the call in a try/except.
* PERIOD_MAP and PERIOD_SECONDS_TO_KEY have been removed from neopool_modbus.registers. They were only meaningful to the Home Assistant integration's `select` entity and live in custom_components/neopool/const.py from v4.0.0 onwards. Library consumers that imported either dict must inline the mapping themselves.

### ✨ Features

* 💥 raise ValueError on invalid AUX relay index ([269b7df](https://github.com/Svasek/python-neopool-modbus/commit/269b7df600471003f8bca15d9a60f7e3a3033579))
* 💥 remove PERIOD_MAP / PERIOD_SECONDS_TO_KEY, mark library Production/Stable ([827fe3d](https://github.com/Svasek/python-neopool-modbus/commit/827fe3d9b6699234ac6fdb0cea3ef751f451e4cb))


### 🐛 Bug Fixes

* 🩹 grant publish-pypi job contents:write for asset upload ([cd48aed](https://github.com/Svasek/python-neopool-modbus/commit/cd48aedc6e23773f2dc8ad2017919e7390ca85ee))
* **client:** 🐛 fall through to device read when timer cache is incomplete ([c5268ad](https://github.com/Svasek/python-neopool-modbus/commit/c5268ad74240ad7ce8312ac2e8b6106dd9e94d1d))
* **client:** 🐛 move get_client() and total_writes bump into _perform_write_timer try block ([e261f47](https://github.com/Svasek/python-neopool-modbus/commit/e261f473c15fb7f0dd8d62f19f48755585322153))
* **client:** 🐛 verify isError() on EEPROM save and EXEC after timer write ([488e8c5](https://github.com/Svasek/python-neopool-modbus/commit/488e8c544cf822e277a5fb9bc19e11dd9b877526))
* **client:** 🐛 verify isError() on every AUX relay write ([d5598f4](https://github.com/Svasek/python-neopool-modbus/commit/d5598f42c65856515a4fa02e2327d34ec4a60676))


### ♻️ Refactoring

* ♻️ collapse aux relay set/clear if-else into ternary ([aff22fa](https://github.com/Svasek/python-neopool-modbus/commit/aff22fa19df400fced0da4dd538447053df24c30))


### 🎨 Style

* 🎨 collapse one-statement raise to single line ([974e709](https://github.com/Svasek/python-neopool-modbus/commit/974e709de10bb838863edd84549caf13ebe3be7a))
* 💄 fix lint findings in test files (B/RUF/SIM) ([25c743c](https://github.com/Svasek/python-neopool-modbus/commit/25c743ca414aecaff080c3c89d3253501db202fb))
* 💄 replace ambiguous unicode dashes with ASCII hyphens ([8fbbc38](https://github.com/Svasek/python-neopool-modbus/commit/8fbbc384a1fdf65404cee4d5a5246b4978ff1653))

## [0.2.0](https://github.com/Svasek/python-neopool-modbus/compare/v0.1.0...v0.2.0) (2026-06-06)


### ✨ Features

* ✨ add decoders module ([6c69762](https://github.com/Svasek/python-neopool-modbus/commit/6c6976269c31dc8c82937a8bc323045917c55599))
* ✨ add registers module ([37ac24c](https://github.com/Svasek/python-neopool-modbus/commit/37ac24cd33101ad50e506cc0d113619113bae1fc))
* ✨ add status_mask module ([211bf66](https://github.com/Svasek/python-neopool-modbus/commit/211bf660b29b346a1a701f280c7868d636f7a827))
* ✨ define public exception hierarchy and module API ([d17d9a6](https://github.com/Svasek/python-neopool-modbus/commit/d17d9a67d03b431487bebcd52869a81a78080f87))
* ✨ port NeoPoolModbusClient to library ([d130527](https://github.com/Svasek/python-neopool-modbus/commit/d1305273b4ade760b912f45e86f75645b66e3cd2))


### 🐛 Bug Fixes

* 🩹 remove unsupported `//` comment from pyrightconfig.json ([504efcb](https://github.com/Svasek/python-neopool-modbus/commit/504efcba31dc6f033c1ad0721c2f4c6d975c9a58))


### 🎨 Style

* 🎨 reflow long lines after modbus_acall inlining ([6fdc344](https://github.com/Svasek/python-neopool-modbus/commit/6fdc344d87f789c011ab44549a68130ad4af2f5a))

## [Unreleased]

### Added

- Initial public API — `NeoPoolModbusClient`, register address constants, exceptions.
- Extracted from the Home Assistant `neopool` integration.
