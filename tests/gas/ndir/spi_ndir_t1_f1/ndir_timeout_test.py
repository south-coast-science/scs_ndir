#!/usr/bin/env python3

"""
Created on 23 Aug 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.sync.interval_timer import IntervalTimer

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.exception.ndir_exception import NDIRException
from scs_ndir.gas.ndir.ndir_conf import NDIRConf

from scs_ndir.gas.ndir.spi_ndir_t1_f1.spi_ndir_t1_f1 import SPINDIRt1f1


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Sensors.open()

    # ------------------------------------------------------------------------------------------------------------
    # resources...

    # Interface...
    interface_conf = InterfaceConf.load(Host)

    if interface_conf is None:
        print("InterfaceConf not available.")
        exit(1)

    interface = interface_conf.interface()
    print(interface)

    # NDIR...
    conf = NDIRConf("t1f1", 5)
    print("conf: %s" % conf)

    ndir = SPINDIRt1f1(interface, Host.ndir_spi_dev_path())
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
    I2C.Sensors.close()
