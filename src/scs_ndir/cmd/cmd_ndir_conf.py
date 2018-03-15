"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdNDIRConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ [-m MODEL] [-t AVERAGING_TALLY] | -d }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--model", "-m", type="string", nargs=1, action="store", dest="model",
                                 help="set the NDIR MODEL")

        self.__parser.add_option("--tally", "-t", type="int", nargs=1, action="store", dest="tally",
                                 help="set the averaging tally")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete",
                                 help="delete the NDIR configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.model is not None and self.delete:
            return False

        return True


    def is_complete(self):
        if self.model is None or self.tally is None:
            return False

        return True


    def set(self):
        return self.__opts.model is not None or self.__opts.tally is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model


    @property
    def tally(self):
        return self.__opts.tally


    @property
    def delete(self):
        return self.__opts.delete


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
        return "CmdNDIRConf:{model:%s, tally:%s, delete:%s, verbose:%s, args:%s}" % \
                    (self.model, self.tally, self.delete, self.verbose, self.args)
