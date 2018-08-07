#!/usr/bin/env python3

"""
Created on 1 Aug 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_run utility is used to shift the NDIR microcontroller between continuous sampling and single-shot sampling
modes.

NDIR microcontroller sampling is normally run in continuous mode. Sampling must be set to single-shot mode in order for
the ndir_measure and ndir_recorder utilities to operate.

SYNOPSIS
ndir_run.py { -s | -c } [-v]

EXAMPLES
./ndir_run.py -s

SEE ALSO
scs_ndir/ndir_measure
scs_ndir/ndir_pressure
scs_ndir/ndir_recorder
scs_ndir/ndir_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_run_mode import CmdNDIRRunMode
from scs_ndir.exception.ndir_exception import NDIRException
from scs_ndir.ndir_conf import NDIRConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRRunMode()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("ndir_run: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        conf =  NDIRConf.load(Host)
        ndir = conf.ndir(Host)

        if cmd.verbose:
            print("ndir_run: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()

        # ------------------------------------------------------------------------------------------------------------
        # run...

        ndir.cmd_sample_mode(cmd.single)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        jstr = JSONify.dumps(ex)
        print(jstr, file=sys.stderr)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
