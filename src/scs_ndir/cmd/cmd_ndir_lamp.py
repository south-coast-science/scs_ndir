"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRLamp(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -r ON | -l LEVEL } [-v]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--level", "-l", type="int", nargs=1, action="store", dest="level",
                                 help="temporarily set lamp voltage")

        self.__parser.add_option("--run", "-r", type="int", nargs=1, action="store", dest="run",
                                 help="run (1) or stop (0) the lamp")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.level is None and self.run is None:
            return False

        if self.run is not None and self.run != 0 and self.run != 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def level(self):
        return self.__opts.level


    @property
    def run(self):
        return self.__opts.run


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
        return "CmdNDIRLamp:{level:%d, run:%d, verbose:%s, args:%s}" % \
               (self.level, self.run, self.verbose, self.args)
