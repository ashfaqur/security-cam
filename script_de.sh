#!/bin/bash

while true; do
    cd /home/pi/sb/security-cam
    if pgrep -f "src.capture.security_cam" > /dev/null
    then
        echo "Running"
    else
        echo "Stopped, Restarting"
        /home/pi/sb/security-cam/.venv/bin/python -m src.capture.security_cam /home/pi/Pictures -v -d /home/pi/sb/Dropbox-Uploader/dropbox_uploader.sh -u de/images -l /home/pi/sb/security-cam/logs &
    fi
    sleep 5
done