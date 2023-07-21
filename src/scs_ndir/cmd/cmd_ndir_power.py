"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_ndir import version


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRPower(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { 1 | 0 } [-v]", version=version())

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.power is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def power(self):
        if len(self.__args) > 0:
            try:
                return bool(int(self.__args[0]))
            except RuntimeError:
                return None

        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdNDIRPower:{power:%d, verbose:%s}" % (self.power, self.verbose)
