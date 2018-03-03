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
./ndir_calib.py -s min-deferral 740
"""

import sys

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_calib import CmdNDIRCalib
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir import NDIR
from scs_ndir.gas.ndir_calib import NDIRCalib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRCalib()

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

        if cmd.default:
            calib = NDIRCalib.default()

            # save...
            ndir.store_calib(calib)


        elif cmd.set():
            # retrieve...
            calib = ndir.retrieve_calib()
            jdict = calib.as_json()

            # validate...
            if cmd.name not in jdict:
                print("ndir_calib: field name not known: %s" % cmd.name, file=sys.stderr)
                exit(2)

            # set...
            jdict[cmd.name] = cmd.value
            calib = NDIRCalib.construct_from_jdict(jdict)

            # datum...
            jdict = calib.as_json()
            if jdict[cmd.name] is None:
                print("ndir_calib: field value not acceptable: %s" % cmd.value, file=sys.stderr)
                exit(2)

            # save...
            ndir.store_calib(calib)

        else:
            calib = ndir.retrieve_calib()

        # report...
        print(JSONify.dumps(calib))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        jstr = JSONify.dumps(ex)
        print(jstr, file=sys.stderr)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
