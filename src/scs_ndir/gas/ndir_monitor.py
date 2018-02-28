"""
Created on 28 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.gas.ndir_datum import NDIRDatum

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_host.lock.lock_timeout import LockTimeout

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

class NDIRMonitor(SynchronisedProcess):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ndir, conf):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__ndir = ndir
        self.__conf = conf


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        self.__ndir.sample()     # reset counts

        try:
            timer = IntervalTimer(NDIR.SAMPLE_INTERVAL)

            while timer.true():
                sample = self.__ndir.sample()

                # report...
                with self._lock:
                    sample.as_list(self._value)

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        try:
            self.__ndir.power_on()

            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        try:
            super().stop()

            self.__ndir.power_off()

        except KeyboardInterrupt:
            pass

        except LockTimeout:             # __power_cycle() may be running!
            pass


    def sample(self):
        with self._lock:
            value = self._value

        return NDIRDatum.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRMonitor:{value:%s, ndir:%s, conf:%s}" % (self._value, self.__ndir, self.__conf)
