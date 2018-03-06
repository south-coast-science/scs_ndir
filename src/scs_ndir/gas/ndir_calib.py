"""
Created on 8 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

NDIR EEPROM parameters

Alphasense Application Note AAN 201-06
http://www.alphasense.com/WEB1213/wp-content/uploads/2014/12/AAN_201-06.pdf

example JSON:
{"ndir-serial": 12601304, "board-serial": 2, "sensor": 0, "lamp-voltage": 5, "lamp-period": 333,
"max-deferral": 160, "min-deferral": 340, "zero": 1.0, "span": -0.292553,
"linear-b": 0.000325, "linear-c": 0.9363,
"temp-beta-o": 1e-05, "temp-alpha": 0.00056, "temp-beta-a": 1e-05,
"t-cal": 1.0}
"""

import json
import os

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable, PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRCalib(PersistentJSONable):
    """
    classdocs
    """
    CALIB_IAQ = '{"ndir-serial": 0, "board-serial": 0, "selected-range": 1, ' \
                '"lamp-voltage": 4.5, "lamp-period": 333, "max-deferral": 160, "min-deferral": 340, ' \
                '"range-iaq": {"zero": 1.6073, "span": -0.292553, "linear-b": 0.000325, "linear-c": 0.9363, ' \
                '"temp-beta-o": 0.00001, "temp-alpha": 0.00056, "temp-beta-a": 0.00001, "t-cal": 36.0}}'

    # ranges...
    RANGE_IAQ =                     1          # 0 to 5,000 ppm
    RANGE_SAFETY =                  2          # 0 to 5% (50,000 ppm)
    RANGE_COMBUSTION =              3          # 0 to 20% (200,000 ppm)
    RANGE_INDUSTRIAL =              4          # 0 to 100% (1,000,000 ppm)

    # identity...
    INDEX_NDIR_SERIAL =             0          # unsigned long         SET IN CALIBRATION
    INDEX_BOARD_SERIAL =            1          # unsigned long

    INDEX_SELECTED_RANGE =          2          # unsigned int

    # common fields...
    INDEX_LAMP_VOLTAGE =            3          # float

    INDEX_LAMP_PERIOD =             4          # unsigned int
    INDEX_MAX_DEFERRAL =            5          # unsigned int
    INDEX_MIN_DEFERRAL =            6          # unsigned int


    __FILENAME = "ndir_calib.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def default(cls):
        jdict = json.loads(cls.CALIB_IAQ, object_pairs_hook=OrderedDict)

        return NDIRCalib.construct_from_jdict(jdict)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # identity...
        ndir_serial = jdict.get('ndir-serial')
        board_serial = jdict.get('board-serial')

        selected_range = jdict.get('selected-range')

        # common fields...
        lamp_voltage = jdict.get('lamp-voltage')

        lamp_period = jdict.get('lamp-period')
        max_deferral = jdict.get('max-deferral')
        min_deferral = jdict.get('min-deferral')

        # range calibrations...
        range_iaq = NDIRRangeCalib.construct_from_jdict(jdict.get('range-iaq'))
        range_safety = NDIRRangeCalib.construct_from_jdict(jdict.get('range-safety'))
        range_combustion = NDIRRangeCalib.construct_from_jdict(jdict.get('range-combustion'))
        range_industrial = NDIRRangeCalib.construct_from_jdict(jdict.get('range-industrial'))

        return NDIRCalib(ndir_serial, board_serial, selected_range,
                         lamp_voltage, lamp_period, max_deferral, min_deferral,
                         range_iaq, range_safety, range_combustion, range_industrial)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ndir_serial, board_serial, selected_range,
                 lamp_voltage, lamp_period, max_deferral, min_deferral,
                 range_iaq, range_safety, range_combustion, range_industrial):
        """
        Constructor
        """
        super().__init__()

        # identity...
        self.__ndir_serial = ndir_serial                            # unsigned long
        self.__board_serial = board_serial                          # unsigned long

        self.__selected_range = Datum.int(selected_range)

        # common fields...
        self.__lamp_voltage = Datum.float(lamp_voltage, 1)

        self.__lamp_period = Datum.int(lamp_period)
        self.__max_deferral = Datum.int(max_deferral)
        self.__min_deferral = Datum.int(min_deferral)

        # range calibrations...
        self.__range_iaq = range_iaq
        self.__range_safety = range_safety
        self.__range_combustion = range_combustion
        self.__range_industrial = range_industrial


    # ----------------------------------------------------------------------------------------------------------------
    # getters: identity

    @property
    def ndir_serial(self):
        return self.__ndir_serial


    @property
    def board_serial(self):
        return self.__board_serial


    @property
    def selected_range(self):
        return self.__selected_range


    # ----------------------------------------------------------------------------------------------------------------
    # getters: common fields

    @property
    def lamp_voltage(self):
        return self.__lamp_voltage


    @property
    def lamp_period(self):
        return self.__lamp_period


    @property
    def max_deferral(self):
        return self.__max_deferral


    @property
    def min_deferral(self):
        return self.__min_deferral


    # ----------------------------------------------------------------------------------------------------------------
    # getters: range calibrations...

    @property
    def range_iaq(self):
        return self.__range_iaq


    @property
    def range_safety(self):
        return self.__range_safety


    @property
    def range_combustion(self):
        return self.__range_combustion


    @property
    def range_industrial(self):
        return self.__range_industrial


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        # identity...
        jdict['ndir-serial'] = self.ndir_serial
        jdict['board-serial'] = self.board_serial

        jdict['selected-range'] = self.selected_range

        # common fields...
        jdict['lamp-voltage'] = self.lamp_voltage

        jdict['lamp-period'] = self.lamp_period
        jdict['max-deferral'] = self.max_deferral
        jdict['min-deferral'] = self.min_deferral

        # range calibrations...
        jdict['range-iaq'] = self.range_iaq
        jdict['range-safety'] = self.range_safety
        jdict['range-combustion'] = self.range_combustion
        jdict['range-industrial'] = self.range_industrial

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRCalib:{ndir_serial:%s, board_serial:%s, selected_range:%s, " \
               "lamp_voltage:%s, lamp_period:%s, max_deferral:%s, min_deferral:%s, " \
               "range_iaq:%s, range_safety:%s, range_combustion:%s, range_industrial:%s}" %  \
               (self.ndir_serial, self.board_serial, self.selected_range, self.lamp_voltage,
                self.lamp_period, self.max_deferral, self.min_deferral,
                self.range_iaq, self.range_safety, self.range_combustion, self.range_industrial)


# --------------------------------------------------------------------------------------------------------------------

class NDIRRangeCalib(JSONable):
    """
    classdocs
    """

    INDEX_RANGE_IS_SET =            0          # bool

    # range fields...
    INDEX_ZERO =                    1          # float                 SET IN CALIBRATION
    INDEX_SPAN =                    2          # float                 SET IN CALIBRATION

    INDEX_LINEAR_B =                3          # float                 SET IN CALIBRATION
    INDEX_LINEAR_C =                4          # float                 SET IN CALIBRATION

    INDEX_TEMP_BETA_O =             5          # float                 SET IN CALIBRATION
    INDEX_TEMP_ALPHA =              6          # float                 SET IN CALIBRATION
    INDEX_TEMP_BETA_A =             7          # float                 SET IN CALIBRATION

    INDEX_T_CAL =                   8          # float                 SET IN CALIBRATION


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # range fields...
        zero = jdict.get('zero')
        span = jdict.get('span')

        linear_b = jdict.get('linear-b')
        linear_c = jdict.get('linear-c')

        temp_beta_o = jdict.get('temp-beta-o')
        temp_alpha = jdict.get('temp-alpha')
        temp_beta_a = jdict.get('temp-beta-a')

        t_cal = jdict.get('t-cal')

        return NDIRRangeCalib(zero, span, linear_b, linear_c, temp_beta_o, temp_alpha, temp_beta_a, t_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, zero, span, linear_b, linear_c, temp_beta_o, temp_alpha, temp_beta_a, t_cal):
        """
        Constructor
        """
        super().__init__()

        # range fields...
        self.__zero = Datum.float(zero, 6)
        self.__span = Datum.float(span, 6)

        self.__linear_b = Datum.float(linear_b, 6)
        self.__linear_c = Datum.float(linear_c, 6)

        self.__temp_beta_o = Datum.float(temp_beta_o, 6)
        self.__temp_alpha = Datum.float(temp_alpha, 6)
        self.__temp_beta_a = Datum.float(temp_beta_a, 6)

        self.__t_cal = Datum.float(t_cal, 6)


    # ----------------------------------------------------------------------------------------------------------------
    # getters: range calibration fields...

    @property
    def zero(self):
        return self.__zero


    @property
    def span(self):
        return self.__span


    @property
    def linear_b(self):
        return self.__linear_b


    @property
    def linear_c(self):
        return self.__linear_c


    @property
    def temp_beta_o(self):
        return self.__temp_beta_o


    @property
    def temp_alpha(self):
        return self.__temp_alpha


    @property
    def temp_beta_a(self):
        return self.__temp_beta_a


    @property
    def t_cal(self):
        return self.__t_cal


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        # range fields...
        jdict['zero'] = self.zero
        jdict['span'] = self.span

        jdict['linear-b'] = self.linear_b
        jdict['linear-c'] = self.linear_c

        jdict['temp-beta-o'] = self.temp_beta_o
        jdict['temp-alpha'] = self.temp_alpha
        jdict['temp-beta-a'] = self.temp_beta_a

        jdict['t-cal'] = self.t_cal

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRRangeCalib:{zero:%s, span:%s, linear_b:%s, linear_c:%s, " \
               "temp_beta_o:%s, temp_alpha:%s, temp_beta_a:%s, t_cal:%s}" %  \
               (self.zero, self.span, self.linear_b, self.linear_c,
                self.temp_beta_o, self.temp_alpha, self.temp_beta_a, self.t_cal)
