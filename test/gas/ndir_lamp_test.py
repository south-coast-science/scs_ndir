#!/usr/bin/env python3

"""
Created on 1 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

ndir = None

start_time = time.time()

try:
    I2C.open(Host.I2C_SENSORS)

    ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
    print(ndir)
    print("-")

    ndir.power_on()

    version = ndir.cmd_version()
    print("version: %s" % version)
    print("-")

    # square wave...

    while True:
        if True:
            on = 0x0fff
            ndir.cmd_lamp_set(on)
            print("lamp: %d ..." % on)

            time.sleep(4)

            pile_ref_voltage, pile_act_voltage, thermistor_voltage = ndir.cmd_sample()

            print("pile_ref_voltage: %f" % pile_ref_voltage)
            print("pile_act_voltage: %f" % pile_act_voltage)
            print("thermistor_voltage: %f" % thermistor_voltage)
            print("-")

        if True:
            on = 0x0000
            ndir.cmd_lamp_set(on)
            print("lamp: %d ..." % on)

            time.sleep(4)

            pile_ref_voltage, pile_act_voltage, thermistor_voltage = ndir.cmd_sample()

            print("pile_ref_voltage: %f" % pile_ref_voltage)
            print("pile_act_voltage: %f" % pile_act_voltage)
            print("thermistor_voltage: %f" % thermistor_voltage)
            print("-")

        status = ndir.cmd_status()
        print("uptime: %s" % status.uptime.timedelta)
        print("-")

        if status.uptime.seconds > 100000:
            break


    # sawtooth wave...

    while False:
        for level in range(4096):
            ndir.cmd_lamp_set(level)
            # print("lamp: %d ..." % level)

            time.sleep(0.01)

        status = ndir.cmd_status()
        print("uptime: %s" % status.uptime.timedelta)
        print("-")


except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    if ndir:
        ndir.cmd_lamp_set(0)

    elapsed_time = time.time() - start_time
    print("elapsed_time: %0.1f" % elapsed_time)

    I2C.close()
