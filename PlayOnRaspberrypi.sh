#!/bin/sh
pwd=$1
sshpass -p ${pwd} scp -r Player pi@192.168.1.200:/home/pi/tmp
# sshpass -p ${pwd} ssh pi@192.168.1.200 "cd /home/pi/tmp/Player; python3 Player.py"