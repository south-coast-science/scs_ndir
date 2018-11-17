#!/usr/bin/env python3

"""
Created on 17 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_recorder utility is used to interrogate the millisecond-level sampling performance of the NDIR board at the
highest-possible sample rate.

The NDIR microcontroller can store up to 250 Pile REF, Pile ACT and THERMISTOR samples. The microcontroller samples all
three signals every millisecond. The ndir_recorder utility commands recording to begin on the next lamp rising edge,
and stop recording after a given number of recorded values. When recording is complete, the utility recovers the
stored values.

Returned values are raw ADC counts.

Command parameters specify interval and total. For example, an interval of 4 and a total of 250 provides one second
of data, at 4 millisecond intervals. A further parameter specifies the time from the rising lamp edge until recording
starts (default 0 milliseconds).

Note that the NDIR must be in single-shot run mode for the ndir_recorder utility to be able to operate. This is set
using the ndir_run utility.

SYNOPSIS
ndir_recorder.py -i INTERVAL -n SAMPLES [-d DEFERRAL] [-v]

EXAMPLES
./ndir_recorder.py -i 4 -n 250

DOCUMENT EXAMPLE - OUTPUT
{"rec": 5, "pile-ref": 10146, "pile-act": 6231}

SEE ALSO
scs_ndir/ndir_measure
scs_ndir/ndir_run
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
        exit(2)

    if cmd.verbose:
        print("ndir_recorder: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        # NDIRConf...
        conf =  NDIRConf.load(Host)

        if conf is None:
            print("ndir_recorder: NDIRConf not available.", file=sys.stderr)
            exit(1)

        # NDIR...
        ndir = conf.ndir(Host)

        if cmd.verbose:
            print("ndir_recorder: %s" % ndir, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        ndir.power_on()

        samples = ndir.record_raw(cmd.deferral, cmd.interval, cmd.samples)

        for i in range(len(samples)):
            datum = NDIRRecorderDatum.construct_from_sample(samples[i])
            print(JSONify.dumps(datum))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        print(JSONify.dumps(ex), file=sys.stderr)
        exit(1)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
