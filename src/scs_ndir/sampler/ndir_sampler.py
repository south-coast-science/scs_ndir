"""
Created on 21 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sample.gases_sample import GasesSample
from scs_core.sampler.sampler import Sampler


# --------------------------------------------------------------------------------------------------------------------

class NDIRSampler(Sampler):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, runner, tag, ndir):
        """
        Constructor
        """
        Sampler.__init__(self, runner)

        self.__tag = tag
        self.__ndir = ndir


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        rec = LocalizedDatetime.now()
        co2_datum = self.__ndir.sample()

        return GasesSample(self.__tag, rec, co2_datum, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRSampler:{runner:%s, tag:%s, ndir:%s}" % (self.runner, self.__tag, self.__ndir)
