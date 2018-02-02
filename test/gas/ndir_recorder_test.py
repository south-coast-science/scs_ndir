#!/usr/bin/env python3

"""
Created on 30 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

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

    pile_ref_value, pile_act_value, thermistor_value = ndir.cmd_sample_raw()
    print("%d, %d, %d" % (pile_ref_value, pile_act_value, thermistor_value))

    data = ndir.cmd_run_recorder(150)

    for datum in data:
        print("%d, %d, %d" % (datum[0], datum[1], datum[2]))


except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
