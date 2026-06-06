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

"""Modbus register addresses and protocol-level constants for NeoPool devices.

These values describe the device hardware and Modbus protocol; they are stable
specifications, not configuration. The Home Assistant integration consumes
them via re-export.
"""

from __future__ import annotations

# Default Modbus framer used when reading from a TCP gateway.
#   "tcp" -- standard Modbus TCP (MBAP header)
#   "rtu" -- RTU encoded over TCP (no MBAP, includes CRC)
DEFAULT_MODBUS_FRAMER = "tcp"

# Single-register write addresses with special semantics.
MANUAL_FILTRATION_REGISTER = 0x0413
EEPROM_SAVE_REGISTER = 0x02F0
EXEC_REGISTER = 0x02F5

# Command registers auto-clear to 0 after write; readback verification must be
# skipped for these.
COMMAND_REGISTERS = {EEPROM_SAVE_REGISTER, EXEC_REGISTER}

HEATING_SETPOINT_REGISTER = 0x0416  # MBF_PAR_HEATING_TEMP
INTELLIGENT_SETPOINT_REGISTER = 0x041C  # MBF_PAR_INTELLIGENT_TEMP

# MBF_RELAY_STATE has 7 relays (bits 0-6); MBF_PAR_*_RELAY_GPIO is 1-based.
MAX_RELAY_GPIO = 7


def is_valid_relay_gpio(gpio: int) -> bool:
    """Return True if the relay GPIO number is within the hardware range (1-based, 1-7)."""
    return 1 <= gpio <= MAX_RELAY_GPIO


# Timer blocks 0x0434-0x04E8 are read in groups of 15 registers due to the
# device's per-request limit.
TIMER_BLOCKS = {
    "filtration1": 0x0434,
    "filtration2": 0x0443,
    "filtration3": 0x0452,
    "relay_light": 0x0470,
    "relay_aux1": 0x04AC,
    "relay_aux1b": 0x0461,
    "relay_aux2": 0x04BB,
    "relay_aux2b": 0x047F,
    "relay_aux3": 0x04CA,
    "relay_aux3b": 0x048E,
    "relay_aux4": 0x04D9,
    "relay_aux4b": 0x049D,
}

__all__ = [
    "COMMAND_REGISTERS",
    "DEFAULT_MODBUS_FRAMER",
    "EEPROM_SAVE_REGISTER",
    "EXEC_REGISTER",
    "HEATING_SETPOINT_REGISTER",
    "INTELLIGENT_SETPOINT_REGISTER",
    "MANUAL_FILTRATION_REGISTER",
    "MAX_RELAY_GPIO",
    "TIMER_BLOCKS",
    "is_valid_relay_gpio",
]
