"""
Created on 22 Aug 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

NDIR EEPROM parameters

Alphasense Application Note AAN 201-06
http://www.alphasense.com/WEB1213/wp-content/uploads/2014/12/AAN_201-06.pdf

This package is compatible with the following microcontroller firmware:
https://github.com/south-coast-science/scs_spi_ndir_t1_mcu_f1

example JSON:
{"ndir-serial": 12700000, "board-serial": 1000000, "selected-range": 1, "lamp-voltage": 4.5,
"lamp-period": 900, "sample-start": 440, "sample-end": 940,
"range-iaq": {"zero": 1.1765, "span": 0.2203, "linear-b": 0.000325, "linear-c": 0.9363,
"alpha-low": 0.00042, "alpha-high": 0.00042, "beta-a": 1e-05, "beta-o": 1e-05, "t-cal": 40.5},
"range-safety": null, "range-combustion": null, "range-industrial": null, "range-custom": null}
"""

import json

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable, PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRCalib(PersistentJSONable):
    """
    classdocs
    """
    CALIB_IAQ = '{"ndir-serial": 12700000, "board-serial": 1000000, "selected-range": 1, "lamp-voltage": 4.5, ' \
                '"lamp-period": 1000, "sample-start": 400, "sample-end": 990, ' \
                '"range-iaq": {"zero": 1.1765, "span": 0.2203, "linear-b": 0.000325, "linear-c": 0.9363, ' \
                '"alpha-low": 0.00042, "alpha-high": 0.00042, "beta-a": 1e-05, "beta-o": 1e-05, "t-cal": 40.5}, ' \
                '"range-safety": null, "range-combustion": null, "range-industrial": null, "range-custom": null}'

    # ranges...
    RANGE_IAQ =                     1          # 0 to 5,000 ppm
    RANGE_SAFETY =                  2          # 0 to 5% (50,000 ppm)
    RANGE_COMBUSTION =              3          # 0 to 20% (200,000 ppm)
    RANGE_INDUSTRIAL =              4          # 0 to 100% (1,000,000 ppm)
    RANGE_CUSTOM =                  5          # 0 to customer-specified

    # identity...
    INDEX_NDIR_SERIAL =             0          # unsigned long         SET IN CALIBRATION
    INDEX_BOARD_SERIAL =            1          # unsigned long

    INDEX_SELECTED_RANGE =          2          # unsigned int

    # common fields...
    INDEX_LAMP_VOLTAGE =            3          # float

    INDEX_LAMP_PERIOD =             4          # unsigned int
    INDEX_SAMPLE_START =            5          # unsigned int
    INDEX_SAMPLE_END =              6          # unsigned int


    __FILENAME = "ndir_calib.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def default(cls):
        jdict = json.loads(cls.CALIB_IAQ)

        return NDIRCalib.construct_from_jdict(jdict)


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        # identity...
        ndir_serial = jdict.get('ndir-serial')
        board_serial = jdict.get('board-serial')

        selected_range = jdict.get('selected-range')

        # common fields...
        lamp_voltage = jdict.get('lamp-voltage')

        lamp_period = jdict.get('lamp-period')
        sample_start = jdict.get('sample-start')
        sample_end = jdict.get('sample-end')

        # range calibrations...
        range_iaq = NDIRRangeCalib.construct_from_jdict(jdict.get('range-iaq'))
        range_safety = NDIRRangeCalib.construct_from_jdict(jdict.get('range-safety'))
        range_combustion = NDIRRangeCalib.construct_from_jdict(jdict.get('range-combustion'))
        range_industrial = NDIRRangeCalib.construct_from_jdict(jdict.get('range-industrial'))
        range_custom = NDIRRangeCalib.construct_from_jdict(jdict.get('range-custom'))

        return NDIRCalib(ndir_serial, board_serial, selected_range,
                         lamp_voltage, lamp_period, sample_start, sample_end,
                         range_iaq, range_safety, range_combustion, range_industrial, range_custom)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ndir_serial, board_serial, selected_range,
                 lamp_voltage, lamp_period, sample_start, sample_end,
                 range_iaq, range_safety, range_combustion, range_industrial, range_custom):
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
        self.__sample_start = Datum.int(sample_start)
        self.__sample_end = Datum.int(sample_end)

        # range calibrations...
        self.__range_iaq = range_iaq
        self.__range_safety = range_safety
        self.__range_combustion = range_combustion
        self.__range_industrial = range_industrial
        self.__range_custom = range_custom


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
    def sample_start(self):
        return self.__sample_start


    @property
    def sample_end(self):
        return self.__sample_end


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


    @property
    def range_custom(self):
        return self.__range_custom


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
        jdict['sample-start'] = self.sample_start
        jdict['sample-end'] = self.sample_end

        # range calibrations...
        jdict['range-iaq'] = self.range_iaq
        jdict['range-safety'] = self.range_safety
        jdict['range-combustion'] = self.range_combustion
        jdict['range-industrial'] = self.range_industrial
        jdict['range-custom'] = self.range_custom

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRCalib:{ndir_serial:%s, board_serial:%s, selected_range:%s, " \
               "lamp_voltage:%s, lamp_period:%s, sample_start:%s, sample_end:%s, " \
               "range_iaq:%s, range_safety:%s, range_combustion:%s, range_industrial:%s, range_custom:%s}" %  \
               (self.ndir_serial, self.board_serial, self.selected_range,
                self.lamp_voltage, self.lamp_period, self.sample_start, self.sample_end,
                self.range_iaq, self.range_safety, self.range_combustion, self.range_industrial, self.range_custom)


# --------------------------------------------------------------------------------------------------------------------

class NDIRRangeCalib(JSONable):
    """
    classdocs
    """

    INDEX_RANGE_IS_SET =        0          # bool

    # range fields...
    INDEX_ZERO =                1          # float                 SET IN CALIBRATION
    INDEX_SPAN =                2          # float                 SET IN CALIBRATION

    INDEX_LINEAR_B =            3          # float                 SET IN CALIBRATION
    INDEX_LINEAR_C =            4          # float                 SET IN CALIBRATION

    INDEX_ALPHA_LOW =           5          # float                 SET IN CALIBRATION
    INDEX_ALPHA_HIGH =          6          # float                 SET IN CALIBRATION

    INDEX_BETA_A =              7          # float                 SET IN CALIBRATION
    INDEX_BETA_O =              8          # float                 SET IN CALIBRATION

    INDEX_T_CAL =               9          # float                 SET IN CALIBRATION


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

        alpha_low = jdict.get('alpha-low')
        alpha_high = jdict.get('alpha-high')

        beta_a = jdict.get('beta-a')
        beta_o = jdict.get('beta-o')

        t_cal = jdict.get('t-cal')

        return NDIRRangeCalib(zero, span, linear_b, linear_c, alpha_low, alpha_high, beta_a, beta_o, t_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, zero, span, linear_b, linear_c, alpha_low, alpha_high, beta_a, beta_o, t_cal):
        """
        Constructor
        """
        # range fields...
        self.__zero = Datum.float(zero, 6)
        self.__span = Datum.float(span, 6)

        self.__linear_b = Datum.float(linear_b, 6)
        self.__linear_c = Datum.float(linear_c, 6)

        self.__alpha_low = Datum.float(alpha_low, 6)
        self.__alpha_high = Datum.float(alpha_high, 6)

        self.__beta_a = Datum.float(beta_a, 6)
        self.__beta_o = Datum.float(beta_o, 6)

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
    def alpha_low(self):
        return self.__alpha_low


    @property
    def alpha_high(self):
        return self.__alpha_high


    @property
    def beta_a(self):
        return self.__beta_a


    @property
    def beta_o(self):
        return self.__beta_o


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

        jdict['alpha-low'] = self.alpha_low
        jdict['alpha-high'] = self.alpha_high

        jdict['beta-a'] = self.beta_a
        jdict['beta-o'] = self.beta_o

        jdict['t-cal'] = self.t_cal

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRRangeCalib:{zero:%s, span:%s, linear_b:%s, linear_c:%s, " \
               "alpha_low:%s, alpha_high:%s, beta_a:%s, beta_o:%s, t_cal:%s}" %  \
               (self.zero, self.span, self.linear_b, self.linear_c,
                self.alpha_low, self.alpha_high, self.beta_a, self.beta_o, self.t_cal)
