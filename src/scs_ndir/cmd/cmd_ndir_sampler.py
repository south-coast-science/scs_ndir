"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRSampler(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -m { 1 | 0 } | -w | [-i INTERVAL [-n SAMPLES]] } [-v]",
                                              version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--mode", "-m", type="int", nargs=1, action="store", dest="mode",
                                 help="run continuous (1) or single-shot (0)")

        self.__parser.add_option("--window", "-w", action="store_true", dest="window",
                                 help="report scan of window (single-shot mode only)")

        self.__parser.add_option("--interval", "-i", type="float", nargs=1, action="store", dest="interval",
                                 help="sampling interval in seconds")

        self.__parser.add_option("--samples", "-n", type="int", nargs=1, action="store", dest="samples",
                                 help="number of samples (1 if interval not specified)")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        param_count = 0

        if self.__opts.mode is not None:
            param_count += 1

        if self.__opts.window is not None:
            param_count += 1

        if self.__opts.interval is not None:
            param_count += 1

        if param_count > 1:
            return False

        if self.__opts.samples is not None and self.__opts.interval is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def run(self):
        if len(self.__args) > 0:
            try:
                return bool(int(self.__args[0]))
            except RuntimeError:
                return None

        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mode(self):
        return self.__opts.mode


    @property
    def window(self):
        return self.__opts.window


    @property
    def interval(self):
        return 1.0 if self.__opts.interval is None else self.__opts.interval


    @property
    def samples(self):
        return 1 if self.__opts.interval is None else self.__opts.samples


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdNDIRSampler:{mode:%s, window:%s, interval:%s, samples:%s, verbose:%s, args:%s}" % \
               (self.mode, self.window, self.interval, self.samples, self.verbose, self.args)
