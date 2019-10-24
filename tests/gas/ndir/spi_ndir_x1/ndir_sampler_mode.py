#!/usr/bin/env python3

"""
Created on 11 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir.spi_ndir_x1.spi_ndir_x1 import SPINDIRx1


# --------------------------------------------------------------------------------------------------------------------

scan_single_shot = True


try:
    I2C.open(Host.I2C_SENSORS)

    ndir = SPINDIRx1(False, Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir, file=sys.stderr)
    print("-", file=sys.stderr)

    ndir.power_on()

    ndir.get_sample_mode(scan_single_shot)
    print("single_shot: %s" % scan_single_shot)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
