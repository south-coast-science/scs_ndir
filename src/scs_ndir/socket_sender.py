#!/usr/bin/env python3

"""
Created on 18 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The socket_sender utility is used to transmit data over a network socket. The recipient may be the same host
(identified as localhost) or another host on the same local area network.

The socket_sender utility should be started after the socket_receiver has been started. When the socket_sender
utility terminates, the socket_receiver utility terminates automatically.

The recipient may be identified by IP address or - if the environment supports ZeroConf / Bonjour - by hostname.local.

If a port number is not specified, then port 2000 is used.

SYNOPSIS
socket_sender.py HOSTNAME [-p PORT] [-e] [-v]

EXAMPLES
./ndir_sampler.py -i 1 -n 10 | ./socket_sender.py bruno.local -e -p 2002

SEE ALSO
scs_analysis/socket_receiver

BUGS
It is possible to create scenarios where a port becomes orphaned. Depending on host operating systems, orphaned ports
may take time to be garbage collected.
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

        sender = NetworkSocket(host=cmd.hostname, port=cmd.port)

        if cmd.verbose:
            print("socket_sender: %s" % sender, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        sender.connect()

        for line in sys.stdin:
            sender.write(line)

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
