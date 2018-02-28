#!/usr/bin/env python3

"""
Created on 11 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.sync.interval_timer import IntervalTimer

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

max_scan_deferral = 200
min_scan_deferral = 740


try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir, file=sys.stderr)
    print("-", file=sys.stderr)

    ndir.power_on()

    start_time = time.time()
    timer = IntervalTimer(1.0)

    print("rec, pile_ref_amplitude, pile_act_amplitude, pile_diff, thermistor_avg")

    while timer.true():
        elapsed_time = time.time() - start_time
        pile_ref_amplitude, pile_act_amplitude, thermistor_avg = ndir.cmd_sample_voltage()
        diff = pile_ref_amplitude - pile_act_amplitude

        print("%7.3f, %0.4f, %0.4f, %0.4f, %0.4f" %
              (elapsed_time, pile_ref_amplitude, pile_act_amplitude, diff, thermistor_avg))
        sys.stdout.flush()

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
