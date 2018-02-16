#!/usr/bin/env python3

"""
Created on 2 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

interval = 0.01             # 10 mS is fastest possible
samples = 200               # 10 mS * 1000 = 10 S

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir, file=sys.stderr)
    print("-", file=sys.stderr)

    ndir.power_on()

    status = ndir.cmd_status()
    jstr = JSONify.dumps(status)

    print("status: %s" % jstr, file=sys.stderr)
    print("-", file=sys.stderr)

    print("calibrating...", file=sys.stderr)
    ndir.cmd_measure_calibrate()

    start_time = time.time()
    timer = IntervalTimer(interval)

    print("rec, pile_ref, pile_act, thermistor")

    for _ in timer.range(samples):
        pile_ref_voltage, pile_act_voltage, thermistor_voltage = ndir.cmd_measure()
        elapsed_time = time.time() - start_time

        print("%0.3f, %0.4f, %0.4f, %0.4f" % (elapsed_time, pile_ref_voltage, pile_act_voltage, thermistor_voltage))
        sys.stdout.flush()

    # ndir.power_off()

except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    pass

finally:
    I2C.close()
