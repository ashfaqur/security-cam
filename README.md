# security-cam
A python based home security observer based on OpenCV optimized to run on raspberry pi zero.

## Taking snapshots

This program observes the camera video input and takes snapshots whenever it detects a person using OpenCV's body detection algorithm.

Here is an example of how the snapshot would look like:

![Example picture](/assets/images/example_detection.jpg)

## Usage

    $ python -m src.capture.security_cam -h
    usage: security_cam.py [-h] [-d dropbox_uploader] [-v] [-w] [-l logdir] [-c crop]
                        [-p period]
                        snapshot_dir

    Captures images and videos from camera based on person detection

    positional arguments:
    snapshot_dir          directory for saving snapshots

    options:
    -h, --help            show this help message and exit
    -d dropbox_uploader, --dropbox_uploader dropbox_uploader
                            Path to dropbox uploader script
    -v, --verbose         Set the log level to DEBUG
    -w, --window          Show video window
    -l logdir, --logdir logdir
                            Path to the log directory
    -c crop, --crop crop  A tuple of four integers for cropping frame
    -p period, --period period
                            Period in seconds for analysing video frame

## Upload to Dropbox

If you wish to upload the images to dropbox, there is a great tool to upload there.

https://github.com/andreafabrizi/Dropbox-Uploader

You can sepecify the path to the dropbox uploader script with the optional `--dropbox_uploader` parameter.

Prequisite is ofcourse you have setup the dropbox uploader script properly and the device is connected to internet.

## Disclaimer

Please be aware of your local legal guidelines for installing security camera and taking people's images.