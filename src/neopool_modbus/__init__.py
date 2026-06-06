# Copyright 2026 Milos Svasek

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Async Python client for Sugar Valley NeoPool Modbus pool controllers.

The top-level package exposes only the high-level :class:`NeoPoolModbusClient`
and the public exception hierarchy.  Lower-level helpers are intentionally
kept in submodules to keep the public surface small:

- :mod:`neopool_modbus.registers`   - register addresses, bit masks, timer block layouts
- :mod:`neopool_modbus.decoders`    - register-value parsers and timer helpers
- :mod:`neopool_modbus.status_mask` - status register bit decoders
- :mod:`neopool_modbus.exceptions`  - exception hierarchy
"""

from __future__ import annotations

from .client import NeoPoolModbusClient
from .exceptions import (
    NeoPoolConnectionError,
    NeoPoolError,
    NeoPoolTimeoutError,
)

__version__ = "1.0.0"

__all__ = [
    "NeoPoolConnectionError",
    "NeoPoolError",
    "NeoPoolModbusClient",
    "NeoPoolTimeoutError",
    "__version__",
]
