"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies whether on not an NDIR is model

example JSON:
{"model": true}
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(PersistentJSONable):
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
        avg_period = jdict.get('avg-period')

        return NDIRConf(model, avg_period)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, avg_period):
        """
        Constructor
        """
        super().__init__()

        self.__model = model
        self.__avg_period = avg_period


    # ----------------------------------------------------------------------------------------------------------------

    def ndir(self, host):               # TODO: handle multiple NDIR models / NDIR monitor
        if self.model is None:
            return None

        return NDIR(host.ndir_spi_bus(), host.ndir_spi_device())


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def avg_period(self):
        return self.__avg_period


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model
        jdict['avg-period'] = self.avg_period

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRConf:{model:%s, avg_period:%s}" %  (self.model, self.avg_period)
