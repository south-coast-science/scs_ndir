"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import math
import struct
import time

from scs_core.gas.co2_datum import CO2Datum
from scs_core.gas.ndir_datum import NDIRDatum

from scs_dfe.board.io import IO

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock

from scs_ndir.gas.ndir_status import NDIRStatus
from scs_ndir.gas.ndir_uptime import NDIRUptime
from scs_core.gas.ndir_version import NDIRVersion, NDIRTag


# --------------------------------------------------------------------------------------------------------------------

class NDIR(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    RECOVERY_TIME =                     3.0             # time between bad SPI interaction and MCU recovery

    RESET_QUARANTINE =                  8.0             # time between reset and stable readings


    # ----------------------------------------------------------------------------------------------------------------

    __INDEX_TIME_TO_SAMPLE =             0
    __INDEX_TIME_AFTER_SAMPLE =          1
    __INDEX_COEFF_B =                    2
    __INDEX_COEFF_C =                    3
    __INDEX_THERM_A =                    4
    __INDEX_THERM_B =                    5
    __INDEX_THERM_C =                    6
    __INDEX_THERM_D =                    7
    __INDEX_ALPHA =                      8
    __INDEX_BETA_A =                     9
    __INDEX_T_CAL =                     10

    __LOCK_TIMEOUT =                    3.0

    __SPI_CLOCK =                       488000
    __SPI_MODE =                        1

    __RESET_DELAY =                     2.000           # seconds
    __BOOT_DELAY =                      0.500           # seconds
    __CMD_DELAY =                       0.002           # seconds

    __RESPONSE_ACK =                    0x01
    __RESPONSE_NACK =                   0x00


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __pack_int(byte_values):
        packed = struct.unpack('h', struct.pack('BB', *byte_values))
        return packed[0]


    @staticmethod
    def __pack_unsigned_int(byte_values):
        packed = struct.unpack('H', struct.pack('BB', *byte_values))
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
    def __unpack_unsigned_int(value):
        unpacked = struct.unpack('BB', struct.pack('H', value))

        return unpacked


    @staticmethod
    def __unpack_unsigned_long(value):
        unpacked = struct.unpack('BBBB', struct.pack('L', value))

        return unpacked


    @staticmethod
    def __unpack_float(value):
        unpacked = struct.unpack('BBBB', struct.pack('f', value))

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
        self.__spi = SPI(spi_bus, spi_device, NDIR.__SPI_MODE, NDIR.__SPI_CLOCK)


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        self.__io.ndir_power = IO.LOW
        time.sleep(self.__BOOT_DELAY)


    def power_off(self):
        self.__io.ndir_power = IO.HIGH


    # ----------------------------------------------------------------------------------------------------------------
    # sampling...

    # noinspection PyMethodMayBeStatic
    def sample(self):
        return NDIRDatum(None, None, None, None)        # TODO: implement sample


    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def sample_co2(self, ideal_gas_law):                # TODO: implement sample_co2
        return CO2Datum(None)


    # noinspection PyMethodMayBeStatic
    def sample_temp(self):                              # TODO: implement sample_temp
        return None


    # noinspection PyMethodMayBeStatic
    def sample_dc(self):                                # TODO: implement sample_dc
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_echo(self, byte_values):
        try:
            self.obtain_lock()

            size = len(byte_values)
            response = self._command('ec', size, size, *byte_values)

        finally:
            self.release_lock()

        return response


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_version(self):
        try:
            self.obtain_lock()

            response = self._command('vi', 40)
            id = ''.join([chr(byte) for byte in response]).strip()

            response = self._command('vt', 11)
            tag = ''.join([chr(byte) for byte in response]).strip()

            version = NDIRVersion(id, NDIRTag.construct_from_jdict(tag))

        finally:
            self.release_lock()

        return version


    def cmd_status(self):
        try:
            self.obtain_lock()

            response = self._command('ws', 1)
            watchdog_reset = bool(response)

            response = self._command('mv', 4)
            pwr_in = self.__pack_float(response)

            response = self._command('up', 4)
            seconds = self.__pack_unsigned_long(response)

            status = NDIRStatus(watchdog_reset, pwr_in, NDIRUptime(seconds))

        finally:
            self.release_lock()

        return status


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_watchdog_clear(self):
        try:
            self.obtain_lock()

            self._command('wc', 0)

        finally:
            self.release_lock()


    def cmd_reset(self):
        try:
            self.obtain_lock()

            self._command('wr', 0)
            time.sleep(NDIR.__RESET_DELAY + NDIR.__BOOT_DELAY)

            self._command('wc', 0)      # clear watchdog flag because reset was commanded

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_eeprom_read_time_to_sample(self):
        return self._cmd_eeprom_read_unsigned_int(self.__INDEX_TIME_TO_SAMPLE)


    def cmd_eeprom_write_time_to_sample(self, time_to_sample):
        self._cmd_eeprom_write_unsigned_int(self.__INDEX_TIME_TO_SAMPLE, time_to_sample)


    def cmd_eeprom_read_time_after_sample(self):
        return self._cmd_eeprom_read_unsigned_int(self.__INDEX_TIME_AFTER_SAMPLE)


    def cmd_eeprom_write_time_after_sample(self, time_after_sample):
        self._cmd_eeprom_write_unsigned_int(self.__INDEX_TIME_AFTER_SAMPLE, time_after_sample)


    def cmd_eeprom_read_coeff_b(self):
        return self._cmd_eeprom_read_float(self.__INDEX_COEFF_B)


    def cmd_eeprom_write_coeff_b(self, coeff_b):
        self._cmd_eeprom_write_float(self.__INDEX_COEFF_B, coeff_b)


    def cmd_eeprom_read_coeff_c(self):
        return self._cmd_eeprom_read_float(self.__INDEX_COEFF_C)


    def cmd_eeprom_write_coeff_c(self, coeff_c):
        self._cmd_eeprom_write_float(self.__INDEX_COEFF_C, coeff_c)


    def cmd_eeprom_read_therm_a(self):
        return self._cmd_eeprom_read_float(self.__INDEX_THERM_A)


    def cmd_eeprom_write_therm_a(self, therm_a):
        self._cmd_eeprom_write_float(self.__INDEX_THERM_A, therm_a)


    def cmd_eeprom_read_therm_b(self):
        return self._cmd_eeprom_read_float(self.__INDEX_THERM_B)


    def cmd_eeprom_write_therm_b(self, therm_b):
        self._cmd_eeprom_write_float(self.__INDEX_THERM_B, therm_b)


    def cmd_eeprom_read_therm_c(self):
        return self._cmd_eeprom_read_float(self.__INDEX_THERM_C)


    def cmd_eeprom_write_therm_c(self, therm_c):
        self._cmd_eeprom_write_float(self.__INDEX_THERM_C, therm_c)


    def cmd_eeprom_read_therm_d(self):
        return self._cmd_eeprom_read_float(self.__INDEX_THERM_D)


    def cmd_eeprom_write_therm_d(self, therm_d):
        self._cmd_eeprom_write_float(self.__INDEX_THERM_D, therm_d)


    def cmd_eeprom_read_alpha(self):
        return self._cmd_eeprom_read_float(self.__INDEX_ALPHA)


    def cmd_eeprom_write_alpha(self, alpha):
        self._cmd_eeprom_write_float(self.__INDEX_ALPHA, alpha)


    def cmd_eeprom_read_beta_a(self):
        return self._cmd_eeprom_read_float(self.__INDEX_BETA_A)


    def cmd_eeprom_write_beta_a(self, beta_a):
        self._cmd_eeprom_write_float(self.__INDEX_BETA_A, beta_a)


    def cmd_eeprom_read_t_cal(self):
        return self._cmd_eeprom_read_float(self.__INDEX_T_CAL)


    def cmd_eeprom_write_t_cal(self, t_cal):
        self._cmd_eeprom_write_float(self.__INDEX_T_CAL, t_cal)


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_lamp_level(self, voltage):
        try:
            self.obtain_lock()

            voltage_bytes = self.__unpack_float(voltage)
            response = self._command('ll', 0, *voltage_bytes)

        finally:
            self.release_lock()

        return response


    def cmd_lamp_pwm(self, period):
        try:
            self.obtain_lock()

            period_bytes = self.__unpack_int(period)
            response = self._command('lp', 0, *period_bytes)

        finally:
            self.release_lock()

        return response


    def cmd_lamp_run(self, on):
        try:
            self.obtain_lock()

            on_byte = 1 if on else 0
            response = self._command('lr', 0, on_byte)

        finally:
            self.release_lock()

        return response


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_monitor_raw(self):
        try:
            self.obtain_lock()

            response = self._command('mr', 2)
            v_in_value = self.__pack_int(response)

        finally:
            self.release_lock()

        return v_in_value


    def cmd_monitor(self):
        try:
            self.obtain_lock()

            response = self._command('mv', 4)
            v_in_voltage = self.__pack_float(response)

        finally:
            self.release_lock()

        return v_in_voltage


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_sample_raw(self):
        try:
            self.obtain_lock()

            response = self._command('sr', 6)

            pile_ref_value = self.__pack_unsigned_int(response[0:2])
            pile_act_value = self.__pack_unsigned_int(response[2:4])
            thermistor_value = self.__pack_unsigned_int(response[4:6])

        finally:
            self.release_lock()

        return pile_ref_value, pile_act_value, thermistor_value


    def cmd_sample(self):
        try:
            self.obtain_lock()

            response = self._command('sv', 12)

            pile_ref_voltage = self.__pack_float(response[0:4])
            pile_act_voltage = self.__pack_float(response[4:8])
            thermistor_voltage = self.__pack_float(response[8:12])

        finally:
            self.release_lock()

        return pile_ref_voltage, pile_act_voltage, thermistor_voltage


    def cmd_run_recorder(self, count):
        try:
            self.obtain_lock()

            count_bytes = self.__unpack_unsigned_int(count)
            response = self._command('rr', count * 6, *count_bytes)

            values = []

            for i in range(0, count * 6, 6):
                timestamp = self.__pack_unsigned_int(response[i:i + 2])
                pile_ref_voltage = self.__pack_unsigned_int(response[i + 2:i + 4])
                pile_act_voltage = self.__pack_unsigned_int(response[i + 4:i + 6])

                values.append((timestamp, pile_ref_voltage, pile_act_voltage))

        finally:
            self.release_lock()

        return values


    # ----------------------------------------------------------------------------------------------------------------

    def _cmd_eeprom_read_unsigned_int(self, index):
        try:
            self.obtain_lock()

            response = self._command('er', 2, index)
            value = self.__pack_unsigned_int(response)

        finally:
            self.release_lock()

        return value


    def _cmd_eeprom_write_unsigned_int(self, index, value):
        try:
            self.obtain_lock()

            value_bytes = self.__unpack_unsigned_int(value)
            self._command('ew', 0, index, *value_bytes)

        finally:
            self.release_lock()


    def _cmd_eeprom_read_float(self, index):
        try:
            self.obtain_lock()

            response = self._command('er', 4, index)
            value = self.__pack_float(response)

        finally:
            self.release_lock()

        return value


    def _cmd_eeprom_write_float(self, index, value):
        try:
            self.obtain_lock()

            value_bytes = self.__unpack_float(value)
            self._command('ew', 0, index, *value_bytes)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_fail(self):
        try:
            self.obtain_lock()

            self._command('mr', 0)          # should return two bytes - ignore these

        finally:
            self.release_lock()




    # ----------------------------------------------------------------------------------------------------------------

    def _command(self, cmd, return_size, *params):
        print("cmd: %s return_size: %d params:%s len:%d" % (cmd, return_size, str(params), len(params)))

        try:
            self.__spi.open()

            # request...
            request = [ord(cmd[0]), ord(cmd[1])]
            request.extend(params)

            self.__spi.xfer(request)
            time.sleep(self.__CMD_DELAY)

            if cmd == 'rr':
                time.sleep(1.0)

            # ACK...
            response = self.__spi.read_bytes(1)

            if response[0] != self.__RESPONSE_ACK:
                raise ValueError("NACK received for command: %s params: %s" % (cmd, params))

            # response...
            if return_size < 1:
                return None

            response = self.__spi.read_bytes(return_size)

            print("response: %s" % str(response))

            return response[0] if return_size == 1 else response

        finally:
            self.__spi.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIR:{io:%s, spi:%s}" % (self.__io, self.__spi)
