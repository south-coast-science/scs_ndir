"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import math
import struct
# import sys
import time

from scs_core.gas.co2_datum import CO2Datum
from scs_core.gas.ndir_datum import NDIRDatum
from scs_core.gas.ndir_version import NDIRVersion, NDIRTag

from scs_dfe.board.io import IO

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock

from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir_cmd import NDIRCmd
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

    __LOCK_TIMEOUT =                    4.0             # seconds

    __BOOT_DELAY =                      0.500           # seconds
    __PARAM_DELAY =                     0.001           # seconds

    __RESPONSE_ACK =                    0x01
    __RESPONSE_NACK =                   0x02
    __RESPONSE_BUSY =                   0x03

    __SPI_CLOCK =                       488000
    __SPI_MODE =                        1


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
    # identity...

    def version(self):
        try:
            self.obtain_lock()

            # version ident...
            cmd = NDIRCmd.find('vi')
            response = self._execute(cmd)
            id = ''.join([chr(byte) for byte in response]).strip()

            # version tag...
            cmd = NDIRCmd.find('vt')
            response = self._execute(cmd)
            tag = ''.join([chr(byte) for byte in response]).strip()

            version = NDIRVersion(id, NDIRTag.construct_from_jdict(tag))

            return version

        finally:
            self.release_lock()


    def status(self):
        try:
            self.obtain_lock()

            # restart status...
            cmd = NDIRCmd.find('ws')
            response = self._execute(cmd)
            watchdog_reset = bool(response)

            # input voltage...
            cmd = NDIRCmd.find('iv')
            response = self._execute(cmd)
            pwr_in = self.__pack_float(response)

            # uptime...
            cmd = NDIRCmd.find('up')
            response = self._execute(cmd)
            seconds = self.__pack_unsigned_long(response)

            status = NDIRStatus(watchdog_reset, pwr_in, NDIRUptime(seconds))

            return status

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_watchdog_clear(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('wc')
            self._execute(cmd)

        finally:
            self.release_lock()


    def cmd_reset(self):
        try:
            self.obtain_lock()

            # force reset...
            cmd = NDIRCmd.find('wr')
            self._execute(cmd)

            time.sleep(cmd.execution_time)

            # clear status...
            cmd = NDIRCmd.find('wc')
            self._execute(cmd)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_store_eeprom_calib(self, calib):
        try:
            self.obtain_lock()

            # common fields...
            self.eeprom_write_float(NDIRCalib.INDEX_LAMP_VOLTAGE, calib.lamp_voltage)
            self.eeprom_write_unsigned_int(NDIRCalib.INDEX_LAMP_PERIOD, calib.lamp_period)

            self.eeprom_write_unsigned_int(NDIRCalib.INDEX_MAX_DEFERRAL, calib.max_deferral)
            self.eeprom_write_unsigned_int(NDIRCalib.INDEX_MIN_DEFERRAL, calib.min_deferral)

            self.eeprom_write_unsigned_int(NDIRCalib.INDEX_SPAN, calib.span)

            # span fields...
            self.eeprom_write_float(NDIRCalib.INDEX_LINEAR_B, calib.linear_b)
            self.eeprom_write_float(NDIRCalib.INDEX_LINEAR_C, calib.linear_c)

            self.eeprom_write_float(NDIRCalib.INDEX_TEMP_BETA_O, calib.temp_beta_o)
            self.eeprom_write_float(NDIRCalib.INDEX_TEMP_ALPHA, calib.temp_alpha)
            self.eeprom_write_float(NDIRCalib.INDEX_TEMP_BETA_A, calib.temp_beta_a)

            self.eeprom_write_float(NDIRCalib.INDEX_THERM_A, calib.therm_a)
            self.eeprom_write_float(NDIRCalib.INDEX_THERM_B, calib.therm_b)
            self.eeprom_write_float(NDIRCalib.INDEX_THERM_C, calib.therm_c)
            self.eeprom_write_float(NDIRCalib.INDEX_THERM_D, calib.therm_d)

            self.eeprom_write_float(NDIRCalib.INDEX_T_CAL, calib.t_cal)

        finally:
            self.release_lock()


    def cmd_retrieve_eeprom_calib(self):
        try:
            self.obtain_lock()

            # common fields...
            lamp_voltage = self.eeprom_read_float(NDIRCalib.INDEX_LAMP_VOLTAGE)
            lamp_period = self.eeprom_read_unsigned_int(NDIRCalib.INDEX_LAMP_PERIOD)

            max_deferral = self.eeprom_read_unsigned_int(NDIRCalib.INDEX_MAX_DEFERRAL)
            min_deferral = self.eeprom_read_unsigned_int(NDIRCalib.INDEX_MIN_DEFERRAL)

            span = self.eeprom_read_unsigned_int(NDIRCalib.INDEX_SPAN)

            # span fields...
            linear_b = self.eeprom_read_float(NDIRCalib.INDEX_LINEAR_B)
            linear_c = self.eeprom_read_float(NDIRCalib.INDEX_LINEAR_C)

            temp_beta_o = self.eeprom_read_float(NDIRCalib.INDEX_TEMP_BETA_O)
            temp_alpha = self.eeprom_read_float(NDIRCalib.INDEX_TEMP_ALPHA)
            temp_beta_a = self.eeprom_read_float(NDIRCalib.INDEX_TEMP_BETA_A)

            therm_a = self.eeprom_read_float(NDIRCalib.INDEX_THERM_A)
            therm_b = self.eeprom_read_float(NDIRCalib.INDEX_THERM_B)
            therm_c = self.eeprom_read_float(NDIRCalib.INDEX_THERM_C)
            therm_d = self.eeprom_read_float(NDIRCalib.INDEX_THERM_D)

            t_cal = self.eeprom_read_float(NDIRCalib.INDEX_T_CAL)

            return NDIRCalib(lamp_voltage, lamp_period, max_deferral, min_deferral, span, linear_b, linear_c,
                             temp_beta_o, temp_alpha, temp_beta_a, therm_a, therm_b, therm_c, therm_d, t_cal)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_lamp_run(self, on):
        try:
            self.obtain_lock()

            on_byte = 1 if on else 0

            cmd = NDIRCmd.find('lr')
            self._execute(cmd, (on_byte,))

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_input_raw(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('ir')
            response = self._execute(cmd)
            v_in_value = self.__pack_int(response)

            return v_in_value

        finally:
            self.release_lock()


    def cmd_input(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('iv')
            response = self._execute(cmd)
            v_in_voltage = self.__pack_float(response)

            return v_in_voltage

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_measure_calibrate(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('mc')
            self._execute(cmd)

            time.sleep(cmd.execution_time)

        finally:
            self.release_lock()


    def cmd_measure_raw(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('mr')
            response = self._execute(cmd)

            pile_ref_value = self.__pack_unsigned_int(response[0:2])
            pile_act_value = self.__pack_unsigned_int(response[2:4])
            thermistor_value = self.__pack_unsigned_int(response[4:6])

            return pile_ref_value, pile_act_value, thermistor_value

        finally:
            self.release_lock()


    def cmd_measure(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('mv')
            response = self._execute(cmd)

            pile_ref_voltage = self.__pack_float(response[0:4])
            pile_act_voltage = self.__pack_float(response[4:8])
            thermistor_voltage = self.__pack_float(response[8:12])

            return pile_ref_voltage, pile_act_voltage, thermistor_voltage

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_record_raw(self, deferral, interval, count):
        try:
            self.obtain_lock()

            # start recording...
            deferral_bytes = self.__unpack_unsigned_int(deferral)
            interval_bytes = self.__unpack_unsigned_int(interval)
            count_bytes = self.__unpack_unsigned_int(count)

            param_bytes = []
            param_bytes.extend(deferral_bytes)
            param_bytes.extend(interval_bytes)
            param_bytes.extend(count_bytes)

            cmd = NDIRCmd.find('rs')
            self._execute(cmd, param_bytes)

            # wait...
            time.sleep(cmd.execution_time + (deferral / 1000))

            # playback...
            cmd = NDIRCmd.find('rp')
            cmd.return_count = count * 6

            response = self._execute(cmd)

            values = []

            for i in range(0, cmd.return_count, 6):
                timestamp = self.__pack_unsigned_int(response[i:i + 2])
                pile_ref = self.__pack_unsigned_int(response[i + 2:i + 4])
                pile_act = self.__pack_unsigned_int(response[i + 4:i + 6])

                values.append((timestamp, pile_ref, pile_act))

            return values

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_sample_mode(self, single_shot):
        try:
            self.obtain_lock()

            mode_byte = 1 if single_shot else 0

            cmd = NDIRCmd.find('sm')
            self._execute(cmd, (mode_byte, ))

            time.sleep(cmd.execution_time)

        finally:
            self.release_lock()


    def cmd_sample_raw(self):
        try:
            self.obtain_lock()

            # report...
            cmd = NDIRCmd.find('sr')
            response = self._execute(cmd)

            pile_ref_amplitude = self.__pack_unsigned_int(response[0:2])
            pile_act_amplitude = self.__pack_unsigned_int(response[2:4])
            thermistor_average = self.__pack_unsigned_int(response[4:6])

            return pile_ref_amplitude, pile_act_amplitude, thermistor_average

        finally:
            self.release_lock()


    def cmd_sample(self):
        try:
            self.obtain_lock()

            # report...
            cmd = NDIRCmd.find('sv')
            response = self._execute(cmd)

            pile_ref_amplitude = self.__pack_float(response[0:4])
            pile_act_amplitude = self.__pack_float(response[4:8])
            thermistor_average = self.__pack_float(response[8:12])

            return pile_ref_amplitude, pile_act_amplitude, thermistor_average

        finally:
            self.release_lock()


    def cmd_sample_window(self):
        try:
            self.obtain_lock()

            # playback...
            cmd = NDIRCmd.find('sw')
            response = self._execute(cmd)

            values = []

            for i in range(0, cmd.return_count, 6):
                pile_ref = self.__pack_unsigned_int(response[i:i + 2])
                pile_act = self.__pack_unsigned_int(response[i + 2:i + 4])
                thermistor = self.__pack_unsigned_int(response[i + 4:i + 6])

                values.append((pile_ref, pile_act, thermistor))

            return values

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_fail(self):
        try:
            self.obtain_lock()

            # TODO: test for insufficient bytes sent

            cmd = NDIRCmd.find('mr')
            cmd.return_count = 0            # should return two bytes - ignore these to cause SPI fail

            self._execute(cmd)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def eeprom_read_unsigned_int(self, index):
        cmd = NDIRCmd.find('er')
        cmd.return_count = 2

        response = self._execute(cmd, (index,))
        value = self.__pack_unsigned_int(response)

        return value


    def eeprom_write_unsigned_int(self, index, value):
        cmd = NDIRCmd.find('ew')

        value_bytes = self.__unpack_unsigned_int(value)
        self._execute(cmd, (index,), value_bytes)

        time.sleep(cmd.execution_time)


    def eeprom_read_float(self, index):
        cmd = NDIRCmd.find('er')
        cmd.return_count = 4

        response = self._execute(cmd, (index,))
        value = self.__pack_float(response)

        return value


    def eeprom_write_float(self, index, value):
        cmd = NDIRCmd.find('ew')

        value_bytes = self.__unpack_float(value)
        self._execute(cmd, (index,), value_bytes)

        time.sleep(cmd.execution_time)


    # ----------------------------------------------------------------------------------------------------------------

    def _execute(self, cmd, param_group_1=None, param_group_2=None):
        # print("cmd: %s param_group_1:%s param_group_2:%s" %
        #       (cmd, str(param_group_1), str(param_group_2)), file=sys.stderr)

        try:
            self.__spi.open()

            # transfer...
            self._xfer(cmd.name_bytes())

            if param_group_1:
                time.sleep(self.__PARAM_DELAY)
                self._xfer(param_group_1)

            if param_group_2:
                time.sleep(self.__PARAM_DELAY)
                self._xfer(param_group_2)

            # wait...
            time.sleep(cmd.response_time)

            # ACK / NACK...
            response = self.__spi.read_bytes(1)

            if response[0] == 0:
                raise NDIRException('None received', response[0], cmd, (param_group_1, param_group_2))

            if response[0] == self.__RESPONSE_NACK:
                raise NDIRException('NACK received', response[0], cmd, (param_group_1, param_group_2))

            if response[0] == self.__RESPONSE_BUSY:
                raise NDIRException('BUSY received', response[0], cmd, (param_group_1, param_group_2))

            # response...
            if cmd.return_count < 1:
                return

            response = self.__spi.read_bytes(cmd.return_count)
            # print("response: %s" % str(response), file=sys.stderr)

            return response[0] if cmd.return_count == 1 else response

        finally:
            self.__spi.close()


    def _xfer(self, values):
        request = []                        # convert tuple to array
        request.extend(values)

        self.__spi.xfer(request)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIR:{io:%s, spi:%s}" % (self.__io, self.__spi)
