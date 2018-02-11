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

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    version = ndir.cmd_version()
    jstr = JSONify.dumps(version)

    print("version: %s" % jstr)
    print("-")

    status = ndir.cmd_status()
    jstr = JSONify.dumps(status)

    print("status: %s" % jstr)
    print("-")

    v_in_value = ndir.cmd_input_raw()

    print("v_in_value: %d" % v_in_value)

    v_in_voltage = ndir.cmd_input()

    print("v_in_voltage: %0.3f" % v_in_voltage)
    print("-")

    pile_ref_value, pile_act_value, thermistor_value = ndir.cmd_measure_raw()

    print("pile_ref_value: %d" % pile_ref_value)
    print("pile_act_value: %d" % pile_act_value)
    print("thermistor_value: %d" % thermistor_value)
    print("-")

    pile_ref_voltage, pile_act_voltage, thermistor_voltage = ndir.cmd_measure()

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
