"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_ndir import version


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRLamp(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -r ON | -l VOLTAGE } [-v]", version=version())

        # compulsory...
        self.__parser.add_option("--run", "-r", type="int", action="store", dest="run",
                                 help="run (1) or stop (0) the lamp")

        self.__parser.add_option("--level", "-l", type="float", action="store", dest="level",
                                 help="temporarily set lamp voltage")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.run is None and self.level is None:
            return False

        if self.run is not None and self.run != 0 and self.run != 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def run(self):
        return self.__opts.run


    @property
    def level(self):
        return None if self.__opts.level is None else round(self.__opts.level, 1)


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdNDIRLamp:{run:%s, level:%s, verbose:%s}" % (self.run, self.level, self.verbose)
