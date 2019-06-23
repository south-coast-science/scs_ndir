"""
Created on 11 Dec 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

# import sys
import time

from scs_core.data.datum import Decode, Encode

from scs_core.gas.ndir import NDIR
from scs_core.gas.ndir_datum import NDIRDatum
from scs_core.gas.ndir_version import NDIRVersion, NDIRTag

from scs_dfe.interface.components.io import IO

from scs_host.bus.spi import SPI
from scs_host.lock.lock import Lock

from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.spi_ndir_x1.ndir_calib import NDIRCalib, NDIRRangeCalib
from scs_ndir.gas.spi_ndir_x1.spi_ndir_x1_cmd import SPINDIRx1Cmd
from scs_ndir.gas.spi_ndir_x1.ndir_status import NDIRStatus
from scs_ndir.gas.spi_ndir_x1.ndir_uptime import NDIRUptime


# --------------------------------------------------------------------------------------------------------------------

class SPINDIRx1(NDIR):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    SAMPLE_INTERVAL =                   1.0             # seconds between on-board sampling


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
        Lock.acquire(cls.__name__, SPINDIRx1.__LOCK_TIMEOUT)


    @classmethod
    def release_lock(cls):
        Lock.release(cls.__name__)


    @classmethod
    def get_sample_interval(cls):
        return cls.SAMPLE_INTERVAL


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, load_switch_active_high, spi_bus, spi_device):
        """
        Constructor
        """
        self.__io = IO(load_switch_active_high)
        self.__spi = SPI(spi_bus, spi_device, SPINDIRx1.__SPI_MODE, SPINDIRx1.__SPI_CLOCK)


    # ----------------------------------------------------------------------------------------------------------------
    # NDIR implementation...

    def power_on(self):
        if self.__io.ndir_power:
            return

        self.__io.ndir_power = True
        time.sleep(self.__BOOT_DELAY)


    def power_off(self):
        if not self.__io.ndir_power:
            return

        self.__io.ndir_power = False


    def sample(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRx1Cmd.find('sg')
            response = self._transact(cmd)

            cnc = Decode.float(response[0:4], '<')
            cnc_igl = Decode.float(response[4:8], '<')
            temp = Decode.float(response[8:12], '<')

            return NDIRDatum(temp, cnc, cnc_igl)

        finally:
            self.release_lock()


    def version(self):
        try:
            self.obtain_lock()

            # version ident...
            cmd = SPINDIRx1Cmd.find('vi')
            response = self._transact(cmd)
            id = ''.join([chr(byte) for byte in response]).strip()

            # version tag...
            cmd = SPINDIRx1Cmd.find('vt')
            response = self._transact(cmd)
            tag = ''.join([chr(byte) for byte in response]).strip()

            version = NDIRVersion(id, NDIRTag.construct_from_jdict(tag))

            return version

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # barometric pressure...

    def pressure(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRx1Cmd.find('sp')
            response = self._transact(cmd)

            p_a = Decode.float(response[0:4], '<')

            return round(p_a, 1)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # status...

    def status(self):
        try:
            self.obtain_lock()

            # restart status...
            cmd = SPINDIRx1Cmd.find('ws')
            response = self._transact(cmd)
            watchdog_reset = bool(response)

            # input voltage...
            cmd = SPINDIRx1Cmd.find('iv')
            response = self._transact(cmd)
            pwr_in = Decode.float(response, '<')

            # uptime...
            cmd = SPINDIRx1Cmd.find('up')
            response = self._transact(cmd)
            seconds = Decode.unsigned_long(response, '<')

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
            self._calib_w_unsigned_int(0, NDIRCalib.INDEX_SAMPLE_START, calib.sample_start)
            self._calib_w_unsigned_int(0, NDIRCalib.INDEX_SAMPLE_END, calib.sample_end)

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
            sample_start = self._calib_r_unsigned_int(0, NDIRCalib.INDEX_SAMPLE_START)
            sample_end = self._calib_r_unsigned_int(0, NDIRCalib.INDEX_SAMPLE_END)

            # range calibrations...
            range_iaq = self._retrieve_range_calib(NDIRCalib.RANGE_IAQ)
            range_safety = self._retrieve_range_calib(NDIRCalib.RANGE_SAFETY)
            range_combustion = self._retrieve_range_calib(NDIRCalib.RANGE_COMBUSTION)
            range_industrial = self._retrieve_range_calib(NDIRCalib.RANGE_INDUSTRIAL)
            range_custom = self._retrieve_range_calib(NDIRCalib.RANGE_CUSTOM)

            return NDIRCalib(ndir_serial, board_serial, selected_range,
                             lamp_voltage, lamp_period, sample_start, sample_end,
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

            cmd = SPINDIRx1Cmd.find('cl')
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

            cmd = SPINDIRx1Cmd.find('lr')
            self._transact(cmd, (on_byte,))

        finally:
            self.release_lock()


    def lamp_level(self, voltage):
        try:
            self.obtain_lock()

            voltage_bytes = Encode.float(voltage, '<')

            cmd = SPINDIRx1Cmd.find('ll')
            self._transact(cmd, voltage_bytes)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # low-level commands...

    def get_sample_mode(self, single_shot):
        try:
            self.obtain_lock()

            mode_byte = 1 if single_shot else 0

            cmd = SPINDIRx1Cmd.find('sm')
            self._transact(cmd, (mode_byte, ))

            time.sleep(cmd.execution_time)

        finally:
            self.release_lock()


    def get_sample_raw(self):
        try:
            self.obtain_lock()

            # report...
            cmd = SPINDIRx1Cmd.find('sr')
            response = self._transact(cmd)

            pile_ref_amplitude = Decode.unsigned_int(response[0:2], '<')
            pile_act_amplitude = Decode.unsigned_int(response[2:4], '<')
            thermistor_average = Decode.unsigned_int(response[4:6], '<')

            return pile_ref_amplitude, pile_act_amplitude, thermistor_average

        finally:
            self.release_lock()


    def get_sample_voltage(self):
        try:
            self.obtain_lock()

            # report...
            cmd = SPINDIRx1Cmd.find('sv')
            response = self._transact(cmd)

            pile_ref_amplitude = Decode.float(response[0:4], '<')
            pile_act_amplitude = Decode.float(response[4:8], '<')
            thermistor_average = Decode.float(response[8:12], '<')

            # print("pile_ref_amplitude: %s pile_act_amplitude: %s thermistor_average: %s" % \
            #       (pile_ref_amplitude, pile_act_amplitude, thermistor_average))

            return pile_ref_amplitude, pile_act_amplitude, thermistor_average

        finally:
            self.release_lock()


    def get_sample_offsets(self):
        try:
            self.obtain_lock()

            # report...
            cmd = SPINDIRx1Cmd.find('so')
            response = self._transact(cmd)

            min_ref_offset = Decode.unsigned_int(response[0:2], '<')
            min_act_offset = Decode.unsigned_int(response[2:4], '<')
            max_ref_offset = Decode.unsigned_int(response[4:6], '<')
            max_act_offset = Decode.unsigned_int(response[6:8], '<')

            return min_ref_offset, min_act_offset, max_ref_offset, max_act_offset

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def measure_calibrate(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRx1Cmd.find('mc')
            self._transact(cmd)

            time.sleep(cmd.execution_time)

        finally:
            self.release_lock()


    def measure_raw(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRx1Cmd.find('mr')
            response = self._transact(cmd)

            pile_ref_value = Decode.unsigned_int(response[0:2], '<')
            pile_act_value = Decode.unsigned_int(response[2:4], '<')
            thermistor_value = Decode.unsigned_int(response[4:6], '<')

            return pile_ref_value, pile_act_value, thermistor_value

        finally:
            self.release_lock()


    def measure_voltage(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRx1Cmd.find('mv')
            response = self._transact(cmd)

            pile_ref_voltage = Decode.float(response[0:4], '<')
            pile_act_voltage = Decode.float(response[4:8], '<')
            thermistor_voltage = Decode.float(response[8:12], '<')

            return pile_ref_voltage, pile_act_voltage, thermistor_voltage

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def record_raw(self, deferral, interval, count):
        try:
            self.obtain_lock()

            # start recording...
            deferral_bytes = Encode.unsigned_int(deferral, '<')
            interval_bytes = Encode.unsigned_int(interval, '<')
            count_bytes = Encode.unsigned_int(count, '<')

            param_bytes = []
            param_bytes.extend(deferral_bytes)
            param_bytes.extend(interval_bytes)
            param_bytes.extend(count_bytes)

            cmd = SPINDIRx1Cmd.find('rs')
            self._transact(cmd, param_bytes)

            # wait...
            execution_time = cmd.execution_time + (((interval * count) + deferral) / 1000)
            # print("execution time: %s" % execution_time, file=sys.stderr)

            time.sleep(execution_time)

            # playback...
            cmd = SPINDIRx1Cmd.find('rp')
            cmd.return_count = count * 10

            response = self._transact(cmd)

            values = []

            for i in range(0, cmd.return_count, 10):
                timestamp = Decode.unsigned_int(response[i:i + 2], '<')
                pile_ref = Decode.long(response[i + 2:i + 6], '<')
                pile_act = Decode.long(response[i + 6:i + 10], '<')

                values.append((timestamp, pile_ref, pile_act))

            return values

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def input_raw(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRx1Cmd.find('ir')
            response = self._transact(cmd)
            v_in_value = Decode.unsigned_int(response, '<')

            return v_in_value

        finally:
            self.release_lock()


    def input_voltage(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRx1Cmd.find('iv')
            response = self._transact(cmd)
            v_in_voltage = Decode.float(response, '<')

            return v_in_voltage

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def watchdog_clear(self):
        try:
            self.obtain_lock()

            cmd = SPINDIRx1Cmd.find('wc')
            self._transact(cmd)

        finally:
            self.release_lock()


    def reset(self):
        try:
            self.obtain_lock()

            # force reset...
            cmd = SPINDIRx1Cmd.find('wr')
            self._transact(cmd)

            time.sleep(cmd.execution_time)

            # clear status...
            cmd = SPINDIRx1Cmd.find('wc')
            self._transact(cmd)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # arbitrary command, used for tests purposes...

    def cmd(self, name, response_time, execution_time, return_count):
        command = SPINDIRx1Cmd(name, response_time, execution_time, return_count)

        try:
            self.obtain_lock()

            self._transact(command)
            time.sleep(execution_time)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------
    # low-level calib functions...

    def _calib_r_unsigned_int(self, block, index):
        cmd = SPINDIRx1Cmd.find('cr')
        cmd.return_count = 2

        response = self._transact(cmd, (block, index))
        value = Decode.unsigned_int(response, '<')

        return value


    def _calib_w_unsigned_int(self, block, index, value):
        cmd = SPINDIRx1Cmd.find('cw')

        value_bytes = Encode.unsigned_int(value, '<')
        self._transact(cmd, (block, index), value_bytes)

        time.sleep(cmd.execution_time)


    def _calib_r_unsigned_long(self, block, index):
        cmd = SPINDIRx1Cmd.find('cr')
        cmd.return_count = 4

        response = self._transact(cmd, (block, index))
        value = Decode.unsigned_long(response, '<')

        return value


    def _calib_w_unsigned_long(self, block, index, value):
        cmd = SPINDIRx1Cmd.find('cw')

        value_bytes = Encode.unsigned_long(value, '<')
        self._transact(cmd, (block, index), value_bytes)

        time.sleep(cmd.execution_time)


    def _calib_r_float(self, block, index):
        cmd = SPINDIRx1Cmd.find('cr')
        cmd.return_count = 4

        response = self._transact(cmd, (block, index))
        value = Decode.float(response, '<')

        return value


    def _calib_w_float(self, block, index, value):
        cmd = SPINDIRx1Cmd.find('cw')

        value_bytes = Encode.float(value, '<')
        self._transact(cmd, (block, index), value_bytes)

        time.sleep(cmd.execution_time)


    # ----------------------------------------------------------------------------------------------------------------
    # SPI interactions...

    def _transact(self, cmd, param_group_1=None, param_group_2=None):
        # print("cmd: %s param_group_1:%s param_group_2:%s" %
        #       (cmd, str(param_group_1), str(param_group_2)), file=sys.stderr)

        try:
            self.__spi.open()

            # start_time = time.time()

            # command...
            self.__xfer(cmd.name_bytes())

            if param_group_1:
                time.sleep(self.__PARAM_DELAY)
                self.__xfer(param_group_1)

            if param_group_2:
                time.sleep(self.__PARAM_DELAY)
                self.__xfer(param_group_2)

            # elapsed_time = time.time() - start_time
            # print("elapsed 1: %0.6f" % elapsed_time, file=sys.stderr)

            # wait...
            time.sleep(cmd.response_time)

            # start_time = time.time()

            # ACK / NACK...
            response = self.__spi.read_bytes(1)
            # print("response 1: %s" % str(response), file=sys.stderr)

            if response[0] in self.__RESPONSE_NONE:
                raise NDIRException('None received', response[0], cmd, (param_group_1, param_group_2))

            if response[0] == self.__RESPONSE_NACK:
                raise NDIRException('NACK received', response[0], cmd, (param_group_1, param_group_2))

            if response[0] == self.__RESPONSE_BUSY:
                raise NDIRException('BUSY received', response[0], cmd, (param_group_1, param_group_2))

            # elapsed_time = time.time() - start_time
            # print("elapsed 2: %0.6f" % elapsed_time, file=sys.stderr)

            # return values...
            if cmd.return_count < 1:
                return

            # wait...
            time.sleep(self.__PARAM_DELAY)

            # start_time = time.time()

            response = self.__spi.read_bytes(cmd.return_count)
            # print("response 2: %s" % str(response), file=sys.stderr)

            # elapsed_time = time.time() - start_time
            # print("elapsed 3: %0.6f" % elapsed_time, file=sys.stderr)

            return response[0] if cmd.return_count == 1 else response

        finally:
            self.__spi.close()


    def wait(self):
        try:
            self.__spi.open()

            start_time = time.time()

            response = self.__spi.read_bytes(1)
            elapsed_time = time.time() - start_time

            print("wait: %s: 0x%02x" % (elapsed_time, response[0]))

        finally:
            self.__spi.close()


    def __xfer(self, values):
        self.__spi.xfer(list(values))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SPINDIRx1:{io:%s, spi:%s}" % (self.__io, self.__spi)
