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

class NDIRRecorderDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_sample(cls, sample):
        if not sample:
            return None

        rec, pile_ref, pile_act = sample

        return NDIRRecorderDatum(rec, pile_ref, pile_act)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = jdict.get('rec')

        pile_ref = jdict.get('pile-ref')
        pile_act = jdict.get('pile-act')

        return NDIRRecorderDatum(rec, pile_ref, pile_act)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, pile_ref, pile_act):
        """
        Constructor
        """
        self.__rec = Datum.int(rec)

        self.__pile_ref = Datum.int(pile_ref)
        self.__pile_act = Datum.int(pile_act)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec

        jdict['pile-ref'] = self.pile_ref
        jdict['pile-act'] = self.pile_act

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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRRecorderDatum:{rec:%s, pile_ref:%s, pile_act:%s}" % \
               (self.rec, self.pile_ref, self.pile_act)
