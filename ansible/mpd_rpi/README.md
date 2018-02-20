MPD on Raspberry Pi
===================

The role and playbook are intended for:
 
* Installation [MPD](http://www.musicpd.org/) on Raspberry Pi 2.
* Setup [HiFiberry DAC+](https://www.hifiberry.com/dacplus/) on brand new [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) installation.
* Tuning MPD for bit perfect output.
* Setup MPD to consume audio data from SMB share.
* Original [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) installation is "minimized", i.e. redundant packages are deleted (e.g. xserver-xorg, etc.).

Requirements
------------

1. Ansible itself.
1. Well, Ansible works perfectly on the Linux, so Linux control host is required as well :smile:
1. Running __Raspberry Pi 2__ machine with brand new [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) installed.  
1. Ansible [inventory file](http://docs.ansible.com/ansible/intro_inventory.html) with your __Raspberry Pi 2__ machine.
1. SMB server with shared audio files for all users (i.e. without password).

Role Variables
--------------

These variables are all situated in the vars/main.yml and have to be adjusted by you.

|Name                   | Type   | Description                                                                |
|-----------------------|--------|----------------------------------------------------------------------------|
|mpdrpi_media_share_name| string | The full path top SMB share (example: //nas/media) |
|mpdrpi_music_directory | string | It represents the audio files directory relative to the mounted SMB share (example: audio/).|
 
Inventory
---------
The [inventory file](http://docs.ansible.com/ansible/intro_inventory.html) file has to
contain __mpd_hosts__ group, which is
used in the role. 
You have to add your Raspberry Pi host name into this group. 
Example of inventory file:
    
    [mpd_hosts]
    my_rpi_for_mpd

Dependencies
------------

___RPI Mini___ role is used to reduce bloating of intact [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) installation.

Example Playbook
----------------

    - hosts:
        - mpd_hosts
      roles:
        - rpi_mini
        - mpd_rpi
        
Usage examples
--------------

1. It's a good practice to reset default SSH host keys. It's useful to apply once only.
   Note the __"rpimini_ssh_reset=true"__ usage.

        ansible-playbook -i hosts mpd_rpi.yml -u root --tags=ssh_reset --extra-vars "rpimini_ssh_reset=true" 

1. To make all role tasks except SSH host keys resetting run following command.

        ansible-playbook -i hosts mpd_rpi.yml -u root 
    
1. If the MPD configuration (i.e. mpd.conf.j2) was changed, it can be
   deployed by following command. Note the __"--tags=mpd"__ usage.
   Other tasks are not executed.

        ansible-playbook -i hosts mpd_rpi.yml -u root --tags=mpd
        
Notes
-----

After first complete (i.e. without any applied tags) role execution 
the Raspberry Pi host should be restarted.
It's necessary to load all modules required by HiFiberry DAC+. 

License
-------

GPLv3

References
------------------
* [YAML](http://www.yaml.org/spec/1.2/spec.html)
* [Ansible](http://www.ansible.com/home)
* [Ansible Galaxy](https://galaxy.ansible.com/)
* [The test stand of this playbook](https://drive.google.com/open?id=0BzNoFr6FEfkPdzFrWGtoRTRscGc) :smile:
