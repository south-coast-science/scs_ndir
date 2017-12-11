"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import math
import struct
import time

from scs_dfe.board.io import IO

from scs_host.lock.lock import Lock
from scs_host.sys.host_spi import HostSPI


# --------------------------------------------------------------------------------------------------------------------

class NDIR(object):
    """
    classdocs
    """


    # ----------------------------------------------------------------------------------------------------------------

    __LOCK_TIMEOUT =                    1.0


    # ----------------------------------------------------------------------------------------------------------------

    __SPI_CLOCK =                       488000
    __SPI_MODE =                        1

    __CMD_DELAY =                       0.01
    __TRANSFER_DELAY =                  0.00002


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __pack_int(byte_values):
        packed = struct.unpack('h', struct.pack('BB', *byte_values))
        return packed[0]


    @staticmethod
    def __pack_float(byte_values):
        packed = struct.unpack('f', struct.pack('BBBB', *byte_values))

        return None if math.isnan(packed[0]) else packed[0]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__name__, NDIR.__LOCK_TIMEOUT)


    @classmethod
    def release_lock(cls):
        Lock.release(cls.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__io = IO()
        self.__spi = HostSPI(1, NDIR.__SPI_MODE, NDIR.__SPI_CLOCK)


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        self.__io.ndir_power = IO.LOW


    def power_off(self):
        self.__io.ndir_power = IO.HIGH


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        try:
            self.obtain_lock()
            self.__spi.open()

        finally:
            self.__spi.close()
            self.release_lock()


    def firmware(self):
        try:
            self.obtain_lock()
            self.__spi.open()

        finally:
            self.__spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def __read_byte(self):
        time.sleep(NDIR.__TRANSFER_DELAY)
        read_bytes = self.__spi.read_bytes(1)

        return read_bytes[0]


    def __read_int(self):
        read_bytes = []

        for _ in range(2):
            time.sleep(NDIR.__TRANSFER_DELAY)
            read_bytes.extend(self.__spi.read_bytes(1))

        return NDIR.__pack_int(read_bytes)


    def __read_float(self):
        read_bytes = []

        for _ in range(4):
            time.sleep(NDIR.__TRANSFER_DELAY)
            read_bytes.extend(self.__spi.read_bytes(1))

        return NDIR.__pack_float(read_bytes)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIR:{io:%s, spi:%s}" % (self.__io, self.__spi)
