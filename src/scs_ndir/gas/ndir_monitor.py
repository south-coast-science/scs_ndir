"""
Created on 28 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.data.average import Average

from scs_core.gas.ndir.ndir_datum import NDIRDatum

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_host.lock.lock_timeout import LockTimeout


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
        self.__averaging = Average(conf.tally)


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def start(self):
        try:
            self.__ndir.power_on()
            self.__averaging.reset()

            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        try:
            super().stop()

            self.__ndir.power_off()

        except (BrokenPipeError, KeyboardInterrupt, LockTimeout):
            pass


    def run(self):
        sleep_time = self.__ndir.get_sample_interval()
        timer = IntervalTimer(sleep_time + 0.2)

        try:
            while timer.true():
                self.__ndir.sample()
                time.sleep(sleep_time)

                datum = self.__ndir.get_sample_gas()

                self.__averaging.append(datum)
                average = self.__averaging.compute()

                # report...
                with self._lock:
                    average.as_list(self._value)

        except (BrokenPipeError, KeyboardInterrupt, LockTimeout):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # data retrieval for client process...

    def firmware(self):
        return self.__ndir.version()


    def sample(self):
        with self._lock:
            value = self._value

        return NDIRDatum.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRMonitor:{value:%s, averaging:%s, ndir:%s}" % (self._value, self.__averaging, self.__ndir)
