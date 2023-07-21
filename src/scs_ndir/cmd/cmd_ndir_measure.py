"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_ndir import version


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRMeasure(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-i INTERVAL [-n SAMPLES]] [-v]", version=version())

        # compulsory...
        self.__parser.add_option("--interval", "-i", type="float", action="store", dest="interval",
                                 help="sampling interval in seconds >= 0.01")

        self.__parser.add_option("--samples", "-n", type="int", action="store", dest="samples",
                                 help="number of samples")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.interval is None and self.__opts.samples is not None:
            return False

        if self.interval < 0.01:
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
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdNDIRMeasure:{interval:%s, samples:%s, verbose:%s}" % (self.interval, self.samples, self.verbose)
