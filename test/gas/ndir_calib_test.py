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

CALIB_TEST = '{"ndir-serial": 3, "board-serial": 2, "selected-range": 1, ' \
             '"lamp-voltage": 4.5, "lamp-period": 333, "max-deferral": 160, "min-deferral": 340, ' \
             '"range-iaq": {"zero": 1.1, "span": 1.2, "linear-b": 1.3, "linear-c": 1.4, ' \
             '"temp-beta-o": 1.5, "temp-alpha": 1.6, "temp-beta-a": 1.7, "t-cal": 1.8}, ' \
             '"range-safety": {"zero": 2.1, "span": 2.2, "linear-b": 2.3, "linear-c": 2.4, ' \
             '"temp-beta-o": 2.5, "temp-alpha": 2.6, "temp-beta-a": 2.7, "t-cal": 2.8}, ' \
             '"range-combustion": {"zero": 3.1, "span": 3.2, "linear-b": 3.3, "linear-c": 3.4, ' \
             '"temp-beta-o": 3.5, "temp-alpha": 3.6, "temp-beta-a": 3.7, "t-cal": 3.8}, ' \
             '"range-industrial": {"zero": 4.1, "span": 4.2, "linear-b": 4.3, "linear-c": 4.4, ' \
             '"temp-beta-o": 4.5, "temp-alpha": 4.6, "temp-beta-a": 4.7, "t-cal": 4.8}}'

jdict = json.loads(CALIB_TEST, object_pairs_hook=OrderedDict)

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
