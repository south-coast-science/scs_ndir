#!/usr/bin/env python3

"""
Created on 31 Jul 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_pressure utility is used to sample the NXP MPL115A2 digital barometer on the NDIR board. The reported value
is actual pressure, measured in kilopascals.

Note that barometric pressure is not currently used by the data interpretation algorithm on board the NDIR
microcontroller.

SYNOPSIS
ndir_pressure.py [-i INTERVAL [-n SAMPLES]] [-v]

EXAMPLES
./ndir_pressure.py -i 2 -n 10

DOCUMENT EXAMPLE - OUTPUT
{"rec": "2018-07-31T15:32:37.117+00:00", "pA": 101.6}

SEE ALSO
scs_ndir/ndir_run
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.timed_runner import TimedRunner

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_pressure import CmdNDIRPressure
from scs_ndir.exception.ndir_exception import NDIRException
from scs_ndir.sampler.ndir_pressure_sampler import NDIRPressureSampler

from scs_ndir.ndir_conf import NDIRConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRPressure()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("ndir_pressure: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        conf =  NDIRConf.load(Host)
        ndir = conf.ndir(Host)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        runner = TimedRunner(cmd.interval, cmd.samples)
        sampler = NDIRPressureSampler(runner, ndir)

        if cmd.verbose:
            print("ndir_pressure: %s" % sampler, file=sys.stderr)
            sys.stderr.flush()

        for sample in sampler.samples():
            print(JSONify.dumps(sample))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        jstr = JSONify.dumps(ex)
        print(jstr, file=sys.stderr)

    finally:
        I2C.close()
