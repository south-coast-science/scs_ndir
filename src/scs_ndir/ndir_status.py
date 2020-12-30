#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_status utility is used to report on the NDIR microcontroller operation, startup condition, and input
power voltage.

SYNOPSIS
ndir_status.py [-v]

EXAMPLES
./ndir_status.py

DOCUMENT EXAMPLE - OUTPUT
{"w-rst": false, "pwr-in": 4.6, "up": {"period": "00-00:08:58.000"}}

SEE ALSO
scs_ndir/ndir_version
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_verbose import CmdVerbose
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir.ndir_conf import NDIRConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdVerbose()

    if cmd.verbose:
        print("ndir_status: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.Sensors.open()

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        if interface_conf is None:
            print("ndir_status: InterfaceConf not available.", file=sys.stderr)
            exit(1)

        interface = interface_conf.interface()

        if interface is None:
            print("ndir_status: Interface not available.", file=sys.stderr)
            exit(1)

        # NDIRConf...
        ndir_conf =  NDIRConf.load(Host)

        if ndir_conf is None:
            print("ndir_status: NDIRConf not available.", file=sys.stderr)
            exit(1)

        # NDIR...
        ndir = ndir_conf.ndir(interface, Host)

        if cmd.verbose:
            print("ndir_status: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        ndir.power_on()

        status = ndir.status()
        print(JSONify.dumps(status))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        print(JSONify.dumps(ex), file=sys.stderr)
        exit(1)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.Sensors.close()

