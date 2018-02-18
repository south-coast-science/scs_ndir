"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRException(RuntimeError, JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, problem, status, cmd, params):
        """
        Constructor
        """
        self.__problem = problem

        self.__status = status
        self.__cmd = cmd
        self.__params = params


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['problem'] = self.problem

        jdict['status'] = self.status
        jdict['cmd'] = self.cmd
        jdict['params'] = self.params

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def problem(self):
        return self.__problem


    @property
    def status(self):
        return self.__status


    @property
    def cmd(self):
        return self.__cmd


    @property
    def params(self):
        return self.__params


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRException:{problem:%s, status:%s, cmd:%s, params:%s}" % \
               (self.problem, self.status, self.cmd, self.params)
