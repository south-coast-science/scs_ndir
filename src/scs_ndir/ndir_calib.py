#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_calib utility is used to read or set a wide range of parameters that are stored on the EEPROM on the NDIR
SPI board. Parameters fall into two groups:

* Common to all ranges - ndir-serial, board-serial, selected-range, lamp-voltage, lamp-period, sample-start, sample-end
* Range-specific - zero, span, linear-b, linear-c, alpha-low, alpha-high, beta-a, beta-o, and t-cal

Up to five range sets can be specified:

1. range-iaq
2. range-safety
3. range-combustion
4. range-industrial
5. range-custom

The range set to be used is specified by the selected-range field, which must be set to an integer between 1 and 5.

An initial group of settings can be written to the EEPROM using the -d flag (default). The default settings will not
provide an accurate calibration, but will enable the NDIR board to operate.

SYNOPSIS
ndir_calib.py [{ -d | -s PATH VALUE | -r }] [-v]

EXAMPLES
./ndir_calib.py -s selected-range 1
./ndir_calib.py -s range-iaq.zero 0.644

DOCUMENT EXAMPLE
{"ndir-serial": 12701439, "board-serial": 2000001, "selected-range": 1, "lamp-voltage": 4.5, "lamp-period": 1000,
"sample-start": 10, "sample-end": 990, "range-iaq": {"zero": 0.644, "span": 0.2203,
"linear-b": 0.000325, "linear-c": 0.9363, "alpha-low": 0.00042, "alpha-high": 0.00042,
"beta-a": 1e-05, "beta-o": 1e-05, "t-cal": 34.0}, "range-safety": null, "range-combustion": null,
"range-industrial": null, "range-custom": null}

SEE ALSO
scs_ndir/ndir_reset
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_calib import CmdNDIRCalib
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.gas.ndir_conf import NDIRConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRCalib()

    if cmd.verbose:
        print("ndir_calib: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        if interface_conf is None:
            print("ndir_calib: InterfaceConf not available.", file=sys.stderr)
            exit(1)

        interface = interface_conf.interface()

        if interface is None:
            print("ndir_calib: Interface not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose and interface:
            print("ndir_calib: %s" % interface, file=sys.stderr)

        # NDIRConf...
        ndir_conf =  NDIRConf.load(Host)

        if ndir_conf is None:
            print("ndir_calib: NDIRConf not available.", file=sys.stderr)
            exit(1)

        # calib...
        calib_class = ndir_conf.calib_class()

        # NDIR...
        ndir = ndir_conf.ndir(interface, Host)

        if cmd.verbose:
            print("ndir_calib: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        ndir.power_on()

        if cmd.default:
            calib = calib_class.default()

            # save...
            ndir.store_calib(calib)

        elif cmd.restart:
            ndir.reload_calib()

        elif cmd.set():
            # retrieve...
            calib = ndir.retrieve_calib()
            dictionary = PathDict.construct_from_jstr(JSONify.dumps(calib))

            # validate...
            if not dictionary.has_path(cmd.path):
                print("ndir_calib: field name not known: %s" % cmd.path, file=sys.stderr)
                exit(2)

            # set...
            dictionary.append(cmd.path, cmd.value)
            calib = calib_class.construct_from_jdict(dictionary.as_json())

            # validate...
            dictionary = PathDict.construct_from_jstr(JSONify.dumps(calib))

            if dictionary.node(cmd.path) is None:
                print("ndir_calib: field value not acceptable: %s" % cmd.value, file=sys.stderr)
                exit(2)

            # save...
            ndir.store_calib(calib)

        # confirm...
        calib = ndir.retrieve_calib()

        # report...
        print(JSONify.dumps(calib))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        print(JSONify.dumps(ex), file=sys.stderr)
        exit(1)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
