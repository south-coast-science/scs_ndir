"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.sampler.sampler import Sampler

from scs_ndir.datum.ndir_measure_voltage_datum import NDIRMeasureVoltageDatum


# --------------------------------------------------------------------------------------------------------------------

class NDIRVoltageMeasure(Sampler):
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
        sample = self.__ndir.measure_voltage()

        return NDIRMeasureVoltageDatum.construct_from_sample(rec, sample)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRVoltageMeasure:{runner:%s, ndir:%s}" % (self.runner, self.__ndir)
