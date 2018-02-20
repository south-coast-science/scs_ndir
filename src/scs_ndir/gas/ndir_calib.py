"""
Created on 8 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

NDIR EEPROM parameters

Alphasense Application Note AAN 201-06
http://www.alphasense.com/WEB1213/wp-content/uploads/2014/12/AAN_201-06.pdf

example JSON:
{"ndir-serial": 12601304, "board-serial": 2, "sensor": 0,
"lamp-voltage": 5.0, "lamp-period": 500, "max-deferral": 220, "min-deferral": 480,
"zero": 1.0, "span": 2.0, "linear-b": 0.000325, "linear-c": 0.9363,
"temp-beta-o": 1e-05, "temp-alpha": 0.00056, "temp-beta-a": 1e-05,
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

    CALIB_IAQ = '{"ndir-serial": 12601304, "board-serial": 2, "sensor": 0, ' \
                '"lamp-voltage": 5.0, "lamp-period": 500, "max-deferral": 220, "min-deferral": 480, ' \
                '"zero": 1.0, "span": 2.0, "linear-b": 0.000325, "linear-c": 0.9363, ' \
                '"temp-beta-o": 0.00001, "temp-alpha": 0.00056, "temp-beta-a": 0.00001, "t-cal": 1.0}'

    # sensor ranges...
    SENSOR_IAQ =                     0          # 0 to 5,000 ppm
    SENSOR_SAFETY =                  1          # 0 to 50,000 ppm (5%)
    SENSOR_COMBUSTION =              2          # 0 to 200,000 ppm (20%)
    SENSOR_INDUSTRIAL =              3          # 0 to 1,000,000 ppm (100%)

    # TODO: lamp voltage points?

    # common fields...
    INDEX_NDIR_SERIAL =              0          # unsigned long         SET IN CALIBRATION
    INDEX_BOARD_SERIAL =             1          # unsigned long

    INDEX_SENSOR =                   2          # unsigned int          SET IN CALIBRATION

    INDEX_LAMP_VOLTAGE =             3          # unsigned int
    INDEX_LAMP_PERIOD =              4          # unsigned int

    INDEX_MAX_DEFERRAL =             5          # unsigned int
    INDEX_MIN_DEFERRAL =             6          # unsigned int

    # RANGE fields...
    INDEX_ZERO =                     7          # float                 SET IN CALIBRATION
    INDEX_SPAN =                     8          # float                 SET IN CALIBRATION

    INDEX_LINEAR_B =                 9          # float                 SET IN CALIBRATION
    INDEX_LINEAR_C =                10          # float                 SET IN CALIBRATION

    INDEX_TEMP_BETA_O =             11          # float                 SET IN CALIBRATION
    INDEX_TEMP_ALPHA =              12          # float                 SET IN CALIBRATION
    INDEX_TEMP_BETA_A =             13          # float                 SET IN CALIBRATION

    INDEX_T_CAL =                   14          # float                 SET IN CALIBRATION


    __FILENAME = "ndir_calib.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # common fields...
        ndir_serial = jdict.get('ndir-serial')
        board_serial = jdict.get('board-serial')

        sensor = jdict.get('sensor')

        lamp_voltage = jdict.get('lamp-voltage')
        lamp_period = jdict.get('lamp-period')

        max_deferral = jdict.get('max-deferral')
        min_deferral = jdict.get('min-deferral')

        # RANGE fields...
        zero = jdict.get('zero')
        span = jdict.get('span')

        linear_b = jdict.get('linear-b')
        linear_c = jdict.get('linear-c')

        temp_beta_o = jdict.get('temp-beta-o')
        temp_alpha = jdict.get('temp-alpha')
        temp_beta_a = jdict.get('temp-beta-a')

        t_cal = jdict.get('t-cal')

        return NDIRCalib(ndir_serial, board_serial, sensor, lamp_voltage, lamp_period, max_deferral, min_deferral,
                         zero, span, linear_b, linear_c, temp_beta_o, temp_alpha, temp_beta_a, t_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ndir_serial, board_serial, sensor, lamp_voltage, lamp_period, max_deferral, min_deferral,
                 zero, span, linear_b, linear_c, temp_beta_o, temp_alpha, temp_beta_a, t_cal):
        """
        Constructor
        """
        super().__init__()

        # common fields...
        self.__ndir_serial = ndir_serial
        self.__board_serial = board_serial

        self.__sensor = Datum.int(sensor)

        self.__lamp_voltage = Datum.int(lamp_voltage)
        self.__lamp_period = Datum.int(lamp_period)

        self.__max_deferral = Datum.int(max_deferral)
        self.__min_deferral = Datum.int(min_deferral)

        # RANGE fields...
        self.__zero = Datum.float(zero, 6)
        self.__span = Datum.float(span, 6)

        self.__linear_b = Datum.float(linear_b, 6)
        self.__linear_c = Datum.float(linear_c, 6)

        self.__temp_beta_o = Datum.float(temp_beta_o, 6)
        self.__temp_alpha = Datum.float(temp_alpha, 6)
        self.__temp_beta_a = Datum.float(temp_beta_a, 6)

        self.__t_cal = Datum.float(t_cal, 6)


    # ----------------------------------------------------------------------------------------------------------------
    # getters: common fields

    @property
    def ndir_serial(self):
        return self.__ndir_serial


    @property
    def board_serial(self):
        return self.__board_serial


    @property
    def sensor(self):
        return self.__sensor

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
    # getters: RANGE fields

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

        # common fields...
        jdict['ndir-serial'] = self.ndir_serial
        jdict['board-serial'] = self.board_serial

        jdict['sensor'] = self.sensor

        jdict['lamp-voltage'] = self.lamp_voltage
        jdict['lamp-period'] = self.lamp_period

        jdict['max-deferral'] = self.max_deferral
        jdict['min-deferral'] = self.min_deferral

        # RANGE fields...
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
        return "NDIRCalib:{ndir_serial:%s, board_serial:%s, sensor:%s, lamp_voltage:%s, lamp_period:%s, " \
               "max_deferral:%s, min_deferral:%s, zero:%s, span:%s, " \
               "linear_b:%s, linear_c:%s, temp_beta_o:%s, temp_alpha:%s, temp_beta_a:%s, t_cal:%s}" %  \
               (self.ndir_serial, self.board_serial, self.sensor, self.lamp_voltage, self.lamp_period,
                self.max_deferral, self.min_deferral, self.zero, self.span,
                self.linear_b, self.linear_c, self.temp_beta_o, self.temp_alpha, self.temp_beta_a, self.t_cal)
