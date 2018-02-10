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


jdict = json.loads(NDIRCalib.CALIB_IAQ, object_pairs_hook=OrderedDict)

calib = NDIRCalib.construct_from_jdict(jdict)
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
