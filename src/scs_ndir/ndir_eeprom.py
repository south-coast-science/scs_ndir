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
./ndir_eeprom.py -s min-deferral 740
"""

import sys

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_eeprom import CmdNDIREEPROM
from scs_ndir.gas.ndir import NDIR
from scs_ndir.gas.ndir_calib import NDIRCalib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIREEPROM()

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

        calib = ndir.cmd_retrieve_eeprom_calib()
        jdict = calib.as_json()

        if cmd.get() or cmd.set():
            if cmd.name not in jdict:
                print("ndir_eeprom: name not known: %s" % cmd.name, file=sys.stderr)
                exit(2)

        if cmd.get():
            print(jdict[cmd.name])

        elif cmd.set():
            # set...
            jdict[cmd.name] = cmd.value
            calib = NDIRCalib.construct_from_jdict(jdict)

            # test...
            jdict = calib.as_json()
            if jdict[cmd.name] is None:
                print("ndir_eeprom: value not acceptable: %s" % cmd.value, file=sys.stderr)
                exit(2)

            # save...
            ndir.cmd_store_eeprom_calib(calib)

        else:
            # report...
            print(JSONify.dumps(calib))



    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except ValueError as ex:
        print("ValueError: %s" % ex)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
