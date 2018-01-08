#!/usr/bin/env python3

"""
Created on 6 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    status = ndir.cmd_status()
    print("status: %s" % status)
    print("-")

    jstr = JSONify.dumps(status)
    print(jstr)
    print("-")

    ndir.cmd_reset()
    print("NDIR RESET")
    print("-")

    status = ndir.cmd_status()
    print("status: %s" % status)
    print("-")

    jstr = JSONify.dumps(status)
    print(jstr)
    print("-")

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
