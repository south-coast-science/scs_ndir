"""
Created on 28 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"model": "SPINDIRv1", "tally": 10}
"""

import os

from collections import OrderedDict

from scs_core.gas.ndir_conf import NDIRConf as AbstractNDIRConf
from scs_core.gas.ndir_monitor import NDIRMonitor

from scs_ndir.gas.spi_ndir_v1.ndir_calib import NDIRCalib as SPINDIRv1Calib
from scs_ndir.gas.spi_ndir_v1.spi_ndir_v1 import SPINDIRv1


# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(AbstractNDIRConf):
    """
    classdocs
    """

    __FILENAME = "ndir_conf.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.conf_dir(), cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        model = jdict.get('model')
        tally = jdict.get('tally')

        return NDIRConf(model, tally)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, tally):
        """
        Constructor
        """
        super().__init__()

        self.__model = model
        self.__tally = tally


    # ----------------------------------------------------------------------------------------------------------------

    def ndir_monitor(self, host):
        return NDIRMonitor(self.ndir(host), self)


    def ndir(self, host):
        if self.model is None:
            raise ValueError('unknown model: %s' % self.model)

        return SPINDIRv1(host.ndir_spi_bus(), host.ndir_spi_device())


    def calib_class(self):
        if self.model is None:
            raise ValueError('unknown model: %s' % self.model)

        return SPINDIRv1Calib


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def tally(self):
        return self.__tally


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model
        jdict['tally'] = self.tally

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRConf:{model:%s, tally:%s}" %  (self.model, self.tally)
