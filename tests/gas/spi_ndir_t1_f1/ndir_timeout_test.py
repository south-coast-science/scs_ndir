#!/usr/bin/env python3

"""
Created on 23 Aug 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.sync.interval_timer import IntervalTimer

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.exception.ndir_exception import NDIRException
from scs_ndir.gas.ndir_conf import NDIRConf

from scs_ndir.gas.spi_ndir_t1_f1.spi_ndir_t1_f1 import SPINDIRt1f1


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    conf = NDIRConf("t1f1", 5)
    print("conf: %s" % conf)

    ndir = SPINDIRt1f1(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print("ndir: %s" % ndir)
    print("-")

    ndir.power_on()

    interval = ndir.get_sample_interval()
    print("interval: %s" % interval)
    print("-")

    ndir.sample()
    time.sleep(interval)

    datum = ndir.get_sample_gas()

    print("response after %s secs..." % interval)
    print("datum: %s" % datum)
    print("-")

    ndir.sample()

    start_time = time.time()
    time.sleep(0.7)

    timer = IntervalTimer(0.1)

    for i in timer.range(15):
        elapsed_time = time.time() - start_time

        try:
            datum = ndir.get_sample_gas()
        except NDIRException as ex:
            datum = ex

        print("%0.3f: datum: %s" % (elapsed_time, datum))

    print("-")

    version = ndir.version()
    print("version: %s" % version)

except KeyboardInterrupt:
    pass

finally:
    I2C.close()