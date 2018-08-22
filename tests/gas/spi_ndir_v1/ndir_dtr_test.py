#!/usr/bin/env python3

"""
Created on 30 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.exception.ndir_exception import NDIRException
from scs_ndir.gas.spi_ndir_v1.spi_ndir_v1 import SPINDIRv1


# --------------------------------------------------------------------------------------------------------------------

ndir = None

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = SPINDIRv1(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    # ndir.power_on()
    #
    # status = ndir.status()
    # print("status: %s" % status)
    # print("-")
    #
    # ndir.cmd_sample_mode(True)

    ndir.wait()

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
