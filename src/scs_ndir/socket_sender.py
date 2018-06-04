#!/usr/bin/env python3

"""
Created on 18 Aug 2016

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
./status_sampler.py -n 10 | ./socket_sender.py bruno.local -e
"""

import sys

from scs_host.comms.network_socket import NetworkSocket

from scs_ndir.cmd.cmd_socket_sender import CmdSocketSender


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    sender = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSocketSender()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("socket_sender: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        sender = NetworkSocket(cmd.hostname, cmd.port)

        if cmd.verbose:
            print("socket_sender: %s" % sender, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        sender.connect(True)

        for line in sys.stdin:
            sender.write(line, True)

            if cmd.echo:
                print(line.strip())
                sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        print("")

    finally:
        if sender:
            sender.close()
