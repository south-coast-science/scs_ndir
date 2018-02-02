#!/usr/bin/env python3

"""
Created on 2 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer

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

    echo = ndir.cmd_echo([12, 34, 56, 78, 90])
    print("echo: %s" % echo)
    print("-")

    version = ndir.cmd_version()
    jstr = JSONify.dumps(version)

    print("version: %s" % jstr)
    print("-")

    status = ndir.cmd_status()
    jstr = JSONify.dumps(status)

    print("status: %s" % jstr)
    print("-")

    start_time = time.time()

    timer = IntervalTimer(0.1)

    while timer.true():
        pile_ref_value, pile_act_value, thermistor_value = ndir.cmd_sample_raw()
        elapsed_time = time.time() - start_time

        print("%0.3f, %d, %d, %d" % (elapsed_time, pile_ref_value, pile_act_value, thermistor_value))

    # ndir.power_off()

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    pass

finally:
    I2C.close()
