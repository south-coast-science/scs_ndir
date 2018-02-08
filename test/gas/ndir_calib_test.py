#!/usr/bin/env python3

"""
Created on 8 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_ndir.gas.ndir_calib import NDIRCalib


# --------------------------------------------------------------------------------------------------------------------

lamp_period =   1000

coeff_b =       -0.00043
coeff_c =       1 / 0.89

therm_a =       1.1
therm_b =       2.2
therm_c =       3.3
therm_d =       4.4

alpha =         5.5
beta_a =        6.6

t_cal =         7.7


calib = NDIRCalib(lamp_period, coeff_b, coeff_c, therm_a, therm_b, therm_c, therm_d, alpha, beta_a, t_cal)
print("calib: %s" % calib)
print("-")

jstr = JSONify.dumps(calib)
print(jstr)
print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)

calib = NDIRCalib.construct_from_jdict(jdict)
print("calib: %s" % calib)
print("=")

calib.save(Host)

calib = NDIRCalib.load(Host)
print("calib: %s" % calib)
print("-")
