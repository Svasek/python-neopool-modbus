# Vistapool Control System - MODBUS Register Description

**Author:** Hayward technical department
**Date:** October 13th, 2023
**Version:** 10.23
**Manufacturer:** Hayward / Vistapool

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Register Description](#2-register-description)
   - 2.1 [Modbus Page (MODBUS)](#21-modbus-page-modbus)
   - 2.2 [Measures Page (MEASURE)](#22-measures-page-measure)
   - 2.3 [Global Page (GLOBAL)](#23-global-page-global)
   - 2.4 [Factory Page (FACTORY)](#24-factory-page-factory)
   - 2.5 [Installer Page (INSTALLER)](#25-installer-page-installer)
   - 2.6 [User Page (USER)](#26-user-page-user)
   - 2.7 [Miscellaneous Page (MISC)](#27-miscellaneous-page-misc)

---

## 1 Introduction

The Vistapool Control System is equipped with three ports, with a MODBUS protocol that allows a remote controller to adjust the different working parameters of the device.

The first port, labelled on the board as **"DISPLAY"**, is usually connected to the Screen Controller, which is itself a MODBUS master. The other port, labelled as **"RF/WIFI"**, is available for external communications.

A semaphore system has been implemented between all ports in order to manage register change requests happening simultaneously in both ports. However, the remote masters can always read any register concurrently.

The slave has the **MODBUS address 1** as default communication address, but it can be changed with a reserved procedure.

**Communication parameters for the RS485 asynchronous serial port:**

| Parameter | Value       |
| --------- | ----------- |
| Baud rate | 19200 bauds |
| Parity    | None        |
| Stop bits | 1           |

> **Warning:** The alteration of registers other than the ones described in this document could lead to a bad operation of the system, and in some cases, to an unrecoverable failure requiring technical assistance.

---

## 2 Register Description

The register set is divided into 7 different pages:

| Starting Address | Name      | Description                                                                                                                                                                   |
| ---------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0x0000           | MODBUS    | Manages general configuration of the box. This page is reserved for internal purposes.                                                                                        |
| 0x0100           | MEASURE   | Contains the different measurement information including hydrolysis current, pH level, redox level, etc.                                                                      |
| 0x0200           | GLOBAL    | Contains global information, such as the amount of time that each power unit has been working.                                                                                |
| 0x0300           | FACTORY   | Contains factory data such as calibration parameters for the different power units of the box.                                                                                |
| 0x0400           | INSTALLER | Contains a set of configuration registers related to the box installation, such as the relays used for each function, the amount of time that each pump must operate, etc.   |
| 0x0500           | USER      | Contains user configuration registers, such as the production level for the ionization and the hydrolysis, or the set points for the pH, redox, or chlorine regulation loops. |
| 0x0600           | MISC      | Contains the configuration parameters for the screen controllers (language, colours, sound, etc.).                                                                            |

Any modifications done over the registers should be made persistent by requesting an EEPROM storage. See [`MBF_SAVE_TO_EEPROM`](#register-0x02f0--mbf_save_to_eeprom) for more information.

---

## 2.1 Modbus Page (MODBUS)

### Register 0x0000 - `MBF_NODE_ADDR`

This register contains the current MODBUS slave address. Writing to this register changes the MODBUS address of the node.

The value of this register must be in the range of 1 to 240, both inclusive. Address 0 is reserved for sending broadcast messages to all devices.

When a write to this register occurs, the system must complete the write transaction by sending the response message, and only after that perform the change of the MODBUS address.

---

## 2.2 Measures Page (MEASURE)

### Register 0x0102 - `MBF_MEASURE_PH`

This register indicates the pH level measured in hundredths. A value of 700 indicates a pH of 7.00.

Reading this register is only valid if the pH module is enabled. To check the enable status of the pH module, see register `MBF_PH_STATUS`.

---

### Register 0x0103 - `MBF_MEASURE_RX`

This register indicates the redox/ORP level measured in hundredths of ppm. A value of 100 indicates a redox level of 1.00 ppm.

Reading this register is only valid if the Redox module is enabled. To check the enable status of the Redox module, see register `MBF_RX_STATUS`.

---

### Register 0x0104 - `MBF_MEASURE_CL`

This register indicates the chlorine concentration level measured in hundredths of ppm. A value of 100 indicates a chlorine level of 1.00 ppm.

Reading this register is only valid if the Chlorine module is enabled. To check the enable status of the chlorine module, see register `MBF_CL_STATUS`.

---

### Register 0x0105 - `MBF_MEASURE_CONDUCTIVITY`

This register indicates the conductivity level measured in the water.

Reading this register is only valid if the conductivity module is enabled. To check the enable status of the conductivity module, see register `MBF_CD_STATUS`.

---

### Register 0x0106 - `MBF_MEASURE_TEMPERATURE`

This register shows the temperature measured by the water temperature sensor. The measurement value is given in tenths of degrees Celsius. This means that a value of 200 means 20.0 °C.

---

### Register 0x0107 - `MBF_PH_STATUS`

This register contains the status of the pH control module. The register is a bit field with the following layout:

| Bits | Mask   | Description                                                                                                                                       |
| ---- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0-3  | 0x000F | pH alarm. The possible alarm values are described in the tables below depending on the regulation model.                                          |
| 10   | 0x0400 | pH module control state by flow detection (if enabled via `MBF_PAR_HIDRO_ION_CAUDAL`).                                                            |
| 11   | 0x0800 | Low pH pump relay on (pump active).                                                                                                               |
| 12   | 0x1000 | High pH pump relay on (pump active).                                                                                                              |
| 13   | 0x2000 | pH control module active and controlling pumps.                                                                                                   |
| 14   | 0x4000 | pH measurement module active and performing measurements. If this bit is set to 1, the pH bar must be shown on the screen.                        |
| 15   | 0x8000 | pH measurement module detected.                                                                                                                   |

Valid alarm values for pH regulation with acid and base:

| Alarm value | Description                                                                                                          |
| ----------- | -------------------------------------------------------------------------------------------------------------------- |
| 0           | No alarm.                                                                                                            |
| 1           | pH too high; the pH value is more than 0.8 points above the set point fixed in PH1.                                  |
| 2           | pH too low; the pH value is more than 0.8 points below the set point fixed in PH2.                                   |
| 3           | The pH pump (acid or base, indistinctly) has exceeded the operating time set by `MBF_PAR_RELAY_PH_MAX_TIME` and stopped. |
| 4           | The pH value is above the set point indicated in PH1.                                                                |
| 5           | The pH value is below the set point indicated in PH2.                                                                |

Valid alarm values for pH regulation with acid only:

| Alarm value | Description                                                                                                          |
| ----------- | -------------------------------------------------------------------------------------------------------------------- |
| 0           | No alarm.                                                                                                            |
| 1           | pH too high; the pH value is more than 0.8 points above the set point fixed in PH1.                                  |
| 2           | pH too low; the pH value is more than 0.8 points below the set point fixed in PH1.                                   |
| 3           | The pH pump has exceeded the operating time set by `MBF_PAR_RELAY_PH_MAX_TIME` and stopped.                          |
| 4           | The pH value is above the set point indicated in PH1 by 0.1.                                                         |
| 5           | The pH value is below the set point indicated in PH1 by 0.3.                                                         |

Valid alarm values for pH regulation with base only:

| Alarm value | Description                                                                                                          |
| ----------- | -------------------------------------------------------------------------------------------------------------------- |
| 0           | No alarm.                                                                                                            |
| 1           | pH too high; the pH value is more than 0.8 points above the set point fixed in PH2.                                  |
| 2           | pH too low; the pH value is more than 0.8 points below the set point fixed in PH2.                                   |
| 3           | The pH pump has exceeded the operating time set by `MBF_PAR_RELAY_PH_MAX_TIME` and stopped.                          |
| 4           | The pH value is above the set point indicated in PH2 by 0.1.                                                         |
| 5           | The pH value is below the set point indicated in PH2 by 0.3.                                                         |

---

### Register 0x0108 - `MBF_RX_STATUS`

This register contains the status of the Redox control module. The register is a bit field with the following layout:

| Bits | Mask   | Description                                                                                                                  |
| ---- | ------ | ---------------------------------------------------------------------------------------------------------------------------- |
| 12   | 0x1000 | Redox pump relay on (pump active).                                                                                           |
| 13   | 0x2000 | Redox control module active and controlling the pump.                                                                        |
| 14   | 0x4000 | Redox measurement module active and performing measurements. If this bit is set to 1, the Redox bar must be shown on screen. |
| 15   | 0x8000 | Redox measurement module detected in the system.                                                                             |

---

### Register 0x0109 - `MBF_CL_STATUS`

This register contains the status of the chlorine control module. The register is a bit field with the following layout:

| Bits | Mask   | Description                                                                                                                                                                         |
| ---- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 3    | 0x0008 | Flow sensor of the chlorine probe. This sensor is built into the probe itself and detects whether water is passing through the chlorine measurement probe. If this bit is 0, the chlorine measurement is not valid. |
| 12   | 0x1000 | Chlorine pump relay on (pump active).                                                                                                                                               |
| 13   | 0x2000 | Chlorine control module active and controlling the pump.                                                                                                                            |
| 14   | 0x4000 | Chlorine measurement module active and performing measurements. If this bit is set to 1, the chlorine bar must be shown on screen.                                                  |
| 15   | 0x8000 | Chlorine measurement module detected in the system.                                                                                                                                 |

---

### Register 0x010A - `MBF_CD_STATUS`

This register contains the status of the conductivity control module. The register is a bit field with the following layout:

| Bits | Mask   | Description                                                                                                                                |
| ---- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 12   | 0x1000 | Conductivity pump relay on (pump active).                                                                                                  |
| 13   | 0x2000 | Conductivity control module active and controlling the pump.                                                                               |
| 14   | 0x4000 | Conductivity measurement module active and performing measurements. If this bit is set to 1, the conductivity bar must be shown on screen. |
| 15   | 0x8000 | Conductivity measurement module detected in the system.                                                                                    |

---

### Register 0x010D - `MBF_HIDRO_STATUS`

This register contains the status of the hydrolysis control module. The register is a bit field with the following layout:

| Bit | Mask   | Description                                                                                |
| --- | ------ | ------------------------------------------------------------------------------------------ |
| 0   | 0x0001 | On Target — the system has reached the configured set point.                               |
| 1   | 0x0002 | Low — the hydrolysis cannot reach the configured set point.                                |
| 2   | 0x0004 | Elec — Reserved.                                                                           |
| 3   | 0x0008 | Flow — Flow indicator of the hydrolysis cell (FL1).                                        |
| 4   | 0x0010 | Cover — Cover input active.                                                                |
| 5   | 0x0020 | Active — Hydrolysis module active (`hidroEnable`).                                         |
| 6   | 0x0040 | Control — Hydrolysis module operating with regulation (`hidroControlEnable`).              |
| 7   | 0x0080 | Redox enable — Hydrolysis activation by the Redox module (`rx_hen`).                       |
| 8   | 0x0100 | Hidro shock enabled — Chlorine shock mode active.                                          |
| 9   | 0x0200 | FL2 — Flow indicator of the chlorine probe, if present.                                    |
| 10  | 0x0400 | Cl enable — Hydrolysis activation by the chlorine module (`cl_hen`).                       |
| 11  | 0x0800 | Unused.                                                                                    |
| 12  | 0x1000 | Ion Pol off — Ionization in dead time.                                                     |
| 13  | 0x2000 | Ion Pol 1 — Ionization operating in polarization 1.                                        |
| 14  | 0x4000 | Ion Pol 2 — Ionization operating in polarization 2.                                        |
| 15  | 0x8000 | Unused.                                                                                    |

---

### Register 0x010E - `MBF_RELAY_STATE`

This register contains the state of every configurable relay:

| Bit | Mask   | Description                                                            |
| --- | ------ | ---------------------------------------------------------------------- |
| 0   | 0x0001 | State of relay 1 (1 = on; 0 = off) (typically assigned to pH).         |
| 1   | 0x0002 | State of relay 2 (1 = on; 0 = off) (typically assigned to filtration). |
| 2   | 0x0004 | State of relay 3 (1 = on; 0 = off) (typically assigned to lighting).   |
| 3   | 0x0008 | State of relay 4.                                                      |
| 4   | 0x0010 | State of relay 5.                                                      |
| 5   | 0x0020 | State of relay 6.                                                      |
| 6   | 0x0040 | State of relay 7.                                                      |

---

## 2.3 Global Page (GLOBAL)

### Registers 0x0206 / 0x0207 - `MBF_PAR_HIDRO_WORK_TIME_LOW` / `MBF_PAR_HIDRO_WORK_TIME_HIGH`

This set of two registers contains the number of seconds that the chlorination cell has been working since the device was manufactured. The two registers must be read consecutively to build a 32-bit unsigned integer with the time.

This counter must not be erased as it is used to estimate the lifetime of the device.

---

### Registers 0x0208 / 0x0209 - `MBF_PAR_PARTIAL_HIDRO_WORK_TIME_LOW` / `MBF_PAR_PARTIAL_HIDRO_WORK_TIME_HIGH`

This set of two registers contains the number of seconds that the chlorination cell has been working since the counter was reset (partial counter). The two registers must be read consecutively to build a 32-bit unsigned integer with the time.

This counter is reset each time the cell is changed by the installer and it is used to estimate the total working time of a cell.

---

### Register 0x02F0 - `MBF_SAVE_TO_EEPROM`

A write operation to this register with value `1` starts an EEPROM storage operation immediately. During the EEPROM storage procedure, the system may be unresponsive to MODBUS requests. The operation will always last less than 1 second.

EEPROM write operations occur periodically every 10 minutes. However, after modifying a MODBUS configuration register it is recommended to force a write operation, since this is the only secure way to keep the information if the box is switched off before the periodic EEPROM write operation automatically occurs.

However, since the EEPROM write operations are limited by the number of cycles that the EEPROM memory itself can be written, it is recommended to write all the needed modifications into the registers and then, when all the registers have been properly written, call the EEPROM write operation.

> **Warning:** The number of EEPROM write operations is guaranteed to be 100,000 cycles. Once this number of cycles is exceeded we cannot guarantee a safe storage of the information.

---

### Register 0x02F1 - `MBF_CLEAR_EEPROM`

A write operation to this register (with any value) restores the register memory to its factory default state immediately. This operation does **not** store the values into non-volatile EEPROM memory. To store the contents of the factory default state, a `MBF_SAVE_TO_EEPROM` operation has to be executed.

---

### Register 0x02F2 - `MBF_RESET_USER_COUNTERS`

A write operation to this register (with any value) resets the user time counters:

- `MBF_PAR_PARTIAL_HIDRO_WORK_TIME`
- `MBF_PAR_PARTIAL_ION_WORK_TIME`
- `MBF_PAR_PARTIAL_UV_WORK_TIME`

These counters are associated with the user-level access.

This operation does **not** store the values into non-volatile EEPROM memory. To store the contents of the factory default state, a `MBF_SAVE_TO_EEPROM` operation has to be executed.

---

### Register 0x02F4 - `MBF_STOP_ALL_MODULES`

A write operation to this register (with any value) stops the operation of all modules. The following operational functions are affected:

- Hydrolysis / Chlorination
- Ionization
- pH, ORP, Conductivity and chlorine control
- Ultraviolet water depuration
- Filtration pump control
- All auxiliary relays

The operation of all those functions can be relaunched by means of the `MBF_RESTART_MODULES` register.

---

### Register 0x02F5 - `MBF_RESTART_MODULES`

A write operation to this register (with any value) restarts the operation of all function modules of the device. The following operational functions are affected:

- Hydrolysis / Chlorination
- Ionization
- pH, ORP, Conductivity and chlorine control
- Ultraviolet water depuration
- Filtration pump control
- All auxiliary relays

It is recommended to relaunch all modules if a parameter change has taken place, like filtration scheduler programming, filtration mode, etc.

---

## 2.4 Factory Page (FACTORY)

### Register 0x0300 - `MBF_PAR_VERSION`

This register contains the software version of the PowerBox device.

> Not used.

---

### Register 0x0323 - `MBF_PAR_HIDRO_FLOW_SIGNAL`

> Note: only Fanless equipment.

This register selects the operation of the flow detection signal associated with the hydrolysis function.

The possible values for this register are:

| Value | Identifier                                       | Description                                                                                                                                                                                                                       |
| ----- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | `MBV_PAR_HIDRO_FLOW_SIGNAL_STD`                  | Standard detection based on the conduction between an auxiliary electrode and either of the two cell electrodes.                                                                                                                  |
| 1     | `MBV_PAR_HIDRO_FLOW_SIGNAL_ALWAYS_ON`            | Always on. This value forces the generation of the hydrolysis current even if no flow is detected on the sensor.                                                                                                                  |
| 2     | `MBV_PAR_HIDRO_FLOW_SIGNAL_PADDLE`               | Detection based on the paddle switch, associated with the FL1 input.                                                                                                                                                              |
| 3     | `MBV_PAR_HIDRO_FLOW_SIGNAL_PADDLE_AND_STD`       | Detection based on the paddle switch (FL1 input) **and** the standard detector. The system considers there is flow only when both elements detect flow. If either of them opens, the hydrolysis is stopped.                       |
| 4     | `MBV_PAR_HIDRO_FLOW_SIGNAL_PADDLE_OR_STD`        | Detection based on the paddle switch (FL1 input) **or** the standard detector. The system considers there is flow when either of the two elements detects flow. The hydrolysis only stops if both detectors report no flow.       |

The default value for this register is 0 (standard detection).

To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

## 2.5 Installer Page (INSTALLER)

### Register 0x0403 - `MBF_PAR_EXT_CTRL`

This register configures the external control mode of ionization, hydrolysis and pumps. It is a bit mask, and its operation is governed by the bits that are active.

| Bit | Mask   | Identifier            | Description                                                                                                                                                              |
| --- | ------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0   | 0x0001 | `FL1_CTRL`            | If the FL1 signal is detected as inactive, the actuation of the different elements of the system is disabled.                                                            |
| 1   | 0x0002 | `FL2_CTRL`            | If the FL2 signal is detected as inactive, the actuation of the different elements of the system is disabled.                                                            |
| 2   | 0x0004 | `FULL_CL_HIDRO_CTRL`  | If a chlorine module is installed and its flow sensor is detected inactive, the actuation of the different elements of the system is disabled.                           |
| 3   | 0x0008 | `SLAVE`               | The slave input value is taken; if it is inactive, the actuation of the different elements of the system is disabled.                                                    |
| 4   | 0x0010 | `PADDLE_SWITCH`       | Paddle switch.                                                                                                                                                           |
| 5   | 0x0020 | `PADDLE_SWITCH_INV`   | Inverted paddle switch.                                                                                                                                                  |
| 6   | 0x0080 | `INVERSION`           | This bit determines whether "active" means open or closed for the electrical input signals, and inverts the operation — for example to implement a paddle switch that closes when there is no flow. |

To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0404 - `MBF_PAR_HIDRO_MODE`

This register configures the external control mode of the hydrolysis from the measurement modules.

| Value | Description                |
| ----- | -------------------------- |
| 0     | No control.                |
| 1     | Standard control (on/off). |
| 2     | With timed pump.           |

---

### Register 0x0405 - `MBF_PAR_HIDRO_POL0`

This register stores the time the unit must remain operating in positive polarization in the hydrolysis/electrolysis. The time is stored in minutes.

To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0406 - `MBF_PAR_HIDRO_POL1`

This register stores the time the unit must remain operating in negative polarization in the hydrolysis/electrolysis. The time is stored in minutes.

To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0407 - `MBF_PAR_HIDRO_POL2`

This register stores the time the unit must remain in dead time (delivering no power) in the hydrolysis/electrolysis. The time is stored in minutes.

To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Registers 0x0408 / 0x0409 - `MBF_PAR_TIME_LOW` / `MBF_PAR_TIME_HIGH`

These two registers operate as a 32-bit time counter. This counter holds the system time, measured in seconds elapsed since January 1st, 1970 (known as "Epoch").

---

### Register 0x040A - `MBF_PAR_PH_ACID_RELAY_GPIO`

Number of the relay assigned to the acid-pump function (only with pH modules).

---

### Register 0x040B - `MBF_PAR_PH_BASE_RELAY_GPIO`

Number of the relay assigned to the base-pump function (only with pH modules).

---

### Register 0x040C - `MBF_PAR_RX_RELAY_GPIO`

This register stores which of the 7 available relays is assigned to the Redox-level regulation function. If the value is 0, no relay is assigned and therefore there is no pump function (ON/OFF must not be displayed).

To know whether this relay is activated or not, there are two ways:

- **Way 1:** check the `MBMSK_RX_STATUS_RELAY` bit in the `MBF_RX_STATUS` register.
- **Way 2:** compute the bit assigned to the relay in `MBF_RELAY_STATE` and check whether that relay is active.

---

### Register 0x040D - `MBF_PAR_CL_RELAY_GPIO`

Number of the relay assigned to the chlorine-pump function (only with free-chlorine measurement modules).

---

### Register 0x040E - `MBF_PAR_CD_RELAY_GPIO`

Number of the relay assigned to the conductivity (brine) pump function (only with conductivity measurement modules).

---

### Register 0x040F - `MBF_PAR_TEMPERATURE_ACTIVE`

Indicates whether the unit has temperature measurement (1) or not (0).

---

### Register 0x0410 - `MBF_PAR_LIGHTING_GPIO`

Number of the relay assigned to the lighting function. `0` = inactive.

---

### Register 0x0411 - `MBF_PAR_FILT_MODE`

This register stores the filtration mode of the unit.

| Value | Identifier      | Description                                                                                                                                                                                                                                                                                |
| ----- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0     | `MANUAL`        | Always available. Allows turning filtration (and all other systems that depend on it) on and off manually.                                                                                                                                                                                 |
| 1     | `AUTO`          | Always available. Turns filtration on and off according to the configuration of timers TIMER1, TIMER2 and TIMER3.                                                                                                                                                                          |
| 2     | `HEATING`       | Similar to AUTO mode, but additionally includes the heating-temperature configuration. This mode is only enabled if `MBF_PAR_HEATING_MODE` is set to a non-zero value and a heating relay is assigned.                                                                                     |
| 3     | `SMART`         | This filtration mode adjusts the pump operating times based on the temperature. This mode is only enabled if `MBF_PAR_TEMPERATURE_ACTIVE` is set to 1.                                                                                                                                     |
| 4     | `INTELLIGENT`   | Performs an intelligent filtration process in combination with the heating function. This mode is only enabled if `MBF_PAR_HEATING_MODE` is set to a non-zero value and a heating relay is assigned.                                                                                       |
| 13    | `BACKWASH`      | This filter mode is started when the backwash operation is activated.                                                                                                                                                                                                                      |
| 14    | `CHLORINATION SHOCK` | This filter mode is started when the chlorination shock operation is activated.                                                                                                                                                                                                       |

The following sections describe each of the filtration modes in detail.

#### Mode 0: MANUAL

This mode allows manually turning the filtration process on and off. There are no timers or additional functions.

#### Mode 1: AUTOMATIC (or timed)

In this mode, filtration is started according to a set of timers that allow adjusting the start and end time of filtration. The timers always operate on a daily basis.

#### Mode 2: HEATING (timed) with optional CLIMATE

This mode operates the same way as the AUTO mode, but additionally includes the option of operating a relay that is activated or deactivated as a function of the temperature. The temperature set point is fixed in this menu, and the system operates with a 1-degree hysteresis.

Additionally, there is a CLIMATE option (shown on the screen as "CLIMA" on/off). This option keeps filtration on after the configured filtration period has elapsed if the temperature is below the set point. When the set point is reached, filtration stops and does not start again until the next period.

> Hysteresis example: if the set-point temperature is 23 °C, the system will activate when the temperature drops below 22 °C and will not stop until it rises above 23 °C.

> Note: this mode is only visible when the option to use a temperature probe is active and heating is enabled.

This mode also turns filtration on automatically when the water temperature is below a set-point temperature. As with the heating mode, the system operates with a 1-degree hysteresis.

> Note: this mode is only visible when the option to use a temperature probe is active.

#### Mode 3: SMART

This mode is based on the AUTO (timed) mode, with its three filtration intervals, but adjusting the filtration times based on the temperature.

For this purpose, two temperature parameters are provided: the maximum temperature, above which the filtration times will be those set by the timers, and the minimum temperature, at which the filtration is reduced to 5 minutes (the minimum operating time). Between these two temperatures the filtration times scale linearly.

Additionally, an antifreeze mode option is available, which turns filtration on if the system temperature drops below 2 degrees.

> Note: this mode is only visible when the option to use a temperature probe is active.

#### Mode 4: INTELLIGENT

This is the most complex filtration mode. Both the temperature and the heating intervene.

In this mode the user has two operating parameters:

- Desired temperature.
- Minimum filtration time (minimum value 2 hours, maximum value 24 hours), `Tfilt`.

The behaviour is as follows:

- The unit starts filtration every 2 hours.
- The minimum filtration time is divided into 12 fragments (`Tfon = Tfilt / 12`).
- A variable called `Tbonus = Tfilt − 2 hours` is created.

After 10 minutes the system starts deducting time from `Tbonus`. If `Tbonus` is exhausted, filtration stops.

After `Tfon`, the temperature is measured (filtration will have run at least the first 10 minutes to allow enough water to flow through the filtration circuit). If the temperature is at or above the set-point temperature, filtration stops.

If, on the contrary, the temperature is below the set point, filtration remains active and the time is deducted from `Tbonus`.

Filtration will run at least 10 minutes every two hours of the day to verify the temperature. Therefore filtration in intelligent mode will run a minimum of 2 hours per day (10 minutes × 12 starts per day).

The customer must select MINIMUM FILTRATION HOURS. For example: 10 hours. That time is divided across the 12 daily filtration starts used to check temperature. Example: 10 hours × 60 minutes / 12 = 50 minutes every 2 hours. THIS IS THE FILTRATION TIME EVERY 2 HOURS. Of those 50 minutes, 10 minutes are mandatory and 40 minutes are deducted if pool heating must be activated at some point.

> Note: this mode is only visible when the option to use a temperature probe is active.

---

### Register 0x0412 - `MBF_PAR_FILT_GPIO`

Relay selected to perform the filtration function (default: relay 2). When this value is zero, no relay is assigned and therefore the unit does not control filtration. In that case, the filtration option does not appear in the user menu.

---

### Register 0x0413 - `MBF_PAR_FILT_MANUAL_STATE`

Filtration state in manual mode (1 = on, 0 = off).

---

### Register 0x0414 - `MBF_PAR_HEATING_MODE`

Heating mode.

| Value | Description                                       |
| ----- | ------------------------------------------------- |
| 0     | The unit has no heating.                          |
| 1     | The unit has heating.                             |
| 2     | The unit has a heat/cool pump (dual set point).   |

---

### Register 0x0415 - `MBF_PAR_HEATING_GPIO`

Relay selected to perform the heating function (default: relay 7). When this value is zero, no relay is assigned and therefore the unit does not control heating. In that case, the filtration modes associated with heating are not shown.

---

### Register 0x0416 - `MBF_PAR_HEATING_TEMP`

Set point for the heating swimming-pool unit. This register holds **two** different set points, one for the heating and another one for the cooling adjustment.

| Bits | Mask   | Description                                                                                          |
| ---- | ------ | ---------------------------------------------------------------------------------------------------- |
| 0-7  | 0x00FF | Low-temperature threshold value. Used to start the water-temperature conditioning system in heating mode. |
| 8-15 | 0xFF00 | High-temperature threshold value. Used to start the water-temperature conditioning system in cooling mode. |

If the system is being used in heating mode (`MBF_PAR_HEATING_MODE = 1`), only the lower part of the 16-bit word is used.

The values specified in this register have to be coded in full Celsius degrees. This means that if the master wants to store a 20 °C set point for the lower temperature threshold, the value to be written is `0x0014`.

---

### Register 0x0417 - `MBF_PAR_CLIMA_ONOFF`

Activation of the climate mode (0 = inactive, 1 = active).

---

### Register 0x0418 - `MBF_PAR_SMART_TEMP_HIGH`

Upper temperature for the Smart mode.

---

### Register 0x0419 - `MBF_PAR_SMART_TEMP_LOW`

Lower temperature for the Smart mode.

---

### Register 0x041A - `MBF_PAR_SMART_ANTI_FREEZE`

Antifreeze mode enabled (1) or not (0). This adjustment is only available in the Smart filtration mode.

---

### Register 0x041B - `MBF_PAR_SMART_INTERVAL_REDUCTION`

This register is read-only and reports to the outside what percentage (0 to 100 %) is being applied to the nominal filtration time. 100 % means the full programmed time is being filtered.

---

### Register 0x041C - `MBF_PAR_INTELLIGENT_TEMP`

Set-point temperature for the intelligent mode.

---

### Register 0x041D - `MBF_PAR_INTELLIGENT_FILT_MIN_TIME`

Minimum filtration time in minutes.

---

### Register 0x041E - `MBF_PAR_INTELLIGENT_BONUS_TIME`

Bonus time for the current set of intervals.

---

### Register 0x041F - `MBF_PAR_INTELLIGENT_TT_NEXT_INTERVAL`

Time to next filtration interval. When it reaches 0, an interval is started and the number of seconds for the next interval is reloaded (`2 × 3600`).

---

### Register 0x0420 - `MBF_PAR_INTELLIGENT_INTERVALS`

Number of started intervals. When it reaches 12, it is reset to 0 and the bonus time is reloaded with the value of `MBF_PAR_INTELLIGENT_FILT_MIN_TIME`.

---

### Register 0x0421 - `MBF_PAR_FILTRATION_STATE`

Filtration function state. This register is read-only and exposes the current state of the filtration procedure: 0 is off and 1 is on.

The filtration state is regulated according to the `MBF_PAR_FILT_MANUAL_STATE` register if the filtration mode held in register `MBF_PAR_FILT_MODE` is set to `FILT_MODE_MANUAL` (0).

---

### Register 0x042A - `MBF_PAR_PH_PUMP_REP_TIME_ON`

This function stores the time that the pH pump will be turned on in repetitive mode.

| Bits | Mask   | Description                                                          |
| ---- | ------ | -------------------------------------------------------------------- |
| 0-14 | 0x7FFF | Time mask. Time level for the pump.                                  |
| 15   | 0x8000 | `MBMSK_PH_PUMP_REPETITIVE`. If this bit is active, the pH pump operates in repetitive mode. |

The time level has a special coding format. It can cover periods of 1 to 180 seconds with 1-second granularity and from 3 to 999 minutes with 1-minute granularity.

If the value is set to 30 for example, a 30-second time will be considered. If the value is 200, the on time will be `(200 − 180 + 3) = 23 minutes`.

---

### Register 0x042B - `MBF_PAR_PH_PUMP_REP_TIME_OFF`

This function stores the time that the pH pump will be turned off in repetitive mode. This register contains the time-level quantity and has no upper configuration bits.

The time level has the same special coding format as `MBF_PAR_PH_PUMP_REP_TIME_ON`. It can cover periods of 1 to 180 seconds with 1-second granularity and from 3 to 999 minutes with 1-minute granularity.

If the value is set to 30, a 30-second time will be considered. If the value is 200, the off time will be `(200 − 180 + 3) = 23 minutes`.

---

### Register 0x042C - `MBF_PAR_HIDRO_COVER_ENABLE`

This register holds the options for the hydrolysis/electrolysis module.

| Bit | Mask   | Identifier                                |
| --- | ------ | ----------------------------------------- |
| 0   | 0x0001 | `MBMSK_HIDRO_COVER_ENABLE`                |
| 1   | 0x0002 | `MBMSK_HIDRO_TEMPERATURE_SHUTDOWN_ENABLE` |

If the cover-enable option is active, the hydrolysis/electrolysis production will be reduced by a given percentage specified in the lower half of the `MBF_PAR_HIDRO_COVER_REDUCTION` register when the cover input is detected.

If the temperature-shutdown option is enabled, the hydrolysis/electrolysis production will stop when the temperature falls below a given temperature threshold specified in the higher part of the `MBF_PAR_HIDRO_COVER_REDUCTION` register.

---

### Register 0x042D - `MBF_PAR_HIDRO_COVER_REDUCTION`

This register holds the configured levels for the cover reduction and the hydrolysis shutdown temperature options.

| Bits | Mask   | Identifier                       | Description                                  |
| ---- | ------ | -------------------------------- | -------------------------------------------- |
| 0-7  | 0x00FF | `MBMSK_HIDRO_COVER_REDUCTION`    | Percentage for the cover reduction.          |
| 8-15 | 0xFF00 | `MBMSK_HIDRO_SHUTDOWN_TEMPERATURE` | Temperature level for the hydrolysis shutdown. |

---

### Register 0x042E - `MBF_PAR_PUMP_RELAY_TIME_OFF`

This register holds the time level in minutes or seconds that the dosing pump must remain off when the temporized pump mode is selected. This time-level register applies to all pumps except pH.

The time level has a special coding format. It can cover periods of 1 to 180 seconds with 1-second granularity and from 3 to 999 minutes with 1-minute granularity.

If the value is set to 30, a 30-second time will be considered. If the value is 200, the off time will be `(200 − 180 + 3) = 23 minutes`.

---

### Register 0x042F - `MBF_PAR_PUMP_RELAY_TIME_ON`

This register holds the time level in minutes or seconds that the dosing pump must remain on when the temporized pump mode is selected. This time-level register applies to all pumps except pH.

The time level has a special coding format. It can cover periods of 1 to 180 seconds with 1-second granularity and from 3 to 999 minutes with 1-minute granularity.

If the value is set to 30, a 30-second time will be considered. If the value is 200, the on time will be `(200 − 180 + 3) = 23 minutes`.

---

### Register 0x0430 - `MBF_PAR_SETPOINT_MODE`

Determines the regulation configuration of the different modules of the unit.

| Bits | Mask   | Identifier                   | Description                              |
| ---- | ------ | ---------------------------- | ---------------------------------------- |
| 0-2  | 0x0007 | `MBMSK_PAR_SETPOINT_MODE_PH` | Regulation mode for the pH module.       |
| 3-5  | 0x0038 | `MBMSK_PAR_SETPOINT_MODE_RX` | Regulation mode for the ORP (Redox) module. |
| 6-8  | 0x01C0 | `MBMSK_PAR_SETPOINT_MODE_CL` | Regulation mode for the chlorine module. |
| 9-11 | 0x0E00 | `MBMSK_PAR_SETPOINT_MODE_CD` | Regulation mode for the conductivity module. |

**pH set-point available modes:**

| Value | Identifier                                       | Description                                                                                                  |
| ----- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| 0     | `MBV_PAR_RELAY_PH_ACID_AND_BASE`                 | The unit operates with both acid and base pumps.                                                             |
| 1     | `MBV_PAR_RELAY_PH_ACID_ONLY`                     | The unit operates with the acid pump only.                                                                   |
| 2     | `MBV_PAR_RELAY_PH_BASE_ONLY`                     | The unit operates with the base pump only.                                                                   |
| 3     | `MBV_PAR_SETPOINT_MODE_PH_ACID_BASE_SINGLE_REL`  | The unit turns on the assigned relay when the pH measurement is outside the range set by the two pH set points. |
| 4     | `MBV_PAR_SETPOINT_MODE_PH_HYST_NEG`              | The pH module operates in negative-hysteresis mode.                                                          |
| 5     | `MBV_PAR_SETPOINT_MODE_PH_HYST_POS`              | The pH module operates in positive-hysteresis mode.                                                          |

**Redox set-point available modes:**

| Value | Identifier                                       | Description                                                                                                  |
| ----- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| 0     | `MBV_PAR_SETPOINT_MODE_RX_UP_ONLY`               | The system operates traditionally. The assigned relay is activated when the measurement falls below the threshold set by RX1. |
| 1     | —                                                | Reserved.                                                                                                    |
| 2     | —                                                | Reserved.                                                                                                    |
| 3     | `MBV_PAR_SETPOINT_MODE_RX_UP_DOWN_SINGLE_REL`    | The unit turns on the assigned relay when the Redox measurement is outside the range set by the two set points RX1 and RX2. |
| 4     | `MBV_PAR_SETPOINT_MODE_RX_HYST_NEG`              | The Redox module operates in negative-hysteresis mode.                                                       |
| 5     | `MBV_PAR_SETPOINT_MODE_RX_HYST_POS`              | The Redox module operates in positive-hysteresis mode.                                                       |

**Chlorine set-point available modes:**

| Value | Identifier                                       | Description                                                                                                  |
| ----- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| 0     | `MBV_PAR_SETPOINT_MODE_CL_UP_ONLY`               | The system operates traditionally. The assigned relay is activated when the measurement falls below the threshold set by CL1. |
| 1     | —                                                | Reserved.                                                                                                    |
| 2     | —                                                | Reserved.                                                                                                    |
| 3     | `MBV_PAR_SETPOINT_MODE_CL_UP_DOWN_SINGLE_REL`    | The unit turns on the assigned relay when the chlorine measurement is outside the range set by the two set points CL1 and CL2. |
| 4     | `MBV_PAR_SETPOINT_MODE_CL_HYST_NEG`              | The chlorine module operates in negative-hysteresis mode.                                                    |
| 5     | `MBV_PAR_SETPOINT_MODE_CL_HYST_POS`              | The chlorine module operates in positive-hysteresis mode.                                                    |

**Conductivity set-point available modes:**

| Value | Identifier                                       | Description                                                                                                  |
| ----- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| 0     | `MBV_PAR_SETPOINT_MODE_CD_UP_ONLY`               | The system operates traditionally. The assigned relay is activated when the measurement falls below the threshold set by CD1. |
| 1     | —                                                | Reserved.                                                                                                    |
| 2     | —                                                | Reserved.                                                                                                    |
| 3     | `MBV_PAR_SETPOINT_MODE_CD_UP_DOWN_SINGLE_REL`    | The unit turns on the assigned relay when the conductivity measurement is outside the range set by the two set points CD1 and CD2. |
| 4     | `MBV_PAR_SETPOINT_MODE_CD_HYST_NEG`              | The conductivity module operates in negative-hysteresis mode.                                                |
| 5     | `MBV_PAR_SETPOINT_MODE_CD_HYST_POS`              | The conductivity module operates in positive-hysteresis mode.                                                |

---

### Register 0x0431 - `MBF_PAR_RELAY_MAX_TIME`

This function holds the maximum amount of time, in seconds, that a dosing pump can operate before raising an alarm signal. The behavior of the system when the dosing time is exceeded is regulated by the type of action stored in the `MBF_PAR_RELAY_MODE` register.

---

### Register 0x0432 - `MBF_PAR_RELAY_MODE`

This register holds the behavior of the system when the dosing time is exceeded.

| Bits | Mask   | Field | Description                          |
| ---- | ------ | ----- | ------------------------------------ |
| 0-1  | 0x0003 | pH    | Behavior for the pH module.          |
| 2-3  | 0x000C | Rx    | Behavior for the Redox/ORP module.   |
| 4-5  | 0x0030 | Cl    | Behavior for the chlorine module.    |
| 6-7  | 0x00C0 | Cd    | Behavior for the conductivity module. |

The possible values for each field are:

| Value | Identifier                          | Description                                                          |
| ----- | ----------------------------------- | -------------------------------------------------------------------- |
| 0     | `MBV_PAR_RELAY_MODE_IGNORE`         | The system simply ignores the alarm and dosing continues.            |
| 1     | `MBV_PAR_RELAY_MODE_SHOW_ONLY`      | The system only shows the alarm on screen, but dosing continues.     |
| 2     | `MBV_PAR_RELAY_MODE_SHOW_AND_STOP`  | The system shows the alarm on screen and stops the dosing pump.      |

---

### Register 0x0433 - `MBF_PAR_RELAY_ACTIVATION_DELAY`

This register holds the delay time in seconds for the pH pump when the measured pH value is outside the allowable pH set points. The system internally adds an extra time of 10 seconds to the value stored here.

The pump starts the dosing operation once the condition of pH out of valid interval is maintained during the time specified in this register.

---

### Registers 0x0434 … 0x04E7 - `MBF_PAR_TIMER_BLOCK_BASE`

This block of 180 registers holds the configuration of the system timers. The system has a set of 12 fully configurable timers, each one assigned to a specific function, described below:

| Timer number | Timer base reg. | Assigned function                    |
| ------------ | --------------- | ------------------------------------ |
| 0            | 0x0434          | Filtration interval 1                |
| 1            | 0x0443          | Filtration interval 2                |
| 2            | 0x0452          | Filtration interval 3                |
| 3            | 0x0461          | Auxiliary relay 1 — Second interval  |
| 4            | 0x0470          | Lighting interval                    |
| 5            | 0x047F          | Auxiliary relay 2 — Second interval  |
| 6            | 0x048E          | Auxiliary relay 3 — Second interval  |
| 7            | 0x049D          | Auxiliary relay 4 — Second interval  |
| 8            | 0x04AC          | Auxiliary relay 1 — First interval   |
| 9            | 0x04BB          | Auxiliary relay 2 — First interval   |
| 10           | 0x04CA          | Auxiliary relay 3 — First interval   |
| 11           | 0x04D9          | Auxiliary relay 4 — First interval   |

Each block of 15 registers configures one single timer. The 15 registers are defined as follows:

| Register offset | Identifier                | Description                                                                                                    |
| --------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 0               | `OFFMB_TIMER_ENABLE`      | Enables the timer function in the selected working mode. See the table below for the allowed working modes.    |
| 1               | `OFFMB_TIMER_ON`          | 32-bit value (2 registers) with the timestamp that starts the timer.                                           |
| 3               | `OFFMB_TIMER_OFF`         | 32-bit value (2 registers) with the timestamp that stops the timer (not used).                                 |
| 5               | `OFFMB_TIMER_PERIOD`      | 32-bit value (2 registers) with the time in seconds between starting points. For example: daily = 86400.       |
| 7               | `OFFMB_TIMER_INTERVAL`    | 32-bit value (2 registers) with the time in seconds that the timer has to run when started. Example: 1 hour = 3600. |
| 9               | `OFFMB_TIMER_COUNTDOWN`   | 32-bit value (2 registers) — time remaining in seconds for the countdown mode.                                 |
| 11              | `OFFMB_TIMER_FUNCTION`    | Function assigned to this timer. See table below.                                                              |
| 13              | `OFFMB_TIMER_WORK_TIME`   | Number of seconds the timer has been operating.                                                                |

**Allowed timer working modes:**

| Value | Identifier              | Description                                       |
| ----- | ----------------------- | ------------------------------------------------- |
| 0     | `CTIMER_DISABLE`        | Timer disabled.                                   |
| 1     | `CTIMER_ENABLED`        | Timer enabled and independent.                    |
| 2     | `CTIMER_ENABLED_LINKED` | Timer enabled and linked to the relay from timer 0. |
| 3     | `CTIMER_ALWAYS_ON`      | Relay assigned to this timer is always on.        |
| 4     | `CTIMER_ALWAYS_OFF`     | Relay assigned to this timer is always off.       |
| 5     | `CTIMER_COUNTDOWN`      | Timer in countdown mode.                          |

**Function codes:**

| Value  | Identifier              | Description                                |
| ------ | ----------------------- | ------------------------------------------ |
| 0x0001 | `CTIMER_FCT_FILTRATION` | Filtration function of the machine.        |
| 0x0002 | `CTIMER_FCT_LIGHTING`   | Lighting function of the machine.          |
| 0x0004 | `CTIMER_FCT_HEATING`    | Heating function of the machine.           |
| 0x0100 | `CTIMER_FCT_AUXREL1`    | Auxiliary function assigned to relay 1.    |
| 0x0200 | `CTIMER_FCT_AUXREL2`    | Auxiliary function assigned to relay 2.    |
| 0x0400 | `CTIMER_FCT_AUXREL3`    | Auxiliary function assigned to relay 3.    |
| 0x0800 | `CTIMER_FCT_AUXREL4`    | Auxiliary function assigned to relay 4.    |
| 0x1000 | `CTIMER_FCT_AUXREL5`    | Auxiliary function assigned to relay 5.    |
| 0x2000 | `CTIMER_FCT_AUXREL6`    | Auxiliary function assigned to relay 6.    |
| 0x4000 | `CTIMER_FCT_AUXREL7`    | Auxiliary function assigned to relay 7.    |

---

### Register 0x04E8 - `MBF_PAR_FILTVALVE_ENABLE`

This register enables or disables the filter-cleaning functionality in a given mode. Currently only two modes exist:

| Value | Description                            |
| ----- | -------------------------------------- |
| 0     | Functionality disabled.                |
| 1     | Functionality enabled in Besgo mode.   |

---

### Register 0x04E9 - `MBF_PAR_FILTVALVE_MODE`

This register stores the timing mode of the valve.

| Value | Identifier            | Description                                                                                                                          |
| ----- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 1     | `CTIMER_ENABLED`      | Timed system. Takes the start time and the periodicity into account to perform the cleaning.                                         |
| 3     | `CTIMER_ALWAYS_ON`    | Cleaning has been activated manually and remains on for the time set in the `MBF_PAR_FILTVALVE_INTERVAL` register.                   |
| 4     | `CTIMER_ALWAYS_OFF`   | Filter cleaning is manually disabled and never turns on.                                                                             |

---

### Register 0x04EA - `MBF_PAR_FILTVALVE_GPIO`

This register selects the relay associated with the filter-cleaning function. The default value is AUX2 (value 5).

| Value | Description                                                          |
| ----- | -------------------------------------------------------------------- |
| 0     | No relay assigned (the filter-cleaning function is inhibited).       |
| 1     | pH relay.                                                            |
| 2     | Filtration relay.                                                    |
| 3     | Lighting relay.                                                      |
| 4     | AUX1 relay.                                                          |
| 5     | AUX2 relay.                                                          |
| 6     | AUX3 relay.                                                          |
| 7     | AUX4 relay.                                                          |

---

### Registers 0x04EB / 0x04EC - `MBF_PAR_FILTVALVE_START` (32 bits)

32-bit timestamp (Low, High) that marks the start of the filter cleaning.

---

### Register 0x04ED - `MBF_PAR_FILTVALVE_PERIOD_MINUTES`

Period in minutes between cleaning actions. For example, if this register stores a value of 60, a cleaning action will occur every hour.

---

### Register 0x04EE - `MBF_PAR_FILTVALVE_INTERVAL`

Duration of the cleaning action in seconds.

---

### Register 0x04EF - `MBF_PAR_FILTVALVE_REMAINING`

Time remaining for the current cleaning action in seconds. If this register is 0, no cleaning function is in progress.

When a cleaning function starts, the contents of `MBF_PAR_FILTVALVE_INTERVAL` are copied into this register and then decremented once per second. The screen uses this register to show the progress of the cleaning function.

---

## 2.6 User Page (USER)

### Register 0x0502 - `MBF_PAR_HIDRO`

This register contains the hydrolysis target production level. When the hydrolysis production is to be set in percent values, this value will contain the percent of production. If the hydrolysis module is set to work in g/h production, this register will contain the desired amount of production in g/h units.

The value adjusted in this register must not exceed the value set in the `MBF_PAR_HIDRO_NOM` factory register.

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0504 - `MBF_PAR_PH1`

This register contains the higher limit of the pH regulation system. The value set in this register is multiplied by 100. This means that if we want to set a value of 7.5, the numerical content that we must write in this register is 750.

This register must always be higher than `MBF_PAR_PH2`.

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0505 - `MBF_PAR_PH2`

This register contains the lower limit of the pH regulation system. The value set in this register is multiplied by 100. This means that if we want to set a value of 7.0, the numerical content that we must write in this register is 700.

This register must always be lower than `MBF_PAR_PH1`.

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0506 - `MBF_PAR_HIDRO_CTRL_MODULE`

This function determines which measurement module controls the hydrolysis generation.

| Value | Description                                                |
| ----- | ---------------------------------------------------------- |
| 0     | Hydrolysis generation is controlled by the ORP (RX) module. |
| 1     | Hydrolysis generation is controlled by the Chlorine (CL) module. |

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0508 - `MBF_PAR_RX1`

This register contains the set point for the redox regulation system. When the system is configured as dual setpoint, this field contains the lower set point. This value must be in the range of 0 to 1000.

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x050A - `MBF_PAR_CL1`

This register contains the set point for the chlorine regulation system. When the system is configured as dual set-point mode, this field contains the lower set point.

The value stored in this register is multiplied by 100. This means that if we want to set a value of 1.5 ppm, we will have to write a numerical value of 150.

This value stored in this register must be in the range of 0 to 1000.

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x050E - `MBF_PAR_CD1`

Lower set-point value for the conductivity module. Value is written in microsiemens. When the system is configured as dual set-point mode, this field contains the lower set point.

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x050F - `MBF_PUMP_CONFIG`

This register holds the configuration of the filtration pump. The register is divided into 5 different bit fields. The following table describes each field:

| Bits  | Mask   | Description                                                                                        |
| ----- | ------ | -------------------------------------------------------------------------------------------------- |
| 0-3   | 0x000F | Pump type. Defines the type of pump connected to the system: `0` = STANDARD, `1` = VARIABLE SPEED Type A, `2` = VARIABLE_SPEED Type B. |
| 4-6   | 0x0070 | Pump speed in manual mode: `0` = Slow, `1` = Medium, `2` = Fast.                                   |
| 7-9   | 0x0380 | Pump speed in filtration interval 1: `0` = Slow, `1` = Medium, `2` = Fast.                         |
| 10-12 | 0x1C00 | Pump speed in filtration interval 2: `0` = Slow, `1` = Medium, `2` = Fast.                         |
| 13-15 | 0xE000 | Pump speed in filtration interval 3: `0` = Slow, `1` = Medium, `2` = Fast.                         |

**Example:** the `MBF_PUMP_CONFIG` register contains the value `0x0402`. The configuration of the system will then be:

- Pump type: 2 — Variable speed type B
- Manual mode: 0 — Slow speed
- Filtration interval 1: 0 — Slow speed
- Filtration interval 2: 1 — Medium speed
- Filtration interval 3: 0 — Slow speed

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0511 - `MBF_PAR_RX2`

This register contains the set point for the redox regulation system. When the system is configured as dual set-point mode, this field contains the upper set point. This value must be in the range of 0 to 1000.

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0512 - `MBF_PAR_CL2`

This register contains the set point for the chlorine regulation system. When the system is configured as dual set-point mode, this field contains the upper set point.

The value stored in this register is multiplied by 100. This means that if we want to set a value of 1.5 ppm, we will have to write a numerical value of 150.

This value stored in this register must be in the range of 0 to 1000.

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x0513 - `MBF_PAR_PUMP_SPEEDS`

This register contains the pump speeds for specific actions when a variable-speed pump is configured in the system.

| Bits | Mask   | Description                                                                                          |
| ---- | ------ | ---------------------------------------------------------------------------------------------------- |
| 0-3  | 0x000F | Speed used when operating the filtration valve: `0` = Slow, `1` = Medium, `2` = Fast, `3` = do not override. |
| 4-7  | 0x00F0 | Speed used when operating cover protection: `0` = Slow, `1` = Medium, `2` = Fast, `3` = do not override. |
| 8-11 | 0x0F00 | Speed used when operating the filtration valve: `0` = Slow, `1` = Medium, `2` = Fast.                |

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x051B - `MBF_PAR_FUNCTION_DEPENDENCY`

This register contains the specification for the dependency of different functions, such as heating, on external events like FL1.

| Bits | Mask   | Identifier              | Description                    |
| ---- | ------ | ----------------------- | ------------------------------ |
| 0-2  | 0x0007 | `MBMSK_FCTDEP_HEATING`  | Heating function dependency.   |

**Bit values:**

| Bit | Mask   | Identifier                       |
| --- | ------ | -------------------------------- |
| 0   | 0x0001 | `MBMSK_DEPENDENCY_FL1_PADDLE`    |
| 1   | 0x0002 | `MBMSK_DEPENDENCY_FL2`           |
| 2   | 0x0004 | `MBMSK_DEPENDENCY_SLAVE`         |

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x051D - `MBF_PAR_PUMP_SCALING`

This register stores the pump scaling for the pH dosing pump and the other dosing pumps available in the system. The register is split in two fields, the lower one for the pH dosing timing and the upper for the rest of the pumps.

| Bits | Mask   | Description                                                                            |
| ---- | ------ | -------------------------------------------------------------------------------------- |
| 0-7  | 0x00FF | Pump scaling for the pH pump. Valid value range: 0 for 0 % to 100 for 100 % of scaling. |
| 8-15 | 0xFF00 | Pump scaling for the other pumps. Valid value range: 0 for 0 % to 100 for 100 % of scaling. |

Scaling changes the pump-on time according to the difference between the set point and the currently measured parameter. The following maximum scaling differences are chosen for the four measurement modules:

| Module             | Difference     |
| ------------------ | -------------- |
| pH                 | 1.0            |
| Redox (ORP)        | 100 mV         |
| Chlorine (Cl)      | 50 ppm         |
| Conductivity (Cd)  | 500 microsiemens |

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

### Register 0x051E - `MBF_PAR_CD2`

Upper set-point value for the conductivity module. Value is written in microsiemens. When the system is configured as dual set-point mode, this field contains the upper set point.

> To make the modification of this register persistent, execute the EEPROM storage procedure described in global register `MBF_SAVE_TO_EEPROM`.

---

## 2.7 Miscellaneous Page (MISC)

This page contains the registers associated with the screen configuration and its display options.

---

### Register 0x0601 - `MBF_PAR_UICFG_LANGUAGE`

This parameter selects the language used by the user interface of the unit.

| Value | Identifier                  |
| ----- | --------------------------- |
| 0     | SPANISH                     |
| 1     | ENGLISH                     |
| 2     | FRENCH                      |
| 3     | GERMAN                      |
| 4     | ITALIAN                     |
| 5     | PORTUGUESE (not implemented) |
| 6     | TURKISH                     |
| 7     | CZECH                       |

---

### Register 0x0602 - `MBF_PAR_UICFG_BACKLIGHT`

This register contains the configuration of the screen backlight. It is divided into two halves of 8 bits each.

The **low byte** (8 LSBs) contains the screen-off interval when no keys are pressed:

| Value | Timeout                            |
| ----- | ---------------------------------- |
| 0     | 15 seconds                         |
| 1     | 30 seconds                         |
| 2     | 60 seconds                         |
| 3     | 5 minutes                          |
| 4     | The screen never turns off         |

The **high byte** (8 MSBs) contains the intensity in percentage (10 to 100 %) of the screen backlight.

---

### Register 0x0603 - `MBF_PAR_UICFG_SOUND`

This register stores the configuration of the screen sound alerts. It is a bit field with the following layout:

| Bit | Mask   | Identifier   | Description                                                                |
| --- | ------ | ------------ | -------------------------------------------------------------------------- |
| 0   | 0x0001 | `CLICK`      | A click sounds each time a key is pressed.                                 |
| 1   | 0x0002 | `POPUPS`     | A sound is played each time a popup message appears.                       |
| 2   | 0x0004 | `ALERTS`     | An alarm sounds when there is an alert in the unit (AL3).                  |
| 3   | 0x0008 | `FILTRATION` | A sound notice is played each time filtration starts.                      |
