#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_measure utility is used to interrogate the millisecond-level sampling performance of the NDIR board for
any period of time.

Sampling is performed on a round-trip basis - a single sample is requested, and the resulting values returned to the
host. This process limits the rate to 10 millisecond intervals but, because no microcontroller storage is required,
any volume of data can be obtained.

Returned values are voltages.

Note that the NDIR must be in single-shot run mode for the ndir_measure utility to be able to operate. This is set
using the ndir_run utility.

SYNOPSIS
ndir_measure.py [-i INTERVAL [-n SAMPLES]] [-v]

EXAMPLES
./ndir_measure.py -v -i 0.01

DOCUMENT EXAMPLE - OUTPUT
{"rec": "2018-06-04T15:50:20.513+00:00", "pile-ref": 2.4197, "pile-act": 2.8766, "therm": 0.9082}

SEE ALSO
scs_ndir/ndir_run
scs_ndir/ndir_sampler
scs_ndir/ndir_recorder
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.timed_runner import TimedRunner

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_measure import CmdNDIRMeasure
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir_conf import NDIRConf
from scs_ndir.sampler.ndir_voltage_measure import NDIRVoltageMeasure


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRMeasure()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("ndir_measure: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        if interface_conf is None:
            print("ndir_measure: InterfaceConf not available.", file=sys.stderr)
            exit(1)

        interface = interface_conf.interface()

        if interface is None:
            print("ndir_measure: Interface not available.", file=sys.stderr)
            exit(1)

        # NDIRConf...
        ndir_conf =  NDIRConf.load(Host)

        if ndir_conf is None:
            print("ndir_measure: NDIRConf not available.", file=sys.stderr)
            exit(1)

        # NDIR...
        ndir = ndir_conf.ndir(interface, Host)

        if cmd.verbose:
            print("ndir_measure: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        ndir.power_on()

        runner = TimedRunner(cmd.interval, cmd.samples)
        sampler = NDIRVoltageMeasure(runner, ndir)

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
