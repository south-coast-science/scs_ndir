#!/usr/bin/env python3

"""
Created on 1 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

ndir = None

start_time = time.time()

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    version = ndir.cmd_version()
    print("version: %s" % version)
    print("-")


    ndir.cmd_lamp_run(False)
    time.sleep(5.0)

    ndir.cmd_lamp_run(True)


except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    if ndir:
        pass
        # ndir.cmd_lamp_level(0)

        # time.sleep(10.0)
        # ndir.power_off()

    elapsed_time = time.time() - start_time
    print("elapsed time: %0.1f" % elapsed_time)

    I2C.close()
