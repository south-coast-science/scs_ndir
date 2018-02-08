"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import math
import struct
import time

from scs_core.gas.co2_datum import CO2Datum
from scs_core.gas.ndir_datum import NDIRDatum
from scs_core.gas.ndir_version import NDIRVersion, NDIRTag

from scs_dfe.board.io import IO

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock

from scs_ndir.gas.ndir_status import NDIRStatus
from scs_ndir.gas.ndir_uptime import NDIRUptime

from scs_ndir.gas.ndir_calib import NDIRCalib


# --------------------------------------------------------------------------------------------------------------------

class NDIR(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    RECOVERY_TIME =                     1.0             # time between bad SPI interaction and MCU recovery

    RESET_QUARANTINE =                  8.0             # time between reset and stable readings


    # ----------------------------------------------------------------------------------------------------------------

    __LOCK_TIMEOUT =                    3.0

    __SPI_CLOCK =                       488000
    __SPI_MODE =                        1

    __RESET_DELAY =                     2.000           # seconds
    __BOOT_DELAY =                      0.500           # seconds
    __CMD_DELAY =                       0.001           # seconds
    __EEPROM_WRITE_DELAY =              0.01            # seconds

    __RESPONSE_ACK =                    0x01
    __RESPONSE_NACK =                   0x02


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

    def cmd_version(self):
        try:
            self.obtain_lock()

            response = self._command(40, 'vi')
            id = ''.join([chr(byte) for byte in response]).strip()

            response = self._command(11, 'vt')
            tag = ''.join([chr(byte) for byte in response]).strip()

            version = NDIRVersion(id, NDIRTag.construct_from_jdict(tag))

            return version

        finally:
            self.release_lock()


    def cmd_status(self):
        try:
            self.obtain_lock()

            response = self._command(1, 'ws')
            watchdog_reset = bool(response)

            response = self._command(4, 'mv')
            pwr_in = self.__pack_float(response)

            response = self._command(4, 'up')
            seconds = self.__pack_unsigned_long(response)

            status = NDIRStatus(watchdog_reset, pwr_in, NDIRUptime(seconds))

            return status

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_watchdog_clear(self):
        try:
            self.obtain_lock()

            self._command(0, 'wc')

        finally:
            self.release_lock()


    def cmd_reset(self):
        try:
            self.obtain_lock()

            self._command(0, 'wr')
            time.sleep(NDIR.__RESET_DELAY + NDIR.__BOOT_DELAY)

            self._command(0, 'wc')      # clear watchdog flag because reset was commanded

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_store_eeprom_calib(self, calib):
        try:
            self.obtain_lock()

            self._cmd_eeprom_write_unsigned_int(NDIRCalib.INDEX_LAMP_PERIOD, calib.lamp_period)

            self._cmd_eeprom_write_float(NDIRCalib.INDEX_COEFF_B, calib.coeff_b)
            self._cmd_eeprom_write_float(NDIRCalib.INDEX_COEFF_C, calib.coeff_c)

            self._cmd_eeprom_write_float(NDIRCalib.INDEX_THERM_A, calib.therm_a)
            self._cmd_eeprom_write_float(NDIRCalib.INDEX_THERM_B, calib.therm_b)
            self._cmd_eeprom_write_float(NDIRCalib.INDEX_THERM_C, calib.therm_c)
            self._cmd_eeprom_write_float(NDIRCalib.INDEX_THERM_D, calib.therm_d)

            self._cmd_eeprom_write_float(NDIRCalib.INDEX_ALPHA, calib.alpha)
            self._cmd_eeprom_write_float(NDIRCalib.INDEX_BETA_A, calib.beta_a)

            self._cmd_eeprom_write_float(NDIRCalib.INDEX_T_CAL, calib.t_cal)

        finally:
            self.release_lock()


    def cmd_retrieve_eeprom_calib(self):
        try:
            self.obtain_lock()

            lamp_period = self._cmd_eeprom_read_unsigned_int(NDIRCalib.INDEX_LAMP_PERIOD)

            coeff_b = self._cmd_eeprom_read_float(NDIRCalib.INDEX_COEFF_B)
            coeff_c = self._cmd_eeprom_read_float(NDIRCalib.INDEX_COEFF_C)

            therm_a = self._cmd_eeprom_read_float(NDIRCalib.INDEX_THERM_A)
            therm_b = self._cmd_eeprom_read_float(NDIRCalib.INDEX_THERM_B)
            therm_c = self._cmd_eeprom_read_float(NDIRCalib.INDEX_THERM_C)
            therm_d = self._cmd_eeprom_read_float(NDIRCalib.INDEX_THERM_D)

            alpha = self._cmd_eeprom_read_float(NDIRCalib.INDEX_ALPHA)
            beta_a = self._cmd_eeprom_read_float(NDIRCalib.INDEX_BETA_A)

            t_cal = self._cmd_eeprom_read_float(NDIRCalib.INDEX_T_CAL)

            return NDIRCalib(lamp_period, coeff_b, coeff_c, therm_a, therm_b, therm_c, therm_d, alpha, beta_a, t_cal)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_lamp_level(self, voltage):
        try:
            self.obtain_lock()

            voltage_bytes = self.__unpack_float(voltage)
            self._command(0, 'll', voltage_bytes)

        finally:
            self.release_lock()


    def cmd_lamp_pwm(self, period):
        try:
            self.obtain_lock()

            period_bytes = self.__unpack_int(period)
            self._command(0, 'lp', period_bytes)

        finally:
            self.release_lock()


    def cmd_lamp_run(self, on):
        try:
            self.obtain_lock()

            on_byte = 1 if on else 0
            self._command(0, 'lr', (on_byte, ))

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_monitor_raw(self):
        try:
            self.obtain_lock()

            response = self._command(2, 'mr')
            v_in_value = self.__pack_int(response)

            return v_in_value

        finally:
            self.release_lock()


    def cmd_monitor(self):
        try:
            self.obtain_lock()

            response = self._command(4, 'mv')
            v_in_voltage = self.__pack_float(response)

            return v_in_voltage

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_sample_raw(self):
        try:
            self.obtain_lock()

            response = self._command(6, 'sr')

            pile_ref_value = self.__pack_unsigned_int(response[0:2])
            pile_act_value = self.__pack_unsigned_int(response[2:4])
            thermistor_value = self.__pack_unsigned_int(response[4:6])

            return pile_ref_value, pile_act_value, thermistor_value

        finally:
            self.release_lock()


    def cmd_sample(self):
        try:
            self.obtain_lock()

            response = self._command(12, 'sv')

            pile_ref_voltage = self.__pack_float(response[0:4])
            pile_act_voltage = self.__pack_float(response[4:8])
            thermistor_voltage = self.__pack_float(response[8:12])

            return pile_ref_voltage, pile_act_voltage, thermistor_voltage

        finally:
            self.release_lock()



    # ----------------------------------------------------------------------------------------------------------------

    def cmd_record_raw(self, delay, interval, count):
        try:
            self.obtain_lock()

            # start recording...
            delay_bytes = self.__unpack_unsigned_int(delay)
            interval_bytes = self.__unpack_unsigned_int(interval)
            count_bytes = self.__unpack_unsigned_int(count)

            param_bytes = []
            param_bytes.extend(delay_bytes)
            param_bytes.extend(interval_bytes)
            param_bytes.extend(count_bytes)

            self._command(0, 'rs', param_bytes)

            # wait...
            time.sleep(2.2)

            # playback...
            response = self._command(count * 8, 'rp')

            values = []

            for i in range(0, count * 8, 8):
                timestamp = self.__pack_unsigned_int(response[i:i + 2])
                pile_ref_voltage = self.__pack_unsigned_int(response[i + 2:i + 4])
                pile_act_voltage = self.__pack_unsigned_int(response[i + 4:i + 6])
                thermistor_voltage = self.__pack_unsigned_int(response[i + 6:i + 8])

                values.append((timestamp, pile_ref_voltage, pile_act_voltage, thermistor_voltage))

            return values

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_fail(self):
        try:
            self.obtain_lock()

            self._command(0, 'mr')          # should return two bytes - ignore these to cause SPI fail

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def _cmd_eeprom_read_unsigned_int(self, index):
        response = self._command(2, 'er', (index, ))
        value = self.__pack_unsigned_int(response)

        return value


    def _cmd_eeprom_write_unsigned_int(self, index, value):
        value_bytes = self.__unpack_unsigned_int(value)
        self._command(0, 'ew', (index, ), value_bytes)

        time.sleep(self.__EEPROM_WRITE_DELAY)


    def _cmd_eeprom_read_float(self, index):
        response = self._command(4, 'er', (index, ))
        value = self.__pack_float(response)

        return value


    def _cmd_eeprom_write_float(self, index, value):
        value_bytes = self.__unpack_float(value)
        self._command(0, 'ew', (index, ), value_bytes)

        time.sleep(self.__EEPROM_WRITE_DELAY)


    # ----------------------------------------------------------------------------------------------------------------

    def _command(self, return_size, cmd, param_group_1=None, param_group_2=None):
        # print("return_size: %d cmd: %s param_group_1:%s param_group_2:%s" %
        #       (return_size, cmd, str(param_group_1), str(param_group_2)), file=sys.stderr)

        try:
            self.__spi.open()

            # transfer...
            self._command_xfer((ord(cmd[0]), ord(cmd[1])))

            if param_group_1:
                self._command_xfer(param_group_1)

            if param_group_2:
                self._command_xfer(param_group_2)

            # wait...
            time.sleep(self.__CMD_DELAY)

            # ACK / NACK...
            response = self.__spi.read_bytes(1)

            if response[0] == 0:
                raise ValueError("None received for command: %s params: %s %s" % (cmd, param_group_1, param_group_2))

            if response[0] == self.__RESPONSE_NACK:
                raise ValueError("NACK received for command: %s params: %s %s" % (cmd, param_group_1, param_group_2))

            # response...
            if return_size < 1:
                return

            response = self.__spi.read_bytes(return_size)
            # print("response: %s" % str(response), file=sys.stderr)

            return response[0] if return_size == 1 else response

        finally:
            self.__spi.close()


    def _command_xfer(self, values):
        request = []                        # convert tuple to array
        request.extend(values)

        self.__spi.xfer(request)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIR:{io:%s, spi:%s}" % (self.__io, self.__spi)
