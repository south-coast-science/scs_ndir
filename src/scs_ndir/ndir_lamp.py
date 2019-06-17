#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_lamp utility is used to command the lamp to oscillate on and off, or to remain off.

Note that ff the lamp is switched off, it will only retain this state until the NDIR board is reset or power cycled.

On future versions of the NDIR board, the ndir_lamp utility may also be used to set the lamp voltage.

SYNOPSIS
ndir_lamp.py { -r ON | -l VOLTAGE } [-v]

EXAMPLES
./ndir_lamp.py -v 0
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.board.dfe_conf import DFEConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_lamp import CmdNDIRLamp
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir_conf import NDIRConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRLamp()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("ndir_lamp: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        # DFEConf...
        dfe_conf = DFEConf.load(Host)

        if dfe_conf is None:
            print("ndir_lamp: DFEConf not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose and dfe_conf:
            print("ndir_lamp: %s" % dfe_conf, file=sys.stderr)

        # NDIRConf...
        ndir_conf =  NDIRConf.load(Host)

        if ndir_conf is None:
            print("ndir_lamp: NDIRConf not available.", file=sys.stderr)
            exit(1)

        # NDIR...
        ndir = ndir_conf.ndir(Host, dfe_conf.load_switch_active_high)

        if cmd.verbose:
            print("ndir_lamp: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        ndir.power_on()

        if cmd.level is not None:
            print("lamp level not currently supported", file=sys.stderr)

        if cmd.run is not None:
            ndir.lamp_run(cmd.run == 1)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        print(JSONify.dumps(ex), file=sys.stderr)
        exit(1)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
