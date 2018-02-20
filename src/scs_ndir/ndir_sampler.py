#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The XX utility is used to .

EXAMPLES
xx

FILES
~/SCS/aws/

DOCUMENT EXAMPLE
xx

SEE ALSO
scs_ndir/



command line example:
./ndir_sampler.py -v -i 1.0
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.timed_runner import TimedRunner

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_sampler import CmdNDIRSampler
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir import NDIR
from scs_ndir.sampler.ndir_voltage_sampler import NDIRVoltageSampler

from scs_ndir.test.ndir_window_datum import NDIRWindowDatum


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRSampler()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(1)

    if cmd.verbose:
        print(cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
        ndir.power_on()

        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.mode is not None:
            # set run mode...
            ndir.cmd_sample_mode(cmd.mode == 0)

        elif cmd.window is not None:
            # retrieve the last sample window...
            calib = ndir.cmd_retrieve_eeprom_calib()
            samples = ndir.cmd_sample_window()

            for i in range(len(samples)):
                rec = calib.min_deferral + i + 1
                datum = NDIRWindowDatum.construct_from_sample(rec, samples[i])
                print(JSONify.dumps(datum))


        elif cmd.dump is not None:
            single_shot, is_running, index, max_cycles, min_cycles, cycles = ndir.cmd_sample_dump()

            print("single_shot: %s" % single_shot)
            print("is_running: %s" % is_running)
            print("index: %s" % index)
            print("max_cycles: %s" % max_cycles)
            print("min_cycles: %s" % min_cycles)
            print("cycles: %s" % cycles)

        else:
            # run sampling...
            runner = TimedRunner(cmd.interval, cmd.samples)
            sampler = NDIRVoltageSampler(runner, ndir)

            prev_prev_sample = None
            prev_sample = None

            for sample in sampler.samples():
                print(JSONify.dumps(sample))
                sys.stdout.flush()

                # check for stuck data
                if sample == prev_sample == prev_prev_sample:
                    print(chr(7))

                    single_shot, is_running, index, max_cycles, min_cycles, cycles = ndir.cmd_sample_dump()

                    print("single_shot: %s" % single_shot)
                    print("is_running: %s" % is_running)
                    print("index: %s" % index)
                    print("max_cycles: %s" % max_cycles)
                    print("min_cycles: %s" % min_cycles)
                    print("cycles: %s" % cycles)

                    break

                prev_prev_sample = prev_sample
                prev_sample = sample


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        jstr = JSONify.dumps(ex)
        print(jstr, file=sys.stderr)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
