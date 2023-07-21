"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_ndir import version


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRRecorder(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog -i INTERVAL -n SAMPLES [-d DEFERRAL] [-v]",
                                              version=version())

        # compulsory...
        self.__parser.add_option("--interval", "-i", type="int", action="store", dest="interval",
                                 help="sampling interval in milliseconds")

        self.__parser.add_option("--samples", "-n", type="int", action="store", dest="samples",
                                 help="number of samples")

        # optional...
        self.__parser.add_option("--deferral", "-d", type="int", action="store", dest="deferral", default=0,
                                 help="deferral from PWM edge in milliseconds (default 0, max 999)")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.interval is None or self.samples is None:
            return False

        if self.interval < 1:
            return False

        if self.samples < 1:
            return False

        if self.deferral < 0 or self.deferral > 999:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interval(self):
        return self.__opts.interval


    @property
    def samples(self):
        return self.__opts.samples


    @property
    def deferral(self):
        return self.__opts.deferral


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdNDIRRecorder:{interval:%s, samples:%s, deferral:%s, verbose:%s}" % \
               (self.interval, self.samples, self.deferral, self.verbose)
