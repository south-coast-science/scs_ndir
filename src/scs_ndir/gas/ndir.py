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

from scs_ndir.gas.ndir_status import NDIRStatus
from scs_ndir.gas.ndir_uptime import NDIRUptime
from scs_core.gas.ndir_version import NDIRVersion, NDIRTag


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

    __BOOT_DELAY =                      0.500
    __CMD_DELAY =                       0.002

    __RESPONSE_ACK =                    0x01


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __pack_int(byte_values):
        packed = struct.unpack('h', struct.pack('BB', *byte_values))
        return packed[0]


    @staticmethod
    def __pack_unsigned_long(byte_values):
        packed = struct.unpack('L', struct.pack('BBBB', *byte_values))
        return packed[0]


    @staticmethod
    def __pack_float(byte_values):
        packed = struct.unpack('f', struct.pack('BBBB', *byte_values))

        return None if math.isnan(packed[0]) else packed[0]


    @staticmethod
    def __unpack_int(value):
        unpacked = struct.unpack('BB', struct.pack('h', value))

        return unpacked


    @staticmethod
    def __unpack_unsigned_long(value):
        unpacked = struct.unpack('BBBB', struct.pack('L', value))

        return unpacked


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__name__, NDIR.__LOCK_TIMEOUT)


    @classmethod
    def release_lock(cls):
        Lock.release(cls.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, spi_bus, spi_device):
        """
        Constructor
        """
        self.__io = IO()
        self.__spi = HostSPI(spi_bus, spi_device, NDIR.__SPI_MODE, NDIR.__SPI_CLOCK)


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        self.__io.ndir_power = IO.LOW
        time.sleep(self.__BOOT_DELAY)


    def power_off(self):
        self.__io.ndir_power = IO.HIGH


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_echo(self, byte_values):
        size = len(byte_values)
        response = self._command('ec', size, size, *byte_values)

        return response


    def cmd_version(self):
        response = self._command('vi', 17)
        id = ''.join([chr(byte) for byte in response])

        response = self._command('vt', 11)
        tag = ''.join([chr(byte) for byte in response])

        version = NDIRVersion(id, NDIRTag.construct_from_jdict(tag))

        return version


    def cmd_status(self):
        response = self._command('wr', 1)
        watchdog_reset = bool(response)

        response = self._command('mv', 4)
        pwr_in = self.__pack_float(response)

        response = self._command('up', 4)
        seconds = self.__pack_unsigned_long(response)

        status = NDIRStatus(watchdog_reset, pwr_in, NDIRUptime(seconds))

        return status


    def cmd_watchdog_clear(self):
        self._command('wc', 0)


    def cmd_eeprom_read_unsigned_long(self, addr):
        response = self._command('er', 4, addr, 4)
        value = self.__pack_unsigned_long(response)

        return value


    def cmd_eeprom_write_unsigned_long(self, addr, value):
        value_bytes = self.__unpack_unsigned_long(value)
        self._command('ew', 0, addr, 4, *value_bytes)


    def cmd_lamp_set(self, level):
        level_bytes = self.__unpack_int(level)
        response = self._command('ls', 0, *level_bytes)

        return response


    def cmd_monitor_raw(self):
        response = self._command('mr', 2)
        v_in_value = self.__pack_int(response)

        return v_in_value


    def cmd_monitor(self):
        response = self._command('mv', 4)
        v_in_voltage = self.__pack_float(response)

        return v_in_voltage


    def cmd_sample_raw(self):
        response = self._command('sr', 6)

        pile_ref_value = self.__pack_int(response[0:2])
        pile_act_value = self.__pack_int(response[2:4])
        thermistor_value = self.__pack_int(response[4:6])

        return pile_ref_value, pile_act_value, thermistor_value


    def cmd_sample(self):
        response = self._command('sv', 12)

        pile_ref_voltage = self.__pack_float(response[0:4])
        pile_act_voltage = self.__pack_float(response[4:8])
        thermistor_voltage = self.__pack_float(response[8:12])

        return pile_ref_voltage, pile_act_voltage, thermistor_voltage


    # ----------------------------------------------------------------------------------------------------------------

    def _command(self, cmd, return_size, *params):
        try:
            self.obtain_lock()
            self.__spi.open()

            package = [ord(cmd[0]), ord(cmd[1])]
            package.extend(params)

            self.__spi.xfer(package)
            time.sleep(self.__CMD_DELAY)

            response = self.__spi.read_bytes(1)

            if response[0] != self.__RESPONSE_ACK:
                raise ValueError("NACK received for command: %s params: %s" % (cmd, params))

            if return_size < 1:
                return None

            response = self.__spi.read_bytes(return_size)

            return response[0] if return_size == 1 else response

        finally:
            self.__spi.close()
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIR:{io:%s, spi:%s}" % (self.__io, self.__spi)
