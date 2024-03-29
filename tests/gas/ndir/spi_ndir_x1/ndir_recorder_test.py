#!/usr/bin/env python3

"""
Created on 30 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.interface.dfe.dfe import DFE

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir.spi_ndir_x1.spi_ndir_x1 import SPINDIRx1


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    ndir = SPINDIRx1(DFE(), Host.ndir_spi_dev_path())
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


except KeyboardInterrupt:
    print(file=sys.stderr)

except ValueError as ex:
    print(repr(ex), file=sys.stderr)

finally:
    I2C.Sensors.close()
