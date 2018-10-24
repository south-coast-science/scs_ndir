"""
Created on 1 Aug 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRRunMode(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -s | -c } [-v]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--single", "-s", action="store_true", dest="single", default=False,
                                 help="single-shot mode")

        self.__parser.add_option("--continuous", "-c", action="store_true", dest="continuous", default=False,
                                 help="continuous mode")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.single and self.continuous:
            return False

        if not self.single and not self.continuous:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def single(self):
        return self.__opts.single


    @property
    def continuous(self):
        return self.__opts.continuous


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
        return "CmdNDIRRunMode:{single:%s, continuous:%s, verbose:%s, args:%s}" % \
               (self.single, self.continuous, self.verbose, self.args)