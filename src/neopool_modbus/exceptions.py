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

"""Public exception hierarchy for ``neopool_modbus``.

These classes form a stable contract for callers of the library.  Internal
code currently raises :mod:`pymodbus` exceptions directly; future versions
may translate them into the classes defined here without breaking callers
that already catch :exc:`NeoPoolError`.
"""

from __future__ import annotations


class NeoPoolError(Exception):
    """Base class for all ``neopool_modbus`` errors."""


class NeoPoolConnectionError(NeoPoolError):
    """Raised when the TCP connection to the device fails or is lost."""


class NeoPoolTimeoutError(NeoPoolError):
    """Raised when a Modbus read or write operation times out."""


__all__ = [
    "NeoPoolConnectionError",
    "NeoPoolError",
    "NeoPoolTimeoutError",
]
