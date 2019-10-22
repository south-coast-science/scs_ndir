#!/usr/bin/env python3

"""
Created on 23 Aug 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir_conf import NDIRConf
from scs_ndir.gas.ndir_monitor import NDIRMonitor

from scs_ndir.gas.spi_ndir_t1_f1.spi_ndir_t1_f1 import SPINDIRt1f1

# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

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

    ndir = SPINDIRt1f1(interface, Host.ndir_spi_bus(), Host.ndir_spi_device())
    print("ndir: %s" % ndir)
    print("-")

    ndir.power_on()

    monitor = NDIRMonitor(ndir, conf)
    print("monitor: %s" % monitor)

    firmware = monitor.firmware()
    print("firmware: %s" % firmware)
    print("-")

    monitor.start()

    for i in range(10):
        datum = monitor.sample()
        print("datum: %s" % datum)

        time.sleep(10)

    monitor.stop()

except KeyboardInterrupt:
    pass

finally:
    I2C.close()
