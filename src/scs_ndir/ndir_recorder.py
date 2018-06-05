#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The XX utility is used to .

SYNOPSIS
ndir_recorder.py -i INTERVAL -n SAMPLES [-d DEFERRAL] [-v]

EXAMPLES
./ndir_recorder.py -i 4 -n 250

DOCUMENT EXAMPLE
{"rec": 5, "pile-ref": 10146, "pile-act": 6231}

SEE ALSO
scs_ndir/ndir_measure
scs_ndir/ndir_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_recorder import CmdNDIRRecorder
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.ndir_conf import NDIRConf
from scs_ndir.datum.ndir_recorder_datum import NDIRRecorderDatum


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRRecorder()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(1)

    if cmd.verbose:
        print("ndir_recorder: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        conf =  NDIRConf.load(Host)
        ndir = conf.ndir(Host)

        if cmd.verbose:
            print("ndir_recorder: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()

        # ------------------------------------------------------------------------------------------------------------
        # run...

        ndir.power_on()

        samples = ndir.cmd_record_raw(cmd.deferral, cmd.interval, cmd.samples)

        for i in range(len(samples)):
            datum = NDIRRecorderDatum.construct_from_sample(samples[i])
            print(JSONify.dumps(datum))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        jstr = JSONify.dumps(ex)
        print(jstr, file=sys.stderr)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
