"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"rec": 840, "pile-ref": 4367, "pile-act": 4785, "thermistor": 10284}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRWindowDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_sample(cls, rec, sample):
        if not sample:
            return None

        pile_ref, pile_act, thermistor = sample

        return NDIRWindowDatum(rec, pile_ref, pile_act, thermistor)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = jdict.get('rec')

        pile_ref = jdict.get('pile-ref')
        pile_act = jdict.get('pile-act')
        thermistor = jdict.get('therm')

        return NDIRWindowDatum(rec, pile_ref, pile_act, thermistor)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, pile_ref, pile_act, thermistor):
        """
        Constructor
        """
        self.__rec = Datum.int(rec)

        self.__pile_ref = Datum.int(pile_ref)
        self.__pile_act = Datum.int(pile_act)
        self.__thermistor = Datum.int(thermistor)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec

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
        return "NDIRWindowDatum:{rec:%s, pile_ref:%s, pile_act:%s, thermistor:%s}" % \
               (self.rec, self.pile_ref, self.pile_act, self.thermistor)
