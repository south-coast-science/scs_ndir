#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_reset utility is used to force a system reset on the NDIR microcontroller.

On performing a reset, calibration values are reloaded and the lamp is set to run.

SYNOPSIS
ndir_reset.py [-v]

EXAMPLES
./ndir_reset.py

SEE ALSO
scs_ndir/ndir_calib
scs_ndir/ndir_lamp
scs_ndir/ndir_power
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_verbose import CmdVerbose
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir_conf import NDIRConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdVerbose()

    if cmd.verbose:
        print("ndir_reset: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        if interface_conf is None:
            print("ndir_reset: InterfaceConf not available.", file=sys.stderr)
            exit(1)

        interface = interface_conf.interface()

        if interface is None:
            print("ndir_reset: Interface not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose and interface:
            print("ndir_reset: %s" % interface, file=sys.stderr)

        # NDIRConf...
        ndir_conf =  NDIRConf.load(Host)

        if ndir_conf is None:
            print("ndir_reset: NDIRConf not available.", file=sys.stderr)
            exit(1)

        # NDIR...
        ndir = ndir_conf.ndir(Host, interface.load_switch_active_high)

        if cmd.verbose:
            print("ndir_reset: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        ndir.power_on()

        ndir.reset()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        print(JSONify.dumps(ex), file=sys.stderr)
        exit(1)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
