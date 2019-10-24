#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_sampler utility is used to report CO2 concentrations.

Additional functions are provided: the ndir_sampler can report amplitude voltages, maxima and minima time offsets,
and can change the sampling mode from single-shot to continuous.

When running in continuous mode, the NDIR microcontroller generates a new sample at an interval set by the lamp
period, based on the relative Pile REF and Pile ACT amplitudes, and a THERMISTOR average. The host can interrogate the
NDIR microcontroller at any time to obtain the most recent value.

Returned values are voltages when the -r (raw) flag is set, otherwise the values are gas concentrations.

When in single-shot mode, the -o (offset) mode can be used to find the time offset of REF and ACT maxima and minima.

SYNOPSIS
ndir_sampler.py { -m { 1 | 0 } | [-i INTERVAL [-n SAMPLES] [-r]] | -o } [-v]

EXAMPLES
./ndir_sampler.py -v -i 1.0

DOCUMENT EXAMPLES - OUTPUT
{"tag": "scs-be2-3", "rec": "2018-06-04T15:53:34.939+00:00",
"val": {"CO2": {"pile-ref-ampl": 1.9527, "pile-act-ampl": 3.2046, "therm-avg": 0.9128}}}

{"tag": "scs-be2-3", "rec": "2018-06-04T15:53:27.966+00:00",
"val": {"CO2": {"tmp": 36.5, "cnc-raw": 432.1, "cnc": 468.2}}}

SEE ALSO
scs_ndir/ndir_measure
scs_ndir/ndir_recorder
scs_ndir/ndir_run
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.timed_runner import TimedRunner
from scs_core.sys.system_id import SystemID

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_sampler import CmdNDIRSampler
from scs_ndir.datum.ndir_offset_datum import NDIROffsetDatum
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir_conf import NDIRConf

from scs_ndir.sampler.ndir_sampler import NDIRSampler
from scs_ndir.sampler.ndir_voltage_sampler import NDIRVoltageSampler


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRSampler()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("ndir_sampler: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # SystemID...
        system_id = SystemID.load(Host)

        tag = None if system_id is None else system_id.message_tag()

        I2C.open(Host.I2C_SENSORS)

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        if interface_conf is None:
            print("ndir_sampler: InterfaceConf not available.", file=sys.stderr)
            exit(1)

        interface = interface_conf.interface()

        if interface is None:
            print("ndir_sampler: Interface not available.", file=sys.stderr)
            exit(1)

        # NDIRConf...
        ndir_conf =  NDIRConf.load(Host)

        if ndir_conf is None:
            print("ndir_sampler: NDIRConf not available.", file=sys.stderr)
            exit(1)

        # NDIR...
        ndir = ndir_conf.ndir(interface, Host)

        if cmd.verbose:
            print("ndir_sampler: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        ndir.power_on()

        if cmd.offsets is not None:
            datum = NDIROffsetDatum.construct_from_sample(ndir.get_sample_offsets())

            print(JSONify.dumps(datum))
            sys.stdout.flush()

        else:
            runner = TimedRunner(cmd.interval, cmd.samples)
            sampler = NDIRVoltageSampler(runner, tag, ndir) if cmd.raw else NDIRSampler(runner, tag, ndir)

            if cmd.verbose:
                print("ndir_sampler: %s" % sampler, file=sys.stderr)
                sys.stderr.flush()

            for sample in sampler.samples():
                print(JSONify.dumps(sample))
                sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        print(JSONify.dumps(ex), file=sys.stderr)
        exit(1)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
