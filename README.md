# neopool-modbus

[![PyPI](https://img.shields.io/pypi/v/neopool-modbus.svg)](https://pypi.org/project/neopool-modbus/)
[![Python](https://img.shields.io/pypi/pyversions/neopool-modbus.svg)](https://pypi.org/project/neopool-modbus/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

[![Release](https://github.com/Svasek/python-neopool-modbus/actions/workflows/release.yaml/badge.svg)](https://github.com/Svasek/python-neopool-modbus/actions/workflows/release.yaml)
[![Unit Tests](https://github.com/Svasek/python-neopool-modbus/actions/workflows/test.yaml/badge.svg)](https://github.com/Svasek/python-neopool-modbus/actions/workflows/test.yaml)
[![Type Check](https://github.com/Svasek/python-neopool-modbus/actions/workflows/typecheck.yaml/badge.svg)](https://github.com/Svasek/python-neopool-modbus/actions/workflows/typecheck.yaml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/github/Svasek/python-neopool-modbus/graph/badge.svg)](https://app.codecov.io/github/Svasek/python-neopool-modbus)

[![Conventional Branch](https://img.shields.io/badge/Conventional%20Branch-Spec-6192c3)](https://conventional-branch.github.io/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://www.conventionalcommits.org/)
[![Gitmoji](https://img.shields.io/badge/gitmoji-%20%F0%9F%98%9C%20%F0%9F%98%8D-FFDD67.svg)](https://gitmoji.dev/specification)
[![Sponsor me](https://img.shields.io/badge/sponsor-❤-brightgreen?style=flat)](https://github.com/sponsors/svasek)
[![Ko-fi](https://img.shields.io/badge/ko--fi-support-29abe0?style=flat&logo=ko-fi)](https://ko-fi.com/svasek)

Async Python client for **Sugar Valley NeoPool** pool controllers (sold under
brands VistaPool, Hidrolife, Aquascenic, Oxilife, Hayward, Brilix, Bayrol)
connected via **Modbus TCP**.

This library is the communication layer extracted from the
[Home Assistant `neopool` integration](https://github.com/svasek/homeassistant-neopool-modbus)
and is suitable for any async Python project — Home Assistant integrations,
scripts, dashboards, or custom automation.

## Installation

```bash
pip install neopool-modbus
```

Requires Python 3.13+ and `pymodbus>=3.10.0` (installed transitively).

## Quick start

```python
import asyncio

from neopool_modbus import NeoPoolModbusClient


async def main() -> None:
    client = NeoPoolModbusClient(
        {"host": "192.168.1.42", "port": 502, "slave_id": 1}
    )
    try:
        data = await client.async_read_all()
        # Keys are the upstream Sugar Valley register names from
        # https://github.com/arendst/Tasmota/.../xsns_83_neopool.ino,
        # values are decoded into native Python types.
        print(f"pH:          {data['MBF_MEASURE_PH']}")           # e.g. 7.42
        print(f"Temperature: {data['MBF_MEASURE_TEMPERATURE']} °C")  # e.g. 27.3
        print(f"Hydrolysis:  {data['MBF_HIDRO_CURRENT']}")        # e.g. 6.5
    finally:
        await client.close()


asyncio.run(main())
```

The client is lazy — it opens the TCP connection on first use and reuses it
across calls; `close()` releases the socket and resets retry/backoff state.

## Public API

```python
from neopool_modbus import (
    NeoPoolModbusClient,
    NeoPoolError,
    NeoPoolConnectionError,
    NeoPoolModbusError,
    NeoPoolTimeoutError,
    async_probe_serial,
)
from neopool_modbus.registers import (
    DEFAULT_MODBUS_FRAMER,
    EXEC_REGISTER,
    EEPROM_SAVE_REGISTER,
    HEATING_SETPOINT_REGISTER,
    INTELLIGENT_SETPOINT_REGISTER,
    MANUAL_FILTRATION_REGISTER,
    TIMER_BLOCKS,
    is_valid_relay_gpio,
)
from neopool_modbus.decoders import (
    parse_timer_block,
    build_timer_block,
    hhmm_to_seconds,
    seconds_to_hhmm,
    get_machine_name,
    is_hydrolysis_in_percent,
    # ... see neopool_modbus.decoders for the full list
)
from neopool_modbus.status_mask import (
    decode_relay_state,
    decode_named_relay_states,
    decode_uv_lamp_state,
    decode_hidro_status_bits,
    decode_ion_status_bits,
    decode_ph_rx_cl_cd_status_bits,
)
```

All client methods translate underlying pymodbus exceptions into the
`NeoPoolError` hierarchy at the library boundary, so callers never need
to import `pymodbus` to catch errors:

| Class                    | Raised when                                                                      |
| ------------------------ | -------------------------------------------------------------------------------- |
| `NeoPoolConnectionError` | TCP connect fails, returned `False`, or the client is in its post-failure backoff |
| `NeoPoolTimeoutError`    | Connect, read, or write times out (`asyncio.TimeoutError`)                       |
| `NeoPoolModbusError`     | A read returns a Modbus exception response (`isError()` true), or `async_write_aux_relay` / one of the timer write follow-ups returns `isError()` |
| `NeoPoolError`           | Common base; catch this to handle any of the above                                |

> ⚠️ `NeoPoolModbusClient.async_write_register()` is the exception to the
> table above: it returns `None` (rather than raising) on `isError()` so
> existing callers in the Home Assistant integration keep working. A
> future major release will tighten this to raise `NeoPoolModbusError`
> for consistency.

```python
from neopool_modbus import NeoPoolError, NeoPoolModbusClient

client = NeoPoolModbusClient({"host": "192.168.1.42"})
try:
    data = await client.async_read_all()
except NeoPoolError as exc:
    # exc.__cause__ is the original pymodbus / asyncio exception, if any.
    print(f"NeoPool read failed: {exc}")
```

`ValueError` is still raised directly for programmer errors such as an
out-of-range AUX relay index — those are not transport failures.

## Features

- Async I/O on top of `pymodbus.AsyncModbusTcpClient`
- Batched register reads — one round-trip per protocol page, with
  notification-bit-driven cache invalidation so unchanged pages skip the read
- Exponential connection retry with bounded backoff
- Write-and-verify cycle for configuration registers
- Capability detection (hydrolysis, pH, Redox, chlorine, conductivity, ION)
- Strict type hints (`py.typed`), 100 % unit-test coverage

## Logging

The library uses a single logger named `neopool_modbus`. Enable it like any
other Python logger:

```python
import logging
logging.getLogger("neopool_modbus").setLevel(logging.DEBUG)
```

Home Assistant users can flip the integration's "Enable debug logging" toggle
in the UI; the integration's `manifest.json` lists `neopool_modbus` so the
toggle covers the library too.

## Based On

- [Tasmota NeoPool driver](https://github.com/arendst/Tasmota/blob/master/tasmota/tasmota_xsns_sensor/xsns_83_neopool.ino) — implements the NeoPool Modbus register protocol originally documented by Sugar Valley
- _NeoPool Control System MODBUS Register description_ — a Markdown transcription of the official Modbus register documentation by Sugar Valley (see [`docs/modbus-registers.md`](docs/modbus-registers.md))

## Disclaimer

This library is provided "AS IS" and without any warranty or guarantee of any kind.
The author takes no responsibility for any damage, loss, or malfunction resulting from the use or misuse of this code. Use at your own risk.

_This project is not affiliated with or endorsed by Sugar Valley, Hayward, or any other pool equipment manufacturer or distributor._

## License

Apache 2.0 — see [LICENSE](LICENSE).
