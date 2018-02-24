# Lía's Turntable

RaspberryPI-based digital turntable simulator written in Python.

## Installer environment

Setup your installer environment (laptop/PC from which the install process will be performed).

1. Install Ansible
2. Connect to RPI over ethernet
3. Confirm RPI reachable on standard Bonjour name `raspberrypi.local` (`ping raspberrypi.local`)
4. Setup ssh config for a `berry` alias pointing to `raspberrypi.local`
5. (Optional) Install turntable locally (in a venv) with `pip install -e .` . This allows all `turntable` commands listed below to be run locally. Otherwise it is understood each `turntable` command is run on the RPI by ssh-ing in first.

Suggested SSH config for berry:
```
Host berry
    Hostname raspberrypi.local
    User pi
    IdentityFile ~/.ssh/id_rsa
    CheckHostIp no
    StrictHostkeyChecking no
    UserKnownHostsFile=/dev/null
```

## RPI prep

0. Add `ssh` file to boot sector on latest Raspbian (Stretch or newer) image
1. Flash SD Card with image
2. Set up SSH keys on raspberrypi `ssh berry "mkdir -p .ssh && cat >> .ssh/authorized_keys" <  ~/.ssh/id_rsa.pub`

## RPI software setup

1. Run `ansible-playbook ansible/py3.yml` (Installs Python3.5 + dev tools and required libs on RPI)
2. Run `ansible-playbook ansible/turntable.yml` (Installs turntable Python software)

## RPI hardware setup

### (Optional) Install AMP+ "shield" on RPI

Refer to: https://www.hifiberry.com/build/documentation/connecting-power-supply-and-speakers-to-the-hifiberry-amp/

1. Power off RPI
2. Plug AMP+ onto RPI's GPIO
3. Connect speakers
4. Connect 12V power source to AMP+

*Testing*

5. Plug power supply
6. Observe leds
7. `ssh pi@berry` and validate correct login
8. Run `turntable beep`


3. Install Python3.5 on RPI using

Assumes the raspberry gets an IP of `192.168.2.3` and when the SD is inserted in your computer it's mounted at `/Volumes/boot`.

## Headless Raspberry PI setup

* Create Raspbian image on SD
* Create and empty `ssh` file on the volume's root: `touch /Volumes/boot/ssh`
* Unmount and install on Raspberry PI

## Install Python 3.5 and other dependencies


* Install `mpd`
* Modify mpd.conf
    - bind_to_address         "any"

## Hardware setup

1.
