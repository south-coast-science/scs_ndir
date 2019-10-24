#!/usr/bin/env python3

"""
Created on 30 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir.spi_ndir_x1.spi_ndir_x1 import SPINDIRx1


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = SPINDIRx1(False, Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    status = ndir.status()
    print("status: %s" % status)
    print("-")

    data = ndir.record_raw(0, 5, 200)

    print("rec, raw_pile_ref, raw_pile_act")

    for datum in data:
        print("%d, %d, %d" % datum)


except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
