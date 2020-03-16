"""
Created on 31 Jul 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.datetime import LocalizedDatetime
from scs_core.sampler.sampler import Sampler

from scs_ndir.datum.ndir_pressure_datum import NDIRPressureDatum


# --------------------------------------------------------------------------------------------------------------------

class NDIRPressureSampler(Sampler):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, runner, ndir):
        """
        Constructor
        """
        Sampler.__init__(self, runner)

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

        p_a = self.__ndir.get_sample_pressure()

        return NDIRPressureDatum(rec, p_a)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRPressureSampler:{runner:%s, ndir:%s, interval:%s}" % (self.runner, self.__ndir, self.__interval)
