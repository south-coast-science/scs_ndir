"""
Created on 8 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

NDIR EEPROM parameters

Alphasense Application Note AAN 201-06
http://www.alphasense.com/WEB1213/wp-content/uploads/2014/12/AAN_201-06.pdf

example JSON:
{"lamp-period": 1000, "lamp-voltage": 5.0, "span": 1, "linear-b": 0.000325, "linear-c": 0.9363,
"temp-beta-o": 1e-05, "temp-alpha": 0.00056, "temp-beta-a": 1e-05,
"therm-a": 0.0, "therm-b": 0.0, "therm-c": 0.0, "therm-d": 0.0,
"t-cal": 1.0}
"""

import os

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRCalib(PersistentJSONable):
    """
    classdocs
    """

    CALIB_IAQ = '{"lamp-voltage": 5.0, "lamp-period": 1000, "max-deferral": 200, "min-deferral": 740, "span": 1, ' \
                '"linear-b": 0.000325, "linear-c": 0.9363, ' \
                '"temp-beta-o": 0.00001, "temp-alpha": 0.00056, "temp-beta-a": 0.00001, ' \
                '"therm-a": 0.0, "therm-b": 0.0, "therm-c": 0.0, "therm-d": 0.0, "t-cal": 1.0}'

    SPAN_IAQ =                       1              # 0 to 5,000 ppm
    SPAN_SAFETY =                    2              # 0 to 50,000 ppm (5%)
    SPAN_COMBUSTION =                3              # 0 to 200,000 ppm (20%)
    SPAN_INDUSTRIAL =                4              # 0 to 1,000,000 ppm (100%)

    # common fields...
    INDEX_LAMP_VOLTAGE =             0
    INDEX_LAMP_PERIOD =              1

    INDEX_MAX_DEFERRAL =             2
    INDEX_MIN_DEFERRAL =             3

    INDEX_SPAN =                     4

    # span fields...
    INDEX_LINEAR_B =                 5
    INDEX_LINEAR_C =                 6
    INDEX_TEMP_BETA_O =              7
    INDEX_TEMP_ALPHA =               8
    INDEX_TEMP_BETA_A =              9
    INDEX_THERM_A =                 10
    INDEX_THERM_B =                 11
    INDEX_THERM_C =                 12
    INDEX_THERM_D =                 13
    INDEX_T_CAL =                   14

    __FILENAME = "ndir_calib.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        lamp_voltage = jdict.get('lamp-voltage')
        lamp_period = jdict.get('lamp-period')

        max_deferral = jdict.get('max-deferral')
        min_deferral = jdict.get('min-deferral')

        span = jdict.get('span')

        linear_b = jdict.get('linear-b')
        linear_c = jdict.get('linear-c')

        temp_beta_o = jdict.get('temp-beta-o')
        temp_alpha = jdict.get('temp-alpha')
        temp_beta_a = jdict.get('temp-beta-a')

        therm_a = jdict.get('therm-a')
        therm_b = jdict.get('therm-b')
        therm_c = jdict.get('therm-c')
        therm_d = jdict.get('therm-d')

        t_cal = jdict.get('t-cal')

        return NDIRCalib(lamp_voltage, lamp_period, max_deferral, min_deferral, span, linear_b, linear_c,
                         temp_beta_o, temp_alpha, temp_beta_a, therm_a, therm_b, therm_c, therm_d, t_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lamp_voltage, lamp_period, max_deferral, min_deferral, span, linear_b, linear_c,
                 temp_beta_o, temp_alpha, temp_beta_a, therm_a, therm_b, therm_c, therm_d, t_cal):
        """
        Constructor
        """
        super().__init__()

        self.__lamp_voltage = Datum.float(lamp_voltage, 1)
        self.__lamp_period = lamp_period

        self.__max_deferral = max_deferral
        self.__min_deferral = min_deferral

        self.__span = span

        self.__linear_b = Datum.float(linear_b, 6)
        self.__linear_c = Datum.float(linear_c, 6)

        self.__temp_beta_o = Datum.float(temp_beta_o, 6)
        self.__temp_alpha = Datum.float(temp_alpha, 6)
        self.__temp_beta_a = Datum.float(temp_beta_a, 6)

        self.__therm_a = Datum.float(therm_a, 6)
        self.__therm_b = Datum.float(therm_b, 6)
        self.__therm_c = Datum.float(therm_c, 6)
        self.__therm_d = Datum.float(therm_d, 6)

        self.__t_cal = Datum.float(t_cal, 6)


    # ----------------------------------------------------------------------------------------------------------------

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
    def therm_a(self):
        return self.__therm_a


    @property
    def therm_b(self):
        return self.__therm_b


    @property
    def therm_c(self):
        return self.__therm_c


    @property
    def therm_d(self):
        return self.__therm_d


    @property
    def t_cal(self):
        return self.__t_cal


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['lamp-voltage'] = self.lamp_voltage
        jdict['lamp-period'] = self.lamp_period

        jdict['max-deferral'] = self.max_deferral
        jdict['min-deferral'] = self.min_deferral

        jdict['span'] = self.span

        jdict['linear-b'] = self.linear_b
        jdict['linear-c'] = self.linear_c

        jdict['temp-beta-o'] = self.temp_beta_o
        jdict['temp-alpha'] = self.temp_alpha
        jdict['temp-beta-a'] = self.temp_beta_a

        jdict['therm-a'] = self.therm_a
        jdict['therm-b'] = self.therm_b
        jdict['therm-c'] = self.therm_c
        jdict['therm-d'] = self.therm_d

        jdict['t-cal'] = self.t_cal

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRCalib:{lamp_voltage:%s, lamp_period:%s, max_deferral:%s, min_deferral:%s, span:%s, " \
               "linear_b:%s, linear_c:%s, temp_beta_o:%s, temp_alpha:%s, temp_beta_a:%s, " \
               "therm_a:%s, therm_b:%s, therm_c:%s, therm_d:%s, t_cal:%s}" %  \
               (self.lamp_voltage, self.lamp_period, self.max_deferral, self.min_deferral, self.span,
                self.linear_b, self.linear_c, self.temp_beta_o, self.temp_alpha, self.temp_beta_a,
                self.therm_a, self.therm_b, self.therm_c, self.therm_d, self.t_cal)
