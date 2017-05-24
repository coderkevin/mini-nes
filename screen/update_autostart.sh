#!/bin/bash

AUTOSTART_SH=/opt/retropie/configs/all/autostart.sh
VAR_WORK_DIR=/var/lib/screen_manager
RUN_LINE="python $VAR_WORK_DIR/screen_manager.py"

ed -s $AUTOSTART_SH <<EOF
H
/emulationstation/s/^/#
0r !echo $RUN_LINE
wq
EOF

