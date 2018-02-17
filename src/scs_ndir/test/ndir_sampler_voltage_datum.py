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


# --------------------------------------------------------------------------------------------------------------------

class NDIRSampleVoltageDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_sample(cls, rec, sample):
        if not sample:
            return None

        pile_ref_ampl, pile_act_ampl, thermistor_avg = sample

        return NDIRSampleVoltageDatum(rec, pile_ref_ampl, pile_act_ampl, thermistor_avg)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        pile_ref_ampl = jdict.get('pile-ref-ampl')
        pile_act_ampl = jdict.get('pile-act-ampl')
        thermistor_avg = jdict.get('therm-avg')

        return NDIRSampleVoltageDatum(rec, pile_ref_ampl, pile_act_ampl, thermistor_avg)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, pile_ref_ampl, pile_act_ampl, thermistor_avg):
        """
        Constructor
        """
        self.__rec = rec

        self.__pile_ref_ampl = Datum.float(pile_ref_ampl, 4)
        self.__pile_act_ampl = Datum.float(pile_act_ampl, 4)
        self.__thermistor_avg = Datum.float(thermistor_avg, 4)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec.as_json()

        jdict['pile-ref-ampl'] = self.pile_ref_ampl
        jdict['pile-act-ampl'] = self.pile_act_ampl
        jdict['therm-avg'] = self.thermistor_avg

        jdict['pile-diff'] = Datum.float(self.pile_ref_ampl - self.pile_act_ampl, 4)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def pile_ref_ampl(self):
        return self.__pile_ref_ampl


    @property
    def pile_act_ampl(self):
        return self.__pile_act_ampl


    @property
    def thermistor_avg(self):
        return self.__thermistor_avg


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRSampleVoltageDatum:{rec:%s, pile_ref_ampl:%s, pile_act_ampl:%s, thermistor_avg:%s}" % \
               (self.rec, self.pile_ref_ampl, self.pile_act_ampl, self.thermistor_avg)
