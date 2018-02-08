"""
Created on 8 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

manages EEPROM parameters for the NDIR

example JSON:
{"lamp-period": 1000, "coeff-b": -0.00043, "coeff-c": 1.1235955056179776,
"therm-a": 1.1, "therm-b": 2.2, "therm-c": 3.3, "therm-d": 4.4, "alpha": 5.5, "beta-a": 6.6, "t-cal": 7.7}"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRCalib(PersistentJSONable):
    """
    classdocs
    """
    INDEX_LAMP_PERIOD =                 0
    INDEX_COEFF_B =                     1
    INDEX_COEFF_C =                     2
    INDEX_THERM_A =                     3
    INDEX_THERM_B =                     4
    INDEX_THERM_C =                     5
    INDEX_THERM_D =                     6
    INDEX_ALPHA =                       7
    INDEX_BETA_A =                      8
    INDEX_T_CAL =                       9

    __FILENAME = "ndir_calib.json"

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        lamp_period = jdict.get('lamp-period')

        coeff_b = jdict.get('coeff-b')
        coeff_c = jdict.get('coeff-c')

        therm_a = jdict.get('therm-a')
        therm_b = jdict.get('therm-b')
        therm_c = jdict.get('therm-c')
        therm_d = jdict.get('therm-d')

        alpha = jdict.get('alpha')
        beta_a = jdict.get('beta-a')

        t_cal = jdict.get('t-cal')

        return NDIRCalib(lamp_period, coeff_b, coeff_c, therm_a, therm_b, therm_c, therm_d, alpha, beta_a, t_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lamp_period, coeff_b, coeff_c, therm_a, therm_b, therm_c, therm_d, alpha, beta_a, t_cal):
        """
        Constructor
        """
        super().__init__()

        self.__lamp_period = lamp_period

        self.__coeff_b = Datum.float(coeff_b, 6)
        self.__coeff_c = Datum.float(coeff_c, 6)

        self.__therm_a = Datum.float(therm_a, 6)
        self.__therm_b = Datum.float(therm_b, 6)
        self.__therm_c = Datum.float(therm_c, 6)
        self.__therm_d = Datum.float(therm_d, 6)

        self.__alpha = Datum.float(alpha, 6)
        self.__beta_a = Datum.float(beta_a, 6)

        self.__t_cal = Datum.float(t_cal, 6)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lamp_period(self):
        return self.__lamp_period


    @property
    def coeff_b(self):
        return self.__coeff_b


    @property
    def coeff_c(self):
        return self.__coeff_c


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
    def alpha(self):
        return self.__alpha


    @property
    def beta_a(self):
        return self.__beta_a


    @property
    def t_cal(self):
        return self.__t_cal


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['lamp-period'] = self.lamp_period

        jdict['coeff-b'] = self.coeff_b
        jdict['coeff-c'] = self.coeff_c

        jdict['therm-a'] = self.therm_a
        jdict['therm-b'] = self.therm_b
        jdict['therm-c'] = self.therm_c
        jdict['therm-d'] = self.therm_d

        jdict['alpha'] = self.alpha
        jdict['beta-a'] = self.beta_a

        jdict['t-cal'] = self.t_cal

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRCalib:{lamp_period:%s, coeff_b:%s, coeff_c:%s, therm_a:%s, therm_b:%s, therm_c:%s, therm_d:%s, " \
               "alpha:%s, beta_a:%s, t_cal:%s}" %  \
               (self.lamp_period, self.coeff_b, self.coeff_c, self.therm_a, self.therm_b, self.therm_c, self.therm_d,
                self.alpha, self.beta_a, self.t_cal)
