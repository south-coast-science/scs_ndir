"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

# import sys
import time

from scs_core.data.datum import Datum

from scs_core.gas.ndir import NDIR
from scs_core.gas.ndir_datum import NDIRDatum
from scs_core.gas.ndir_version import NDIRVersion, NDIRTag

from scs_dfe.board.io import IO

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock

from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.spi_ndir_v1.ndir_calib import NDIRCalib, NDIRRangeCalib
from scs_ndir.gas.spi_ndir_v1.spi_ndir_v1_cmd import SPINDIRv1Cmd
from scs_ndir.gas.spi_ndir_v1.ndir_status import NDIRStatus
from scs_ndir.gas.spi_ndir_v1.ndir_uptime import NDIRUptime


# --------------------------------------------------------------------------------------------------------------------

class SPINDIRv1(NDIR):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    SAMPLE_INTERVAL =                   1.0             # seconds between sampling


    # ----------------------------------------------------------------------------------------------------------------

    __LOCK_TIMEOUT =                    4.0             # seconds

    __BOOT_DELAY =                      3.500           # seconds to first sample available
    __PARAM_DELAY =                     0.001           # seconds between SPI sessions

    __RESPONSE_ACK =                    0x01
    __RESPONSE_NACK =                   0x02
    __RESPONSE_BUSY =                   0x03
    __RESPONSE_NONE =                   (0x00, 0xff)

    __SPI_CLOCK =                       488000
    __SPI_MODE =                        1


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__name__, SPINDIRv1.__LOCK_TIMEOUT)


    @classmethod
    def release_lock(cls):
        Lock.release(cls.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, spi_bus, spi_device):
        """
        Constructor
        """
        self.__io = IO()
        self.__spi = SPI(spi_bus, spi_device, SPINDIRv1.__SPI_MODE, SPINDIRv1.__SPI_CLOCK)


    # ----------------------------------------------------------------------------------------------------------------
    # NDIR implementation...

    def power_on(self):
        if not self.__io.ndir_power:           # active low
            return

        self.__io.ndir_power = IO.LOW
        time.sleep(self.__BOOT_DELAY)


    def power_off(self):
        if self.__io.ndir_power:                # active low
            return

        self.__io.ndir_power = IO.HIGH


    def sample(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRv1Cmd.find('sg')
            response = self._transact(cmd)

            cnc = Datum.decode_float(response[0:4])
            cnc_igl = Datum.decode_float(response[4:8])
            temp = Datum.decode_float(response[8:12])

            return NDIRDatum(temp, cnc, cnc_igl)

        finally:
            self.release_lock()


    def version(self):
        try:
            self.obtain_lock()

            # version ident...
            cmd = SPINDIRv1Cmd.find('vi')
            response = self._transact(cmd)
            id = ''.join([chr(byte) for byte in response]).strip()

            # version tag...
            cmd = SPINDIRv1Cmd.find('vt')
            response = self._transact(cmd)
            tag = ''.join([chr(byte) for byte in response]).strip()

            version = NDIRVersion(id, NDIRTag.construct_from_jdict(tag))

            return version

        finally:
            self.release_lock()


    @classmethod
    def sample_interval(cls):
        return cls.SAMPLE_INTERVAL


    # ----------------------------------------------------------------------------------------------------------------
    # status...

    def status(self):
        try:
            self.obtain_lock()

            # restart status...
            cmd = SPINDIRv1Cmd.find('ws')
            response = self._transact(cmd)
            watchdog_reset = bool(response)

            # input voltage...
            cmd = SPINDIRv1Cmd.find('iv')
            response = self._transact(cmd)
            pwr_in = Datum.decode_float(response)

            # uptime...
            cmd = SPINDIRv1Cmd.find('up')
            response = self._transact(cmd)
            seconds = Datum.decode_unsigned_long(response)

            status = NDIRStatus(watchdog_reset, pwr_in, NDIRUptime(seconds))

            return status

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # calib...

    def store_calib(self, calib):
        try:
            self.obtain_lock()

            # identity...
            self._calib_w_unsigned_long(0, NDIRCalib.INDEX_NDIR_SERIAL, calib.ndir_serial)
            self._calib_w_unsigned_long(0, NDIRCalib.INDEX_BOARD_SERIAL, calib.board_serial)

            self._calib_w_unsigned_int(0, NDIRCalib.INDEX_SELECTED_RANGE, calib.selected_range)

            # common fields...
            self._calib_w_float(0, NDIRCalib.INDEX_LAMP_VOLTAGE, calib.lamp_voltage)

            self._calib_w_unsigned_int(0, NDIRCalib.INDEX_LAMP_PERIOD, calib.lamp_period)
            self._calib_w_unsigned_int(0, NDIRCalib.INDEX_MAX_DEFERRAL, calib.max_deferral)
            self._calib_w_unsigned_int(0, NDIRCalib.INDEX_MIN_DEFERRAL, calib.min_deferral)

            # range calibrations...
            self._store_range_calib(NDIRCalib.RANGE_IAQ, calib.range_iaq)
            self._store_range_calib(NDIRCalib.RANGE_SAFETY, calib.range_safety)
            self._store_range_calib(NDIRCalib.RANGE_COMBUSTION, calib.range_combustion)
            self._store_range_calib(NDIRCalib.RANGE_INDUSTRIAL, calib.range_industrial)
            self._store_range_calib(NDIRCalib.RANGE_CUSTOM, calib.range_custom)

        finally:
            self.release_lock()


    def _store_range_calib(self, rng, calib):
        # range check...
        if calib is None:
            self._calib_w_unsigned_int(rng, NDIRRangeCalib.INDEX_RANGE_IS_SET, 0)
            return

        self._calib_w_unsigned_int(rng, NDIRRangeCalib.INDEX_RANGE_IS_SET, 1)

        # range fields...
        self._calib_w_float(rng, NDIRRangeCalib.INDEX_ZERO, calib.zero)
        self._calib_w_float(rng, NDIRRangeCalib.INDEX_SPAN, calib.span)

        self._calib_w_float(rng, NDIRRangeCalib.INDEX_LINEAR_B, calib.linear_b)
        self._calib_w_float(rng, NDIRRangeCalib.INDEX_LINEAR_C, calib.linear_c)

        self._calib_w_float(rng, NDIRRangeCalib.INDEX_ALPHA_LOW, calib.alpha_low)
        self._calib_w_float(rng, NDIRRangeCalib.INDEX_ALPHA_HIGH, calib.alpha_high)

        self._calib_w_float(rng, NDIRRangeCalib.INDEX_BETA_A, calib.beta_a)
        self._calib_w_float(rng, NDIRRangeCalib.INDEX_BETA_O, calib.beta_o)

        self._calib_w_float(rng, NDIRRangeCalib.INDEX_T_CAL, calib.t_cal)


    def retrieve_calib(self):
        try:
            self.obtain_lock()

            # identity...
            ndir_serial = self._calib_r_unsigned_long(0, NDIRCalib.INDEX_NDIR_SERIAL)
            board_serial = self._calib_r_unsigned_long(0, NDIRCalib.INDEX_BOARD_SERIAL)

            selected_range = self._calib_r_unsigned_int(0, NDIRCalib.INDEX_SELECTED_RANGE)

            # common fields...
            lamp_voltage = self._calib_r_float(0, NDIRCalib.INDEX_LAMP_VOLTAGE)

            lamp_period = self._calib_r_unsigned_int(0, NDIRCalib.INDEX_LAMP_PERIOD)
            max_deferral = self._calib_r_unsigned_int(0, NDIRCalib.INDEX_MAX_DEFERRAL)
            min_deferral = self._calib_r_unsigned_int(0, NDIRCalib.INDEX_MIN_DEFERRAL)

            # range calibrations...
            range_iaq = self._retrieve_range_calib(NDIRCalib.RANGE_IAQ)
            range_safety = self._retrieve_range_calib(NDIRCalib.RANGE_SAFETY)
            range_combustion = self._retrieve_range_calib(NDIRCalib.RANGE_COMBUSTION)
            range_industrial = self._retrieve_range_calib(NDIRCalib.RANGE_INDUSTRIAL)
            range_custom = self._retrieve_range_calib(NDIRCalib.RANGE_CUSTOM)

            return NDIRCalib(ndir_serial, board_serial, selected_range,
                             lamp_voltage, lamp_period, max_deferral, min_deferral,
                             range_iaq, range_safety, range_combustion, range_industrial, range_custom)

        finally:
            self.release_lock()


    def _retrieve_range_calib(self, rng):
        # range check...
        if not self._calib_r_unsigned_int(rng, NDIRRangeCalib.INDEX_RANGE_IS_SET):
            return None

        # range fields...
        zero = self._calib_r_float(rng, NDIRRangeCalib.INDEX_ZERO)
        span = self._calib_r_float(rng, NDIRRangeCalib.INDEX_SPAN)

        linear_b = self._calib_r_float(rng, NDIRRangeCalib.INDEX_LINEAR_B)
        linear_c = self._calib_r_float(rng, NDIRRangeCalib.INDEX_LINEAR_C)

        alpha_low = self._calib_r_float(rng, NDIRRangeCalib.INDEX_ALPHA_LOW)
        alpha_high = self._calib_r_float(rng, NDIRRangeCalib.INDEX_ALPHA_HIGH)

        beta_a = self._calib_r_float(rng, NDIRRangeCalib.INDEX_BETA_A)
        beta_o = self._calib_r_float(rng, NDIRRangeCalib.INDEX_BETA_O)

        t_cal = self._calib_r_float(rng, NDIRRangeCalib.INDEX_T_CAL)

        return NDIRRangeCalib(zero, span, linear_b, linear_c, alpha_low, alpha_high, beta_a, beta_o, t_cal)


    def reload_calib(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRv1Cmd.find('cl')
            self._transact(cmd)

            time.sleep(cmd.execution_time)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # lamp...

    def lamp_run(self, on):
        try:
            self.obtain_lock()

            on_byte = 1 if on else 0

            cmd = SPINDIRv1Cmd.find('lr')
            self._transact(cmd, (on_byte,))

        finally:
            self.release_lock()


    def lamp_level(self, voltage):
        try:
            self.obtain_lock()

            voltage_bytes = Datum.encode_float(voltage)

            cmd = SPINDIRv1Cmd.find('ll')
            self._transact(cmd, voltage_bytes)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # low-level commands...

    def cmd_sample_mode(self, single_shot):
        try:
            self.obtain_lock()

            mode_byte = 1 if single_shot else 0

            cmd = SPINDIRv1Cmd.find('sm')
            self._transact(cmd, (mode_byte, ))

            time.sleep(cmd.execution_time)

        finally:
            self.release_lock()


    def cmd_sample_raw(self):
        try:
            self.obtain_lock()

            # report...
            cmd = SPINDIRv1Cmd.find('sr')
            response = self._transact(cmd)

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
            cmd = SPINDIRv1Cmd.find('sv')
            response = self._transact(cmd)

            pile_ref_amplitude = Datum.decode_float(response[0:4])
            pile_act_amplitude = Datum.decode_float(response[4:8])
            thermistor_average = Datum.decode_float(response[8:12])

            return pile_ref_amplitude, pile_act_amplitude, thermistor_average

        finally:
            self.release_lock()


    def cmd_sample_offsets(self):
        try:
            self.obtain_lock()

            # report...
            cmd = SPINDIRv1Cmd.find('so')
            response = self._transact(cmd)

            min_ref_offset = Datum.decode_unsigned_int(response[0:2])
            min_act_offset = Datum.decode_unsigned_int(response[2:4])
            max_ref_offset = Datum.decode_unsigned_int(response[4:6])
            max_act_offset = Datum.decode_unsigned_int(response[6:8])

            return min_ref_offset, min_act_offset, max_ref_offset, max_act_offset

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_measure_calibrate(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRv1Cmd.find('mc')
            self._transact(cmd)

            time.sleep(cmd.execution_time)

        finally:
            self.release_lock()


    def cmd_measure_raw(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRv1Cmd.find('mr')
            response = self._transact(cmd)

            pile_ref_value = Datum.decode_unsigned_int(response[0:2])
            pile_act_value = Datum.decode_unsigned_int(response[2:4])
            thermistor_value = Datum.decode_unsigned_int(response[4:6])

            return pile_ref_value, pile_act_value, thermistor_value

        finally:
            self.release_lock()


    def cmd_measure(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRv1Cmd.find('mv')
            response = self._transact(cmd)

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

            cmd = SPINDIRv1Cmd.find('rs')
            self._transact(cmd, param_bytes)

            # wait...
            execution_time = cmd.execution_time + (((interval * count) + deferral) / 1000)
            # print("execution time: %s" % execution_time, file=sys.stderr)

            time.sleep(execution_time)

            # playback...
            cmd = SPINDIRv1Cmd.find('rp')
            cmd.return_count = count * 6

            response = self._transact(cmd)

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

            cmd = SPINDIRv1Cmd.find('ir')
            response = self._transact(cmd)
            v_in_value = Datum.decode_unsigned_int(response)

            return v_in_value

        finally:
            self.release_lock()


    def cmd_input(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRv1Cmd.find('iv')
            response = self._transact(cmd)
            v_in_voltage = Datum.decode_float(response)

            return v_in_voltage

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd_watchdog_clear(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRv1Cmd.find('wc')
            self._transact(cmd)

        finally:
            self.release_lock()


    def cmd_reset(self):
        try:
            self.obtain_lock()

            # force reset...
            cmd = SPINDIRv1Cmd.find('wr')
            self._transact(cmd)

            time.sleep(cmd.execution_time)

            # clear status...
            cmd = SPINDIRv1Cmd.find('wc')
            self._transact(cmd)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # arbitrary command, used for tests purposes...

    def cmd(self, name, response_time, execution_time, return_count):
        command = SPINDIRv1Cmd(name, response_time, execution_time, return_count)

        try:
            self.obtain_lock()

            self._transact(command)
            time.sleep(execution_time)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # low-level calib functions...

    def _calib_r_unsigned_int(self, block, index):
        cmd = SPINDIRv1Cmd.find('cr')
        cmd.return_count = 2

        response = self._transact(cmd, (block, index))
        value = Datum.decode_unsigned_int(response)

        return value


    def _calib_w_unsigned_int(self, block, index, value):
        cmd = SPINDIRv1Cmd.find('cw')

        value_bytes = Datum.encode_unsigned_int(value)
        self._transact(cmd, (block, index), value_bytes)

        time.sleep(cmd.execution_time)


    def _calib_r_unsigned_long(self, block, index):
        cmd = SPINDIRv1Cmd.find('cr')
        cmd.return_count = 4

        response = self._transact(cmd, (block, index))
        value = Datum.decode_unsigned_long(response)

        return value


    def _calib_w_unsigned_long(self, block, index, value):
        cmd = SPINDIRv1Cmd.find('cw')

        value_bytes = Datum.encode_unsigned_long(value)
        self._transact(cmd, (block, index), value_bytes)

        time.sleep(cmd.execution_time)


    def _calib_r_float(self, block, index):
        cmd = SPINDIRv1Cmd.find('cr')
        cmd.return_count = 4

        response = self._transact(cmd, (block, index))
        value = Datum.decode_float(response)

        return value


    def _calib_w_float(self, block, index, value):
        cmd = SPINDIRv1Cmd.find('cw')

        value_bytes = Datum.encode_float(value)
        self._transact(cmd, (block, index), value_bytes)

        time.sleep(cmd.execution_time)


    # ----------------------------------------------------------------------------------------------------------------
    # SPI interactions...

    def _transact(self, cmd, param_group_1=None, param_group_2=None):
        # print("cmd: %s param_group_1:%s param_group_2:%s" %
        #       (cmd, str(param_group_1), str(param_group_2)), file=sys.stderr)

        try:
            self.__spi.open()

            # command...
            self.__xfer(cmd.name_bytes())

            if param_group_1:
                time.sleep(self.__PARAM_DELAY)
                self.__xfer(param_group_1)

            if param_group_2:
                time.sleep(self.__PARAM_DELAY)
                self.__xfer(param_group_2)

            # wait...
            time.sleep(cmd.response_time)

            # ACK / NACK...
            response = self.__spi.read_bytes(1)
            # print("response 1: %s" % str(response), file=sys.stderr)

            if response[0] in self.__RESPONSE_NONE:
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
            # print("response 2: %s" % str(response), file=sys.stderr)

            return response[0] if cmd.return_count == 1 else response

        finally:
            self.__spi.close()


    def __xfer(self, values):
        request = []                        # convert tuple to array
        request.extend(values)

        self.__spi.xfer(request)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SPINDIRv1:{io:%s, spi:%s}" % (self.__io, self.__spi)
