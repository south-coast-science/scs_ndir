"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"rec": "2018-02-17T13:01:25.584+00:00", "pile-ref-ampl": 2.6213, "pile-act-ampl": 2.5588, "therm-avg": 0.9949,
"pile-diff": 0.0625}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class NDIRMeasureVoltageDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_sample(cls, rec, sample):
        if not sample:
            return None

        pile_ref, pile_act, thermistor = sample

        return NDIRMeasureVoltageDatum(rec, pile_ref, pile_act, thermistor)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        pile_ref = jdict.get('pile-ref')
        pile_act = jdict.get('pile-act')
        thermistor = jdict.get('therm')

        return NDIRMeasureVoltageDatum(rec, pile_ref, pile_act, thermistor)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, pile_ref, pile_act, thermistor):
        """
        Constructor
        """
        self.__rec = rec

        self.__pile_ref = Datum.float(pile_ref, 4)
        self.__pile_act = Datum.float(pile_act, 4)
        self.__thermistor = Datum.float(thermistor, 4)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec.as_iso8601(Sample.INCLUDE_MILLIS)

        jdict['pile-ref'] = self.pile_ref
        jdict['pile-act'] = self.pile_act
        jdict['therm'] = self.thermistor

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def pile_ref(self):
        return self.__pile_ref


    @property
    def pile_act(self):
        return self.__pile_act


    @property
    def thermistor(self):
        return self.__thermistor


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRMeasureVoltageDatum:{rec:%s, pile_ref:%s, pile_act:%s, thermistor:%s}" % \
               (self.rec, self.pile_ref, self.pile_act, self.thermistor)
