"""
Created on 21 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sampler.sampler import Sampler


# --------------------------------------------------------------------------------------------------------------------

class NDIRTempSampler(Sampler):
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
        sample = self.__ndir.sample_temp()

        return sample


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRTempSampler:{runner:%s, ndir:%s}" % (self.runner, self.__ndir)
