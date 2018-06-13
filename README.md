# scs_ndir
Calibration, control and environmental sampling tools for the SPI NDIR board

_Contains command line utilities and library classes._


**Required libraries:** 

* SCS root: scs_core
* SCS host: scs_host_bbe, scs_host_bbe_southern or scs_host_rpi


**Branches:**

The stable branch of this repository is master. For deployment purposes, use:

    git clone --branch=master https://github.com/south-coast-science/scs_ndir.git


**Example PYTHONPATH:**

Raspberry Pi, in /home/pi/.bashrc:

    export PYTHONPATH=~/SCS/scs_ndir/src:~/SCS/scs_host_rpi/src:~/SCS/scs_core/src:$PYTHONPATH


BeagleBone, in /root/.bashrc:

    export PYTHONPATH=/home/debian/SCS/scs_ndir/src:/home/debian/SCS/scs_host_bbe/src:/home/debian/SCS/scs_core/src:$PYTHONPATH


BeagleBone, in /home/debian/.bashrc:

    export PYTHONPATH=~debian/SCS/scs_ndir/src:~/SCS/scs_host_bbe/src:~/SCS/scs_core/src:$PYTHONPATH
