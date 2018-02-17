"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIREEPROM(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -g NAME | -s NAME VALUE | -r } [-v]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--get", "-g", type="string", nargs=1, action="store", dest="get",
                                 help="get the value of the named field")

        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set the named field to VALUE")

        self.__parser.add_option("--report", "-r", action="store_true", dest="report",
                                 help="report full EEPROM contents")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        param_count = 0

        if self.__opts.get is not None:
            param_count += 1

        if self.__opts.set is not None:
            param_count += 1

        if self.__opts.report is not None:
            param_count += 1

        if param_count != 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def get(self):
        return self.__opts.get is not None


    def set(self):
        return self.__opts.set is not None


    def report(self):
        return self.__opts.report is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        if self.get():
            return self.__opts.get

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
        return "CmdNDIREEPROM:{get:%s, set:%s, verbose:%s, args:%s}" % \
               (self.__opts.get, self.__opts.set, self.verbose, self.args)
