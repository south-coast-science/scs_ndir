"""
Created on 13 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRCmd(JSONable):
    """
    classdocs
    """

    __COMMANDS = None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.__COMMANDS = {
            'vi': NDIRCmd('vi', 0.001, 0.000, 40),              # version ident
            'vt': NDIRCmd('vt', 0.001, 0.000, 11),              # version tag

            'up': NDIRCmd('up', 0.001, 0.000, 4),               # uptime

            'ws': NDIRCmd('ws', 0.001, 0.000, 1),               # watchdog status
            'wc': NDIRCmd('wc', 0.001, 0.000, 0),               # watchdog clear
            'wr': NDIRCmd('wr', 0.001, 2.500, 0),               # watchdog reset

            'er': NDIRCmd('er', 0.001, 0.000, None),            # EEPROM read
            'ew': NDIRCmd('ew', 0.005, 0.010, 0),               # EEPROM write
            'ez': NDIRCmd('ez', 0.005, 0.010, 0),               # EEPROM zero

            'lr': NDIRCmd('lr', 0.001, 0.000, 0),               # lamp run
            'll': NDIRCmd('ll', 0.001, 0.000, 0),               # lamp level

            'ir': NDIRCmd('ir', 0.001, 0.000, 2),               # input raw
            'iv': NDIRCmd('iv', 0.001, 0.000, 4),               # input voltage

            'mc': NDIRCmd('mc', 0.001, 1.000, 0),               # measure calibrate
            'mr': NDIRCmd('mr', 0.001, 0.000, 6),               # measure raw
            'mv': NDIRCmd('mv', 0.001, 0.000, 12),              # measure voltage

            'rs': NDIRCmd('rs', 0.001, 2.200, 0),               # recorder start
            'rp': NDIRCmd('rp', 0.001, 0.000, None),            # recorder play

            'sm': NDIRCmd('sm', 0.001, 2.200, 0),               # sampler mode
            'sr': NDIRCmd('sr', 0.001, 0.000, 6),               # sampler raw
            'sv': NDIRCmd('sv', 0.001, 0.000, 12),              # sampler voltage
            'sg': NDIRCmd('sg', 0.010, 0.000, 12),              # sampler gas

            'sw': NDIRCmd('sw', 0.003, 0.000, 600),             # sampler window
            'sd': NDIRCmd('sd', 0.001, 0.000, 4),               # sampler dump
        }


    @classmethod
    def find(cls, name):
        if name not in cls.__COMMANDS:
            raise ValueError("NDIRCmd.find: unrecognised name: %s." % name)

        return cls.__COMMANDS[name]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, response_time, execution_time, return_count):
        """
        Constructor
        """
        self.__name = name                                              # 2 char string

        self.__response_time = Datum.float(response_time, 3)            # float Seconds
        self.__execution_time = Datum.float(execution_time, 3)          # float Seconds
        self.__return_count = Datum.int(return_count)                   # int or None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['name'] = self.name

        jdict['response-time'] = self.response_time
        jdict['execution-time'] = self.execution_time
        jdict['return-count'] = self.return_count

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def name_bytes(self):
        return ord(self.name[0]), ord(self.name[1])


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def response_time(self):
        return self.__response_time


    @property
    def execution_time(self):
        return self.__execution_time


    @property
    def return_count(self):
        return self.__return_count


    @return_count.setter
    def return_count(self, count):
        self.__return_count = count


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRCmd:{name:%s, response_time:%0.3f, execution_time:%0.3f, return_count:%s}" % \
               (self.name, self.response_time, self.execution_time, self.return_count)
