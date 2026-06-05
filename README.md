# neopool-modbus

[![PyPI](https://img.shields.io/pypi/v/neopool-modbus.svg)](https://pypi.org/project/neopool-modbus/)
[![Python](https://img.shields.io/pypi/pyversions/neopool-modbus.svg)](https://pypi.org/project/neopool-modbus/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/svasek/python-neopool-modbus/actions/workflows/ci.yaml/badge.svg)](https://github.com/svasek/python-neopool-modbus/actions/workflows/ci.yaml)

Async Python client for **Sugar Valley NeoPool** pool controllers (sold under
brands VistaPool, Hidrolife, Aquascenic, Oxilife, Hayward, Brilix, Bayrol)
connected via **Modbus TCP**.

This library is the communication layer extracted from the
[Home Assistant `neopool` integration](https://github.com/svasek/homeassistant-vistapool-modbus)
and is suitable for any Python project — Home Assistant, scripts, dashboards,
or custom automation.

## Status

🚧 **Alpha** — under active development. Public API may change before `1.0.0`.

## Installation

```bash
pip install neopool-modbus
```

Requires Python 3.13+ and `pymodbus>=3.10.0`.

## Quick start

```python
import asyncio

from neopool_modbus import NeoPoolModbusClient


async def main() -> None:
    client = NeoPoolModbusClient(host="192.168.1.42", port=502, slave_id=1)
    await client.connect()
    try:
        data = await client.read_all()
        print(data["measure_temperature"], data["measure_ph"])
    finally:
        await client.close()


asyncio.run(main())
```

## Features

- Async I/O on top of `pymodbus.AsyncModbusTcpClient`
- Batched register reads (single round-trip per register block)
- Write-and-verify mechanism for configuration registers
- Capability detection (hydrolysis, pH, Redox, chlorine, conductivity)
- Strict type hints (`py.typed`), 100 % test coverage

## License

Apache 2.0 — see [LICENSE](LICENSE).
