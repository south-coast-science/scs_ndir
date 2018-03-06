"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRCalib(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -d | -s PATH VALUE}] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--default", "-d", action="store_true", dest="default",
                                 help="load the default settings")

        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set the named field to VALUE")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.default is not None and self.__opts.set is not None:
            return False

        return True


    def set(self):
        return self.__opts.set is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def default(self):
        return self.__opts.default


    @property
    def path(self):
        if self.set():
            return self.__opts.set[0]

        return None


    @property
    def value(self):
        if self.set():
            return self.__opts.set[1]

        return None


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
        return "CmdNDIRCalib:{default:%s, set:%s, verbose:%s, args:%s}" % \
               (self.default, self.__opts.set, self.verbose, self.args)
