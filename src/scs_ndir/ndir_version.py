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
./ndir_version.py
"""

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        ndir = NDIR(Host.ndir_spi_bus(), Host.ndir_spi_device())
        ndir.power_on()

        # ------------------------------------------------------------------------------------------------------------
        # run...

        version = ndir.cmd_version()
        jstr = JSONify.dumps(version)
        print(jstr)

    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except ValueError as ex:
        print("ValueError: %s" % ex)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
