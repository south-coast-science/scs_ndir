#!/usr/bin/env python3

"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.spi_ndir_v1.spi_ndir_v1 import SPINDIRv1


# --------------------------------------------------------------------------------------------------------------------

eeprom_addr = 1

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = SPINDIRv1(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    version = ndir.version()
    jstr = JSONify.dumps(version)

    print("version: %s" % jstr)
    print("-")

    status = ndir.status()
    jstr = JSONify.dumps(status)

    print("status: %s" % jstr)
    print("-")

    v_in_value = ndir.cmd_input_raw()

    print("v_in_value: %d" % v_in_value)

    v_in_voltage = ndir.cmd_input()

    print("v_in_voltage: %0.3f" % v_in_voltage)
    print("-")

    # ndir.power_off()

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    pass

finally:
    I2C.close()