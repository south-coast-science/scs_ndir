"""
Created on 13 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# TODO: cmd execution times are based on lamp cycle - but what is the lamp cycle time??

# --------------------------------------------------------------------------------------------------------------------

class SPINDIRv1Cmd(JSONable):
    """
    classdocs
    """

    __COMMANDS = None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.__COMMANDS = {
            'vi': SPINDIRv1Cmd('vi', 0.001, 0.000, 40),             # version ident
            'vt': SPINDIRv1Cmd('vt', 0.001, 0.000, 11),             # version tag

            'up': SPINDIRv1Cmd('up', 0.001, 0.000, 4),              # uptime

            'ws': SPINDIRv1Cmd('ws', 0.001, 0.000, 1),              # watchdog status
            'wc': SPINDIRv1Cmd('wc', 0.001, 0.000, 0),              # watchdog clear
            'wr': SPINDIRv1Cmd('wr', 0.001, 2.500, 0),              # watchdog reset

            'cr': SPINDIRv1Cmd('cr', 0.001, 0.000, None),           # calib read
            'cw': SPINDIRv1Cmd('cw', 0.002, 0.010, 0),              # calib write
            'cl': SPINDIRv1Cmd('cl', 0.010, 2.200, 0),              # calib load

            'lr': SPINDIRv1Cmd('lr', 0.001, 0.000, 0),              # lamp run
            'll': SPINDIRv1Cmd('ll', 0.001, 0.000, 0),              # lamp level

            'ir': SPINDIRv1Cmd('ir', 0.001, 0.000, 2),              # input raw
            'iv': SPINDIRv1Cmd('iv', 0.001, 0.000, 4),              # input voltage

            'mc': SPINDIRv1Cmd('mc', 0.001, 1.000, 0),              # measure calibrate
            'mr': SPINDIRv1Cmd('mr', 0.001, 0.000, 6),              # measure raw
            'mv': SPINDIRv1Cmd('mv', 0.001, 0.000, 12),             # measure voltage

            'rs': SPINDIRv1Cmd('rs', 0.001, 1.100, 0),              # recorder start (time depends on period /count)
            'rp': SPINDIRv1Cmd('rp', 0.001, 0.000, None),           # recorder play

            'sm': SPINDIRv1Cmd('sm', 0.001, 2.200, 0),              # sampler mode
            'sr': SPINDIRv1Cmd('sr', 0.001, 0.000, 6),              # sampler raw
            'sv': SPINDIRv1Cmd('sv', 0.001, 0.000, 12),             # sampler voltage
            'sg': SPINDIRv1Cmd('sg', 0.010, 0.000, 12),             # sampler gas

            'so': SPINDIRv1Cmd('so', 0.001, 0.000, 8),              # sampler offsets

            'sp': SPINDIRv1Cmd('sp', 0.001, 0.000, 4),              # sampler actual barometric pressure
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
