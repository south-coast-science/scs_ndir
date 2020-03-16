"""
Created on 21 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.datetime import LocalizedDatetime

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

        self.__interval = self.__ndir.get_sample_interval()


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        rec = LocalizedDatetime.now().utc()

        self.__ndir.sample()

        try:
            time.sleep(self.__interval)
        except KeyboardInterrupt:
            pass

        co2_datum = self.__ndir.get_sample_gas()

        return GasesSample(self.__tag, rec, co2_datum, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRSampler:{runner:%s, tag:%s, ndir:%s, interval:%s}" % \
               (self.runner, self.__tag, self.__ndir, self.__interval)
