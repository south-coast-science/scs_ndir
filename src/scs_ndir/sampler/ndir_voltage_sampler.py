"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sample.gases_sample import GasesSample
from scs_core.sampler.sampler import Sampler

from scs_ndir.datum.ndir_sampler_voltage_datum import NDIRSampleVoltageDatum


# --------------------------------------------------------------------------------------------------------------------

class NDIRVoltageSampler(Sampler):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, runner, system_id, ndir):
        """
        Constructor
        """
        Sampler.__init__(self, runner)

        self.__tag = system_id.message_tag()
        self.__ndir = ndir


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        rec = LocalizedDatetime.now()

        sample = self.__ndir.cmd_sample_voltage()
        co2_datum = NDIRSampleVoltageDatum.construct_from_sample(sample)

        return GasesSample(self.__tag, rec, co2_datum, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRVoltageSampler:{runner:%s, ndir:%s}" % (self.runner, self.__ndir)
