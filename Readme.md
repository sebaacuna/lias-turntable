# Lía's Turntable

## Raspberry PI setup

Assumes the raspberry gets an IP of `192.168.2.3` and when the SD is inserted in your computer it's mounted at `/Volumes/boot`.

## Headless Raspberry PI setup

* Create Raspbian image on SD
* Create and empty `ssh` file on the volume's root: `touch /Volumes/boot/ssh`
* Unmount and install on Raspberry PI

## Install Python 3.5 and other dependencies


* Install `mpd`
* Modify mpd.conf
    - bind_to_address         "any"
