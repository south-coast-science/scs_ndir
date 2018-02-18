#!/usr/bin/env python3

"""
Created on 29 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: ndir_calib_test.py must be run first!
"""

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR
from scs_ndir.gas.ndir_calib import NDIRCalib


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    status = ndir.status()
    print("status: %s" % status)
    print("=")

    # print("current...")
    # calib = ndir.cmd_retrieve_eeprom_calib()
    # print("calib: %s" % calib)

    calib = NDIRCalib.load(Host)

    ndir.cmd_store_eeprom_calib(calib)
    print("-")

    print("new...")
    calib = ndir.cmd_retrieve_eeprom_calib()
    print("new calib: %s" % calib)


except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
