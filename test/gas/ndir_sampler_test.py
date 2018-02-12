#!/usr/bin/env python3

"""
Created on 11 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

max_scan_deferral = 180
min_scan_deferral = 730


try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    status = ndir.cmd_status()
    print("status: %s" % status)
    print("-")

    pile_ref_min, pile_act_min, thermistor_min, pile_ref_max, pile_act_max, thermistor_max, \
    pile_ref_amplitude, pile_act_amplitude, thermistor_average = \
        ndir.cmd_sample_raw(max_scan_deferral, min_scan_deferral)

    print("pile_ref_min: %s" % pile_ref_min)
    print("pile_act_min: %s" % pile_act_min)
    print("thermistor_min: %s" % thermistor_min)
    print("-")

    print("pile_ref_max: %s" % pile_ref_max)
    print("pile_act_max: %s" % pile_act_max)
    print("thermistor_max: %s" % thermistor_max)
    print("-")

    print("pile_ref_amplitude: %s" % pile_ref_amplitude)
    print("pile_act_amplitude: %s" % pile_act_amplitude)
    print("thermistor_average: %s" % thermistor_average)

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
