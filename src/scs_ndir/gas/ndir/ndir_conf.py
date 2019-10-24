"""
Created on 28 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"model": "t1f1", "tally": 10, "raw": false}
"""

from scs_core.gas.ndir.ndir_conf import NDIRConf as AbstractNDIRConf

from scs_ndir.gas.ndir.ndir_monitor import NDIRMonitor

from scs_ndir.gas.ndir.spi_ndir_t1_f1.ndir_calib import NDIRCalib as SPINDIRv1Calib
from scs_ndir.gas.ndir.spi_ndir_t1_f1.spi_ndir_t1_f1 import SPINDIRt1f1


# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(AbstractNDIRConf):
    """
    classdocs
    """

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls._FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        model = jdict.get('model')
        tally = jdict.get('tally')
        raw = jdict.get('raw', False)

        return NDIRConf(model, tally, raw)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, tally, raw=False):
        """
        Constructor
        """
        super().__init__(model, tally, raw)


    # ----------------------------------------------------------------------------------------------------------------
    # AbstractNDIRConf implementation...

    def ndir_monitor(self, interface, host):
        return NDIRMonitor(self.ndir(interface, host), self)


    def ndir(self, interface, host):
        if self.model is None:
            raise ValueError('unknown model: %s' % self.model)

        # TODO: check against a list of supported devices

        return SPINDIRt1f1(interface, host.ndir_spi_bus(), host.ndir_spi_device())


    # ----------------------------------------------------------------------------------------------------------------

    def calib_class(self):
        if self.model is None:
            raise ValueError('unknown model: %s' % self.model)

        return SPINDIRv1Calib
