#!/usr/bin/env python3

"""
Created on 29 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: ndir_calib_test.py must be run first!
"""

from scs_dfe.interface.dfe.dfe import DFE

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir.spi_ndir_x1.spi_ndir_x1 import SPINDIRx1
from scs_ndir.gas.ndir.spi_ndir_x1.ndir_calib import NDIRCalib


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    ndir = SPINDIRx1(DFE(), Host.ndir_spi_dev_path())
    print(ndir)
    print("-")

    ndir.power_on()

    status = ndir.status()
    print("status: %s" % status)
    print("=")

    print("current...")
    calib = ndir.retrieve_calib()
    print("calib: %s" % calib)

    calib = NDIRCalib.load(Host)

    ndir.store_calib(calib)
    print("-")

    print("new...")
    calib = ndir.retrieve_calib()
    print("calib: %s" % calib)


except KeyboardInterrupt:
    print("")

finally:
    I2C.Sensors.close()
