"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

# import sys
import time

from scs_core.data.datum import Datum

from scs_core.gas.ndir_datum import NDIRDatum
from scs_core.gas.ndir_version import NDIRVersion, NDIRTag

from scs_dfe.board.io import IO

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock

from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir_calib import NDIRCalib
from scs_ndir.gas.ndir_cmd import NDIRCmd
from scs_ndir.gas.ndir_status import NDIRStatus
from scs_ndir.gas.ndir_uptime import NDIRUptime


# --------------------------------------------------------------------------------------------------------------------

class NDIR(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    SAMPLE_INTERVAL =                   1.0             # seconds between sampling
    RECOVERY_TIME =                     1.0             # seconds between bad SPI interaction and MCU recovery
    RESET_QUARANTINE =                  8.0             # seconds between reset and stable readings


    # ----------------------------------------------------------------------------------------------------------------

    __LOCK_TIMEOUT =                    4.0             # seconds

    __BOOT_DELAY =                      2.500           # seconds to first sample available
    __PARAM_DELAY =                     0.001           # seconds between SPI sessions

    __RESPONSE_ACK =                    0x01
    __RESPONSE_NACK =                   0x02
    __RESPONSE_BUSY =                   0x03

    __SPI_CLOCK =                       488000
    __SPI_MODE =                        1


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

    def sample(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('sg')
            response = self._execute(cmd)

            cnc = Datum.decode_float(response[0:4])
            cnc_igl = Datum.decode_float(response[4:8])
            temp = Datum.decode_float(response[8:12])

            return NDIRDatum(temp, cnc, cnc_igl)

        finally:
            self.release_lock()


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
            pwr_in = Datum.decode_float(response)

            # uptime...
            cmd = NDIRCmd.find('up')
            response = self._execute(cmd)
            seconds = Datum.decode_unsigned_long(response)

            status = NDIRStatus(watchdog_reset, pwr_in, NDIRUptime(seconds))

            return status

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def store_eeprom_calib(self, calib):
        try:
            self.obtain_lock()

            # identity...
            self.eeprom_write_unsigned_long(NDIRCalib.INDEX_NDIR_SERIAL, calib.ndir_serial)
            self.eeprom_write_unsigned_long(NDIRCalib.INDEX_BOARD_SERIAL, calib.board_serial)

            # common fields...
            self.eeprom_write_unsigned_int(NDIRCalib.INDEX_SENSOR, calib.sensor)

            self.eeprom_write_unsigned_int(NDIRCalib.INDEX_LAMP_VOLTAGE, calib.lamp_voltage)

            self.eeprom_write_unsigned_int(NDIRCalib.INDEX_LAMP_PERIOD, calib.lamp_period)
            self.eeprom_write_unsigned_int(NDIRCalib.INDEX_MAX_DEFERRAL, calib.max_deferral)
            self.eeprom_write_unsigned_int(NDIRCalib.INDEX_MIN_DEFERRAL, calib.min_deferral)

            # range fields...
            self.eeprom_write_float(NDIRCalib.INDEX_ZERO, calib.zero)
            self.eeprom_write_float(NDIRCalib.INDEX_SPAN, calib.span)

            self.eeprom_write_float(NDIRCalib.INDEX_LINEAR_B, calib.linear_b)
            self.eeprom_write_float(NDIRCalib.INDEX_LINEAR_C, calib.linear_c)

            self.eeprom_write_float(NDIRCalib.INDEX_TEMP_BETA_O, calib.temp_beta_o)
            self.eeprom_write_float(NDIRCalib.INDEX_TEMP_ALPHA, calib.temp_alpha)
            self.eeprom_write_float(NDIRCalib.INDEX_TEMP_BETA_A, calib.temp_beta_a)

            self.eeprom_write_float(NDIRCalib.INDEX_T_CAL, calib.t_cal)

        finally:
            self.release_lock()


    def retrieve_eeprom_calib(self):
        try:
            self.obtain_lock()

            # identity...
            ndir_serial = self.eeprom_read_unsigned_long(NDIRCalib.INDEX_NDIR_SERIAL)
            board_serial = self.eeprom_read_unsigned_long(NDIRCalib.INDEX_BOARD_SERIAL)

            # common fields...
            sensor = self.eeprom_read_unsigned_int(NDIRCalib.INDEX_SENSOR)

            lamp_voltage = self.eeprom_read_unsigned_int(NDIRCalib.INDEX_LAMP_VOLTAGE)

            lamp_period = self.eeprom_read_unsigned_int(NDIRCalib.INDEX_LAMP_PERIOD)
            max_deferral = self.eeprom_read_unsigned_int(NDIRCalib.INDEX_MAX_DEFERRAL)
            min_deferral = self.eeprom_read_unsigned_int(NDIRCalib.INDEX_MIN_DEFERRAL)

            # range fields...
            zero = self.eeprom_read_float(NDIRCalib.INDEX_ZERO)
            span = self.eeprom_read_float(NDIRCalib.INDEX_SPAN)

            linear_b = self.eeprom_read_float(NDIRCalib.INDEX_LINEAR_B)
            linear_c = self.eeprom_read_float(NDIRCalib.INDEX_LINEAR_C)

            temp_beta_o = self.eeprom_read_float(NDIRCalib.INDEX_TEMP_BETA_O)
            temp_alpha = self.eeprom_read_float(NDIRCalib.INDEX_TEMP_ALPHA)
            temp_beta_a = self.eeprom_read_float(NDIRCalib.INDEX_TEMP_BETA_A)

            t_cal = self.eeprom_read_float(NDIRCalib.INDEX_T_CAL)

            return NDIRCalib(ndir_serial, board_serial, sensor, lamp_voltage, lamp_period, max_deferral, min_deferral,
                             zero, span, linear_b, linear_c, temp_beta_o, temp_alpha, temp_beta_a, t_cal)

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

            pile_ref_amplitude = Datum.decode_unsigned_int(response[0:2])
            pile_act_amplitude = Datum.decode_unsigned_int(response[2:4])
            thermistor_average = Datum.decode_unsigned_int(response[4:6])

            return pile_ref_amplitude, pile_act_amplitude, thermistor_average

        finally:
            self.release_lock()


    def cmd_sample_voltage(self):
        try:
            self.obtain_lock()

            # report...
            cmd = NDIRCmd.find('sv')
            response = self._execute(cmd)

            pile_ref_amplitude = Datum.decode_float(response[0:4])
            pile_act_amplitude = Datum.decode_float(response[4:8])
            thermistor_average = Datum.decode_float(response[8:12])

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
                pile_ref = Datum.decode_unsigned_int(response[i:i + 2])
                pile_act = Datum.decode_unsigned_int(response[i + 2:i + 4])
                thermistor = Datum.decode_unsigned_int(response[i + 4:i + 6])

                values.append((pile_ref, pile_act, thermistor))

            return values

        finally:
            self.release_lock()


    def cmd_sample_dump(self):
        try:
            self.obtain_lock()

            # report...
            cmd = NDIRCmd.find('sd')
            response = self._execute(cmd)

            single_shot = response[0]
            is_running = response[1]
            index = Datum.decode_unsigned_int(response[2:4])

            return single_shot, is_running, index

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

            pile_ref_value = Datum.decode_unsigned_int(response[0:2])
            pile_act_value = Datum.decode_unsigned_int(response[2:4])
            thermistor_value = Datum.decode_unsigned_int(response[4:6])

            return pile_ref_value, pile_act_value, thermistor_value

        finally:
            self.release_lock()


    def cmd_measure(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('mv')
            response = self._execute(cmd)

            pile_ref_voltage = Datum.decode_float(response[0:4])
            pile_act_voltage = Datum.decode_float(response[4:8])
            thermistor_voltage = Datum.decode_float(response[8:12])

            return pile_ref_voltage, pile_act_voltage, thermistor_voltage

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_record_raw(self, deferral, interval, count):
        try:
            self.obtain_lock()

            # start recording...
            deferral_bytes = Datum.encode_unsigned_int(deferral)
            interval_bytes = Datum.encode_unsigned_int(interval)
            count_bytes = Datum.encode_unsigned_int(count)

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
                timestamp = Datum.decode_unsigned_int(response[i:i + 2])
                pile_ref = Datum.decode_unsigned_int(response[i + 2:i + 4])
                pile_act = Datum.decode_unsigned_int(response[i + 4:i + 6])

                values.append((timestamp, pile_ref, pile_act))

            return values

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_input_raw(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('ir')
            response = self._execute(cmd)
            v_in_value = Datum.decode_unsigned_int(response)

            return v_in_value

        finally:
            self.release_lock()


    def cmd_input(self):
        try:
            self.obtain_lock()

            cmd = NDIRCmd.find('iv')
            response = self._execute(cmd)
            v_in_voltage = Datum.decode_float(response)

            return v_in_voltage

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

    def cmd_fail(self):
        try:
            self.obtain_lock()

            # TODO: datum for insufficient bytes sent

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
        value = Datum.decode_unsigned_int(response)

        return value


    def eeprom_write_unsigned_int(self, index, value):
        cmd = NDIRCmd.find('ew')

        value_bytes = Datum.encode_unsigned_int(value)
        self._execute(cmd, (index,), value_bytes)

        time.sleep(cmd.execution_time)


    def eeprom_read_unsigned_long(self, index):
        cmd = NDIRCmd.find('er')
        cmd.return_count = 4

        response = self._execute(cmd, (index,))
        value = Datum.decode_unsigned_long(response)

        return value


    def eeprom_write_unsigned_long(self, index, value):
        cmd = NDIRCmd.find('ew')

        value_bytes = Datum.encode_unsigned_long(value)
        self._execute(cmd, (index,), value_bytes)

        time.sleep(cmd.execution_time)


    def eeprom_read_float(self, index):
        cmd = NDIRCmd.find('er')
        cmd.return_count = 4

        response = self._execute(cmd, (index,))
        value = Datum.decode_float(response)

        return value


    def eeprom_write_float(self, index, value):
        cmd = NDIRCmd.find('ew')

        value_bytes = Datum.encode_float(value)
        self._execute(cmd, (index,), value_bytes)

        time.sleep(cmd.execution_time)


    # ----------------------------------------------------------------------------------------------------------------

    def _execute(self, cmd, param_group_1=None, param_group_2=None):
        # print("cmd: %s param_group_1:%s param_group_2:%s" %
        #       (cmd, str(param_group_1), str(param_group_2)), file=sys.stderr)

        try:
            self.__spi.open()

            # command...
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

            # return values...
            if cmd.return_count < 1:
                return

            # wait...
            time.sleep(self.__PARAM_DELAY)

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
