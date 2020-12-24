#!/usr/bin/env python3

"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_host.bus.i2c import SensorI2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir.spi_ndir_x1.spi_ndir_x1 import SPINDIRx1


# --------------------------------------------------------------------------------------------------------------------

try:
    SensorI2C.open()

    ndir = SPINDIRx1(False, Host.ndir_spi_bus(), Host.ndir_spi_device())
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

    v_in_value = ndir.input_raw()

    print("v_in_value: %d" % v_in_value)

    v_in_voltage = ndir.input_voltage()

    print("v_in_voltage: %0.3f" % v_in_voltage)
    print("-")

    # ndir.power_off()

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    pass

finally:
    SensorI2C.close()
