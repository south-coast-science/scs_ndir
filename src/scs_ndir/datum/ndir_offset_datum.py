"""
Created on 1 Aug 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"min-ref-offset": 939, "min-act-offset": 958, "max-ref-offset": 490, "max-act-offset": 487}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIROffsetDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_sample(cls, sample):
        if not sample:
            return None

        min_ref_offset, min_act_offset, max_ref_offset, max_act_offset = sample

        return NDIROffsetDatum(min_ref_offset, min_act_offset, max_ref_offset, max_act_offset)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        min_ref_offset = jdict.get('min_ref_offset')
        min_act_offset = jdict.get('min_act_offset')

        max_ref_offset = jdict.get('max_ref_offset')
        max_act_offset = jdict.get('max_act_offset')

        return NDIROffsetDatum(min_ref_offset, min_act_offset, max_ref_offset, max_act_offset)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, min_ref_offset, min_act_offset, max_ref_offset, max_act_offset):
        """
        Constructor
        """
        self.__min_ref_offset = min_ref_offset
        self.__min_act_offset = min_act_offset

        self.__max_ref_offset = max_ref_offset
        self.__max_act_offset = max_act_offset


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['min-ref-offset'] = self.min_ref_offset
        jdict['min-act-offset'] = self.min_act_offset

        jdict['max-ref-offset'] = self.max_ref_offset
        jdict['max-act-offset'] = self.max_act_offset

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def min_ref_offset(self):
        return self.__min_ref_offset


    @property
    def min_act_offset(self):
        return self.__min_act_offset


    @property
    def max_ref_offset(self):
        return self.__max_ref_offset


    @property
    def max_act_offset(self):
        return self.__max_act_offset


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIROffsetDatum:{min_ref_offset:%s, min_act_offset:%s, max_ref_offset:%s, max_act_offset:%s}" % \
               (self.min_ref_offset, self.min_act_offset, self.max_ref_offset, self.max_act_offset)
