"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"rec": "2018-02-20T12:51:34.181+00:00", "pile-ref-ampl": 2.1037, "pile-act-ampl": 2.0615, "therm-avg": 0.9931}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRSampleVoltageDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_sample(cls, sample):
        if not sample:
            return None

        pile_ref_ampl, pile_act_ampl, thermistor_avg = sample

        return NDIRSampleVoltageDatum(pile_ref_ampl, pile_act_ampl, thermistor_avg)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        pile_ref_ampl = jdict.get('pile-ref-ampl')
        pile_act_ampl = jdict.get('pile-act-ampl')
        thermistor_avg = jdict.get('therm-avg')

        return NDIRSampleVoltageDatum(pile_ref_ampl, pile_act_ampl, thermistor_avg)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pile_ref_ampl, pile_act_ampl, thermistor_avg):
        """
        Constructor
        """
        self.__pile_ref_ampl = Datum.float(pile_ref_ampl, 6)
        self.__pile_act_ampl = Datum.float(pile_act_ampl, 6)
        self.__thermistor_avg = Datum.float(thermistor_avg, 6)


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.pile_ref_ampl != other.pile_ref_ampl:
            return False

        if self.pile_act_ampl != other.pile_act_ampl:
            return False

        if self.thermistor_avg != other.thermistor_avg:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pile-ref-ampl'] = self.pile_ref_ampl
        jdict['pile-act-ampl'] = self.pile_act_ampl
        jdict['therm-avg'] = self.thermistor_avg

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

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
        return "NDIRSampleVoltageDatum:{pile_ref_ampl:%s, pile_act_ampl:%s, thermistor_avg:%s}" % \
               (self.pile_ref_ampl, self.pile_act_ampl, self.thermistor_avg)
