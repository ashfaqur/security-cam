#!/bin/bash

while true; do
    cd /home/pi/sb/security-cam
    if pgrep -f "src.capture.security_cam" > /dev/null
    then
        echo "Running"
    else
        echo "Stopped, Restarting"
        /home/pi/sb/security-cam/.venv/bin/python -m src.capture.security_cam /home/pi/Pictures -v -d /home/pi/sb/Dropbox-Uploader/dropbox_uploader.sh -u bd/images -l /home/pi/sb/security-cam/logs -c "110,320,220,440" -p 4 -s 3 &
    fi
    sleep 600
done
