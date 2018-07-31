"""
Created on 31 Jul 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.localized_datetime import LocalizedDatetime
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


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        rec = LocalizedDatetime.now()
        p_a = self.__ndir.pressure()

        return NDIRPressureDatum(rec, p_a)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRPressureSampler:{runner:%s, ndir:%s}" % (self.runner, self.__ndir)
