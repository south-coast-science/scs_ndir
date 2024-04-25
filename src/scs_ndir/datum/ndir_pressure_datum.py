"""
Created on 31 Jul 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"rec": "2018-02-17T13:01:25.584+00:00", "pile-ref-ampl": 2.6213, "pile-act-ampl": 2.5588, "therm-avg": 0.9949,
"pile-diff": 0.0625}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class NDIRPressureDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        p_a = jdict.get('pA')

        return NDIRPressureDatum(rec, p_a)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, p_a):
        """
        Constructor
        """
        self.__rec = rec
        self.__p_a = Datum.float(p_a, 1)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['rec'] = self.rec.as_iso8601(include_millis=Sample.INCLUDE_MILLIS)
        jdict['pA'] = self.p_a

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def p_a(self):
        return self.__p_a


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRPressureDatum:{rec:%s, p_a:%s}" % (self.rec, self.p_a)
