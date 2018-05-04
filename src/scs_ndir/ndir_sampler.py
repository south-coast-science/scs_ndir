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
./ndir_sampler.py -v -i 1.0
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.timed_runner import TimedRunner
from scs_core.sys.system_id import SystemID

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_ndir.cmd.cmd_ndir_sampler import CmdNDIRSampler
from scs_ndir.exception.ndir_exception import NDIRException

from scs_ndir.ndir_conf import NDIRConf

from scs_ndir.sampler.ndir_sampler import NDIRSampler
from scs_ndir.sampler.ndir_voltage_sampler import NDIRVoltageSampler


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRSampler()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(1)

    if cmd.verbose:
        print(cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # SystemID...
        system_id = SystemID.load(Host)

        tag = None if system_id is None else system_id.message_tag()

        # NDIR...
        I2C.open(Host.I2C_SENSORS)

        conf =  NDIRConf.load(Host)
        ndir = conf.ndir(Host)

        ndir.power_on()

        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.mode is not None:
            # set run mode...
            ndir.cmd_sample_mode(cmd.mode == 0)

        elif cmd.offsets is not None:
            min_ref_offset, min_act_offset, max_ref_offset, max_act_offset = ndir.cmd_sample_offsets()

            print("min_ref_offset: %s" % min_ref_offset)
            print("min_act_offset: %s" % min_act_offset)
            print("max_ref_offset: %s" % max_ref_offset)
            print("max_act_offset: %s" % max_act_offset)

        else:
            # run sampling...
            runner = TimedRunner(cmd.interval, cmd.samples)
            sampler = NDIRVoltageSampler(runner, tag, ndir) if cmd.raw else NDIRSampler(runner, tag, ndir)

            for sample in sampler.samples():
                print(JSONify.dumps(sample))
                sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except NDIRException as ex:
        jstr = JSONify.dumps(ex)
        print(jstr, file=sys.stderr)

    except KeyboardInterrupt:
        print("")

    finally:
        I2C.close()
