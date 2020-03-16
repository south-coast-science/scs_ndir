#!/usr/bin/env python3

"""
Created on 11 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.sample.gases_sample import GasesSample

from scs_core.sync.interval_timer import IntervalTimer

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir.spi_ndir_x1.spi_ndir_x1 import SPINDIRx1


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = SPINDIRx1(False, Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir, file=sys.stderr)
    print("-", file=sys.stderr)

    ndir.power_on()

    start_time = time.time()
    timer = IntervalTimer(3.0)

    for _ in timer.range(4000):
        ndir.get_sample_mode(True)
        rec = LocalizedDatetime.now().utc()
        co2_datum = ndir.sample()

        sample = GasesSample('', rec, co2_datum, None, None)

        print(JSONify.dumps(sample))
        sys.stdout.flush()

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
