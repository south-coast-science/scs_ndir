"""
Created on 22 Aug 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

This package is compatible with the following microcontroller firmware:
https://github.com/south-coast-science/scs_spi_ndir_t1_mcu_f1
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SPINDIRt1f1Cmd(JSONable):
    """
    classdocs
    """

    __COMMANDS = None

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        cls.__COMMANDS = {
            'vi': SPINDIRt1f1Cmd('vi', 0.001, 0.000, 40),           # version ident
            'vt': SPINDIRt1f1Cmd('vt', 0.001, 0.000, 11),           # version tag

            'up': SPINDIRt1f1Cmd('up', 0.001, 0.000, 4),            # uptime

            'ws': SPINDIRt1f1Cmd('ws', 0.001, 0.000, 1),            # watchdog status
            'wc': SPINDIRt1f1Cmd('wc', 0.001, 0.000, 0),            # watchdog clear
            'wr': SPINDIRt1f1Cmd('wr', 0.001, 2.500, 0),            # watchdog reset

            'cr': SPINDIRt1f1Cmd('cr', 0.002, 0.000, None),         # calib read
            'cw': SPINDIRt1f1Cmd('cw', 0.004, 0.010, 0),            # calib write
            'cl': SPINDIRt1f1Cmd('cl', 0.010, 2.200, 0),            # calib load

            'lr': SPINDIRt1f1Cmd('lr', 0.001, 0.000, 0),            # lamp run

            'ir': SPINDIRt1f1Cmd('ir', 0.001, 0.000, 2),            # input raw
            'iv': SPINDIRt1f1Cmd('iv', 0.001, 0.000, 4),            # input voltage

            'mc': SPINDIRt1f1Cmd('mc', 0.001, 1.000, 0),            # measure calibrate
            'mr': SPINDIRt1f1Cmd('mr', 0.001, 0.000, 6),            # measure raw
            'mv': SPINDIRt1f1Cmd('mv', 0.001, 0.000, 12),           # measure voltage

            'rs': SPINDIRt1f1Cmd('rs', 0.001, None, 0),             # recorder start (time depends on period /count)
            'rp': SPINDIRt1f1Cmd('rp', 0.001, 0.000, None),         # recorder play

            'sp': SPINDIRt1f1Cmd('sp', 0.001, None, 0),             # sampler mode (time depends on lamp cycle)
            'sr': SPINDIRt1f1Cmd('sr', 0.001, 0.000, 6),            # sampler raw
            'sv': SPINDIRt1f1Cmd('sv', 0.001, 0.000, 12),           # sampler voltage
            'sg': SPINDIRt1f1Cmd('sg', 0.010, 0.000, 12),           # sampler gas

            'so': SPINDIRt1f1Cmd('so', 0.001, 0.000, 8),            # sampler offsets

            'sb': SPINDIRt1f1Cmd('sb', 0.001, 0.000, 4),            # sampler actual barometric pressure
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
        return "NDIRCmd:{name:%s, response_time:%s, execution_time:%s, return_count:%s}" % \
               (self.name, self.response_time, self.execution_time, self.return_count)
