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
    snapshot_dir          directory for saving captured images

    options:
    -h, --help                Show this help message and exit
    -d, --dropbox_uploader    Path to dropbox uploader script
    -v, --verbose             Set the log level to DEBUG
    -w, --window              Show video window
    -l, --logdir              Path to the log directory
    -c, --crop                A tuple of four integers for cropping frame
    -p, --period              Period in seconds for analysing video frame

## Upload to Dropbox

If you wish to upload the images to dropbox, there is a great tool to upload there.

https://github.com/andreafabrizi/Dropbox-Uploader

You can sepecify the path to the dropbox uploader script with the optional `--dropbox_uploader` parameter.

Prequisite is ofcourse you have setup the dropbox uploader script properly and the device is connected to internet.

## Hardware

This tool has been be tested with and optimized to run on raspberry pi zero with a camera attached.
![Raspberry Pi with attached camera module](/assets/images/raspberry_pi_zero_with_camera.jpg)

## Software

This tool is tested on python 3.9, 3.10 and 3.11.

Install the python dependencies with:

    python -m pip install -r requirements.txt --prefer-binary

## Troubleshooting

- Installing python dependencies on the raspberry pi can take considerable amount of time.
- Especially on raspberry pi zero, there can be specific issues installing opencv or numpy. This usually boils down to missing OS packages that need to be installed.

## Disclaimer

Please be aware of your local legal guidelines for installing security camera and taking people's images.