#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_conf utility is used to specify whether an NDIR board is present and if so, which model is provided.
Currently, the only model supported is v1.

The tally count specifies the number of consecutive samples used to perform averaging. Averaging is not performed by
any of the utilities in this package, but is performed by the scs_dev/gases_sampler utility.

This utility is also included in the scs_mfr package.

SYNOPSIS
ndir_conf.py [{ [-m MODEL] [-t AVERAGING_TALLY] | -d }] [-v]

EXAMPLES
./ndir_conf.py -m v1 -t 1

FILES
~/SCS/conf/ndir_conf.json

DOCUMENT EXAMPLE
{"model": "v1", "tally": 10}

SEE ALSO
scs_dev/gases_sampler
scs_mfr/ndir_conf
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_conf import CmdNDIRConf
from scs_ndir.gas.ndir_conf import NDIRConf


# TODO: handle missing conf elegantly - do this throughout the system.

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("ndir_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # NDIRConf...
    conf = NDIRConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("ndir_conf: No configuration is stored. You must therefore set all fields.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        model = cmd.model if cmd.model else conf.model
        tally = cmd.tally if cmd.tally else conf.tally

        conf = NDIRConf(model, tally)
        conf.save(Host)

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
