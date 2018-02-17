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
./ndir_power.py -v 0
"""

import sys

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_power import CmdNDIRPower
from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRPower()

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

        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.power:
            ndir.power_on()
        else:
            ndir.power_off()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except ValueError as ex:
        print("ValueError: %s" % ex)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()