"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"rec": "2018-02-21T18:50:32.761+00:00", "cnc": 301.4, "cnc-igl": 53.4, "temp": 28.9}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class NDIRSampleGasDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_sample(cls, rec, sample):
        if not sample:
            return None

        cnc, cnc_igl, temp = sample

        return NDIRSampleGasDatum(rec, cnc, cnc_igl, temp)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        cnc = jdict.get('cnc')
        cnc_igl = jdict.get('cnc-igl')
        temp = jdict.get('temp')

        return NDIRSampleGasDatum(rec, cnc, cnc_igl, temp)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, cnc, cnc_igl, temp):
        """
        Constructor
        """
        self.__rec = rec

        self.__cnc = Datum.float(cnc, 1)
        self.__cnc_igl = Datum.float(cnc_igl, 1)
        self.__temp = Datum.float(temp, 1)


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        # no check of rec field

        if self.cnc != other.cnc:
            return False

        if self.cnc_igl != other.cnc_igl:
            return False

        if self.temp != other.temp:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec.as_json()

        jdict['cnc'] = self.cnc
        jdict['cnc-igl'] = self.cnc_igl
        jdict['temp'] = self.temp

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def cnc(self):
        return self.__cnc


    @property
    def cnc_igl(self):
        return self.__cnc_igl


    @property
    def temp(self):
        return self.__temp


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRSampleGasDatum:{rec:%s, cnc:%s, cnc_igl:%s, temp:%s}" %  \
               (self.rec, self.cnc, self.cnc_igl, self.temp)
