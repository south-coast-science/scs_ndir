#!/usr/bin/env python3

"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

eeprom_addr = 1

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR()
    print(ndir)
    print("-")

    ndir.power_on()

    echo = ndir.cmd_echo([12, 34, 56, 78, 90])
    print("echo: %s" % echo)
    print("-")

    version = ndir.cmd_version()
    jstr = JSONify.dumps(version)

    print("version: %s" % jstr)
    print("-")

    status = ndir.cmd_status()
    jstr = JSONify.dumps(status)

    print("status: %s" % jstr)
    print("-")

    watchdog = ndir.cmd_watchdog_clear()
    print("-")

    eeprom = ndir.cmd_eeprom_read_unsigned_long(eeprom_addr)
    print("eeprom: %s" % eeprom)

    ndir.cmd_eeprom_write_unsigned_long(eeprom_addr, status.uptime.seconds)

    eeprom = ndir.cmd_eeprom_read_unsigned_long(eeprom_addr)
    print("eeprom: %s" % eeprom)
    print("-")

    v_in_value = ndir.cmd_monitor_raw()

    print("v_in_value: %d" % v_in_value)

    v_in_voltage = ndir.cmd_monitor()

    print("v_in_voltage: %0.3f" % v_in_voltage)
    print("-")

    pile_ref_value, pile_act_value, thermistor_value = ndir.cmd_sample_raw()

    print("pile_ref_value: %d" % pile_ref_value)
    print("pile_act_value: %d" % pile_act_value)
    print("thermistor_value: %d" % thermistor_value)
    print("-")

    pile_ref_voltage, pile_act_voltage, thermistor_voltage = ndir.cmd_sample()

    print("pile_ref_voltage: %f" % pile_ref_voltage)
    print("pile_act_voltage: %f" % pile_act_voltage)
    print("thermistor_voltage: %f" % thermistor_voltage)
    print("-")

    # ndir.power_off()

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    pass

finally:
    I2C.close()
