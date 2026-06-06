# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
