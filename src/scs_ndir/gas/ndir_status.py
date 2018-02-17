"""
Created on 2 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"w-rst": false, "pwr-in": 4.5, "up": {"period": "00-00:21:04.000"}}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable

from scs_ndir.gas.ndir_uptime import NDIRUptime


# --------------------------------------------------------------------------------------------------------------------

class NDIRStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        watchdog_reset = jdict.get('w-rst')
        power_in = jdict.get('pwr-in')

        uptime = NDIRUptime.construct_from_jdict(jdict.get('up'))

        return NDIRStatus(watchdog_reset, power_in, uptime)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, watchdog_reset, power_in, uptime):
        """
        Constructor
        """
        self.__watchdog_reset = watchdog_reset                  # restart because of watchdog timeout       bool
        self.__power_in = Datum.float(power_in, 1)              # PSU input voltage                         float

        self.__uptime = uptime                                  # Uptime


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['w-rst'] = self.watchdog_reset
        jdict['pwr-in'] = self.power_in

        jdict['up'] = self.uptime

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def watchdog_reset(self):
        return self.__watchdog_reset


    @property
    def power_in(self):
        return self.__power_in


    @property
    def uptime(self):
        return self.__uptime


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRStatus:{watchdog_reset:%s, power_in:%s, uptime:%s}" % \
               (self.watchdog_reset, self.power_in, self.uptime)
