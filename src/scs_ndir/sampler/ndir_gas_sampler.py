"""
Created on 21 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.sampler.sampler import Sampler

from scs_ndir.datum.ndir_sampler_gas_datum import NDIRSampleGasDatum


# --------------------------------------------------------------------------------------------------------------------

class NDIRGasSampler(Sampler):
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
        sample = self.__ndir.sample_gas()

        return NDIRSampleGasDatum.construct_from_sample(rec, sample)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRGasSampler:{runner:%s, ndir:%s}" % (self.runner, self.__ndir)
