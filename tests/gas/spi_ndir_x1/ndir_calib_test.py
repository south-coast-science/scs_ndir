#!/usr/bin/env python3

"""
Created on 8 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_ndir.gas.spi_ndir_x1.ndir_calib import NDIRCalib, NDIRRangeCalib


# --------------------------------------------------------------------------------------------------------------------

# identity...
ndir_serial = 111
board_serial = 222

selected_range = 1

# common fields...
lamp_voltage = 4.5

lamp_period = 500
max_deferral = 100
min_deferral = 300

# range calibrations...

# range_iaq...
zero = 1.1
span = 1.2

linear_b = 1.3
linear_c = 1.4

alpha_low = 1.5
alpha_high = 1.6

beta_a = 1.7
beta_o = 1.8

t_cal = 1.9

range_iaq = NDIRRangeCalib(zero, span, linear_b, linear_c, alpha_low, alpha_high, beta_a, beta_o, t_cal)

# range_safety...
zero = 2.1
span = 2.2

linear_b = 2.3
linear_c = 2.4

alpha_low = 2.5
alpha_high = 2.6

beta_a = 2.7
beta_o = 2.8

t_cal = 2.9

range_safety = NDIRRangeCalib(zero, span, linear_b, linear_c, alpha_low, alpha_high, beta_a, beta_o, t_cal)

# range_combustion...
zero = 3.1
span = 3.2

linear_b = 3.3
linear_c = 3.4

alpha_low = 3.5
alpha_high = 3.6

beta_a = 3.7
beta_o = 3.8

t_cal = 3.9

range_combustion = NDIRRangeCalib(zero, span, linear_b, linear_c, alpha_low, alpha_high, beta_a, beta_o, t_cal)

# range_industrial...
zero = 4.1
span = 4.2

linear_b = 4.3
linear_c = 4.4

alpha_low = 4.5
alpha_high = 4.6

beta_a = 4.7
beta_o = 4.8

t_cal = 4.9

range_industrial = NDIRRangeCalib(zero, span, linear_b, linear_c, alpha_low, alpha_high, beta_a, beta_o, t_cal)

# range_custom...
zero = 5.1
span = 5.2

linear_b = 5.3
linear_c = 5.4

alpha_low = 5.5
alpha_high = 5.6

beta_a = 5.7
beta_o = 5.8

t_cal = 5.9

range_custom = NDIRRangeCalib(zero, span, linear_b, linear_c, alpha_low, alpha_high, beta_a, beta_o, t_cal)

calib = NDIRCalib(ndir_serial, board_serial, selected_range,
                  lamp_voltage, lamp_period, max_deferral, min_deferral,
                  range_iaq, range_safety, range_combustion, range_industrial, range_custom)

print("calib: %s" % calib)
print("-")

jstr = JSONify.dumps(calib)
print(jstr)
print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)

print("store...")
calib = NDIRCalib.construct_from_jdict(jdict)
print("calib: %s" % calib)
print("-")

calib.save(Host)

print("retrieve...")
calib = NDIRCalib.load(Host)
print("calib: %s" % calib)
