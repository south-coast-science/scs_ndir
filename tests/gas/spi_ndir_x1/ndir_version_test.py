#!/usr/bin/env python3

"""
Created on 2 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify

from scs_core.gas.ndir_version import NDIRVersion

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.spi_ndir_x1.spi_ndir_x1 import SPINDIRx1


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = SPINDIRx1(False, Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    version = ndir.version()
    print("version: %s" % version)
    print("-")

    jstr = JSONify.dumps(version)
    print(jstr)
    print("-")

    jdict = json.loads(jstr)

    version = NDIRVersion.construct_from_jdict(jdict)
    print("version: %s" % version)
    print("-")

    jstr = JSONify.dumps(version)
    print(jstr)
    print("-")

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
