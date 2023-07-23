"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_ndir import version


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRSampler(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { [-i INTERVAL [-n SAMPLES] [-r]] | -o } [-v]",
                                              version=version())

        # compulsory...
        self.__parser.add_option("--interval", "-i", type="float", action="store", dest="interval",
                                 help="sampling interval in seconds")

        self.__parser.add_option("--samples", "-n", type="int", action="store", dest="samples",
                                 help="number of samples (1 if interval not specified)")

        self.__parser.add_option("--raw", "-r", action="store_true", dest="raw", default=False,
                                 help="report voltages instead of concentrations")

        self.__parser.add_option("--offsets", "-o", action="store_true", dest="offsets",
                                 help="get the latest min / max offsets")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        param_count = 0

        if self.__opts.interval is not None:
            param_count += 1

        if self.__opts.offsets is not None:
            param_count += 1

        if param_count > 1:
            return False

        if self.__opts.samples is not None and self.__opts.interval is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interval(self):
        return 1.0 if self.__opts.interval is None else self.__opts.interval


    @property
    def samples(self):
        return 1 if self.__opts.interval is None else self.__opts.samples


    @property
    def raw(self):
        return self.__opts.raw


    @property
    def offsets(self):
        return self.__opts.offsets


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdNDIRSampler:{interval:%s, samples:%s, raw:%s, offsets:%s, verbose:%s}" % \
               (self.interval, self.samples, self.offsets, self.raw, self.verbose)
