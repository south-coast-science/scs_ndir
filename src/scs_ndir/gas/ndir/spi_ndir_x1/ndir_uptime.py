"""
Created on 2 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"period": "00-00:07:20.000"}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class NDIRUptime(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        timedelta = Timedelta.construct_from_ps_elapsed_report(jdict.get('period'))

        return NDIRUptime(timedelta.delta.total_seconds())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, seconds):
        """
        Constructor
        """
        self.__seconds = Datum.int(seconds)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['period'] = self.timedelta

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def seconds(self):
        return self.__seconds


    @property
    def timedelta(self):
        return Timedelta(seconds=self.seconds)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRUptime:{seconds:%s}" % self.seconds
