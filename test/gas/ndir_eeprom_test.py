#!/usr/bin/env python3

"""
Created on 29 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR
from scs_ndir.gas.ndir_calib import NDIRCalib


# --------------------------------------------------------------------------------------------------------------------

calib = NDIRCalib.load(Host)
print("calib: %s" % calib)
print("-")


try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    status = ndir.cmd_status()
    print("status: %s" % status)
    print("-")

    ndir.cmd_store_eeprom_calib(calib)
    print("=")

    calib = ndir.cmd_retrieve_eeprom_calib()
    print("calib: %s" % calib)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
