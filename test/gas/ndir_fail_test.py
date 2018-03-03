#!/usr/bin/env python3

"""
Created on 30 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.exception.ndir_exception import NDIRException
from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

ndir = None

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    status = ndir.status()
    print("status: %s" % status)
    print("-")

    try:
        print("*** unrecognised command...")
        response = ndir.cmd('xx', 0.001, 0.0, 0)
        print(response)
    except NDIRException as ex:
        print(ex)

    print("-")

    try:
        print("*** unrecognised command with return count...")
        response = ndir.cmd('xx', 0.001, 0.0, 2)
        print(response)
    except NDIRException as ex:
        print(ex)

    print("-")

    time.sleep(NDIR.RECOVERY_TIME)      # TODO: tune the time

    status = ndir.status()
    print("status: %s" % status)
    print("-")


except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
