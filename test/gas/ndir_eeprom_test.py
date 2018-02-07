#!/usr/bin/env python3

"""
Created on 29 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

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

    # version = ndir.cmd_version()
    # print("version: %s" % version)
    # print("-")

    ndir.cmd_eeprom_write_time_to_sample(1234)
    ndir.cmd_eeprom_write_time_after_sample(4321)
    ndir.cmd_eeprom_write_coeff_b(0.123456)
    ndir.cmd_eeprom_write_coeff_c(-0.123456)
    ndir.cmd_eeprom_write_therm_a(1.234567)
    ndir.cmd_eeprom_write_therm_b(-1.234567)
    ndir.cmd_eeprom_write_therm_c(12.345678)
    ndir.cmd_eeprom_write_therm_d(-12.345678)
    ndir.cmd_eeprom_write_alpha(123.456789)
    ndir.cmd_eeprom_write_beta_a(-123.456789)
    ndir.cmd_eeprom_write_t_cal(-1234.567890)

    print("=")
    time_to_sample = ndir.cmd_eeprom_read_time_to_sample()
    print("time_to_sample: %d" % time_to_sample)
    print("-")

    time_after_sample = ndir.cmd_eeprom_read_time_after_sample()
    print("time_after_sample: %d" % time_after_sample)
    print("-")

    coeff_b = ndir.cmd_eeprom_read_coeff_b()
    print("coeff_b: %f" % coeff_b)
    print("-")

    coeff_c = ndir.cmd_eeprom_read_coeff_c()
    print("coeff_c: %f" % coeff_c)
    print("-")

    therm_a = ndir.cmd_eeprom_read_therm_a()
    print("therm_a: %f" % therm_a)
    print("-")

    therm_b = ndir.cmd_eeprom_read_therm_b()
    print("therm_b: %f" % therm_b)
    print("-")

    therm_c = ndir.cmd_eeprom_read_therm_c()
    print("therm_c: %f" % therm_c)
    print("-")

    therm_d = ndir.cmd_eeprom_read_therm_d()
    print("therm_d: %f" % therm_d)
    print("-")

    alpha = ndir.cmd_eeprom_read_alpha()
    print("alpha: %f" % alpha)
    print("-")

    beta_a = ndir.cmd_eeprom_read_beta_a()
    print("beta_a: %f" % beta_a)
    print("-")

    t_cal = ndir.cmd_eeprom_read_t_cal()
    print("t_cal: %f" % t_cal)
    print("-")


except ValueError as ex:
    print("ValueError: %s" % ex)

except KeyboardInterrupt:
    print("")

finally:
    I2C.close()
