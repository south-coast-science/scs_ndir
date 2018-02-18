#!/usr/bin/env python3

"""
Created on 13 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

scan_deferral = 740


try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    status = ndir.status()
    print("status: %s" % status)
    print("-")

    print("rec, pile_ref, pile_act, thermistor")

    data = ndir.cmd_sample_window()

    for i in range(len(data)):
        rec = scan_deferral + i + 1
        datum = data[i]

        print("%d, %d, %d, %d" % (rec, datum[0], datum[1], datum[2]))

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
