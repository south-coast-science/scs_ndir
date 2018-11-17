#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_power utility is used to apply or remove power from the NDIR board.

Note that all other utilities in the scs_ndir package begin by applying power to the NDIR board (if it is not already
powered) and leave power applied on termination.

The ndir_power utility has no effect when used with Raspberry Pi DFE boards.

SYNOPSIS
ndir_power.py { 1 | 0 } [-v]

EXAMPLES
./ndir_power.py -v 0

SEE ALSO
scs_ndir/ndir_reset
"""

import sys

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_power import CmdNDIRPower
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.ndir_conf import NDIRConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRPower()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("ndir_power: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        # NDIRConf...
        conf =  NDIRConf.load(Host)

        if conf is None:
            print("ndir_power: NDIRConf not available.", file=sys.stderr)
            exit(1)

        # NDIR...
        ndir = conf.ndir(Host)

        if cmd.verbose:
            print("ndir_power: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.power:
            ndir.power_on()
        else:
            ndir.power_off()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        print(JSONify.dumps(ex), file=sys.stderr)
        exit(1)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
