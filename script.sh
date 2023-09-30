#!/bin/bash
cd /home/pi/sb/security-cam
/home/pi/sb/security-cam/.venv/bin/python -m src.capture.security_cam /home/pi/Pictures -v -d /home/pi/sb/Dropbox-Uploader/dropbox_uploader.sh -l /home/pi/sb/security-cam/logs
