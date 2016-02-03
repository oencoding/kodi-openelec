#!/bin/sh
PATH=/sbin:/usr/sbin:/bin:/usr/bin
ACEADDON="$HOME/.kodi/userdata/addon_data/program.plexus/acestream"
ACECHROOT="androidfs"
 
if ! [ $(id -u) = 0 ]; then
        PERMISSION=sudo
fi
 
$PERMISSION mount -t proc proc $ACEADDON/$ACECHROOT/proc &>/dev/null
$PERMISSION mount -t sysfs sysfs $ACEADDON/$ACECHROOT/sys &>/dev/null
$PERMISSION mount -o bind /dev $ACEADDON/$ACECHROOT/dev &>/dev/null
$PERMISSION $ACEADDON/chroot $ACEADDON/$ACECHROOT /system/bin/sh -c "cd /system/data/data/org.acestream.engine/files ; /system/bin/acestream.sh" > $ACEADDON/acestream.log 2>&1 - << EOF
import os
import argparse
from acestreamengine import Core
 
params = "$@".split(' ')
if params == ['']:
    params = []
 
Core.run(params)
EOF
