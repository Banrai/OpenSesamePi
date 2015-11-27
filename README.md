# OpenSesamePi

## About

Get notified any time your door is opened and closed.

Connect a [reed switch](https://en.wikipedia.org/wiki/Reed_switch) to your door, wire the leads into the [Raspberry Pi's'](http://www.raspberrypi.org/) [GPIO pins](http://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/) to complete the circuit, and get email alerts.



## Installation

### Physical

1. Create a circuit connecting the reed switch leads to the Pi's GPIO pins

  In addition to the switch itself, you will need a single 330 ohm resistor, as shown here:

  ![Circuit schematic](schematic/RPi Reed Switch.png?raw=true "Circuit schematic")

  ![Breadboard test](http://i.imgur.com/KggrWfL.jpg "Breadboard test")

2. Install the reed switch on the door (make sure the door opens cleanly with the switch in place)

  ![Reed switch on door](http://i.imgur.com/fNtReLQ.jpg "Reed switch on door")

3. Final assembly, with resistor connected and plugged in to the GPIO pins on the Pi:

  ![Final assembly](http://i.imgur.com/2B7Ax0h.jpg "Final assembly")

  In addition to running [OpenSesamePi](https://github.com/Banrai/OpenSesamePi), this particular Pi is doing double duty as a [PiScan](http://imgur.com/a/dXNYW) implementation.

### Software

1. Login to the Pi and install this Software:

  ```sh 
git clone git@github.com:Banrai/OpenSesamePi.git
```

2. Configure the Pi to send email:

  ```sh 
sudo apt-get update
sudo apt-get -y install ssmtp mailutils
```

  Then edit the <tt>SSMTP</tt> configuration file:

  ```sh 
sudo vi /etc/ssmtp/ssmtp.conf
```

  You need these lines defined at a minimum, replacing the [gmail](https://gmail.com/) coordinates with your own. You can of course use any other SMTP mailserver of your choice:

  ```sh 
root=postmaster
mailhub=smtp.gmail.com:587
hostname=raspberrypi
AuthUser=YourGMailUserName@gmail.com
AuthPass=YourGMailPassword
UseSTARTTLS=YES
```

  Note that if you do use gmail, you will also need to update the [Allow less secure apps](https://www.google.com/settings/security/lesssecureapps) setting for this method to work.

3. Define the list of email addresses that should get the opened/closed alerts

  Create a new file called <tt>local_settings.py</tt> in the same folder where you cloned this repo (by default, it will be the <tt>/home/pi/OpenSesamePi/</tt> folder), add a line like this, and save the file:

  ```python
NOTIFY_LIST = ['me@myemail.com', 'myroommate@theiremail.com']
```

  Each of the email addresses defined here will get an email alert when the [DoorChecker](DoorChecker.py) script is triggered.

  This file overrides the <tt>NOTIFY_LIST</tt> defined in the generic [settings.py](settings.py) file.

4. Have the [DoorChecker](DoorChecker.py) script start automatically, every time the Pi does:

  ```sh 
sudo crontab -e
```

  Then add this line at the bottom, and save the file:

  ```sh 
@reboot python /home/pi/OpenSesamePi/DoorChecker.py &
```

## Extensibility

At the moment, the [DoorChecker](DoorChecker.py) script's [notification action](DoorChecker.py#L36) is to send email, but that can be extended to triggering an alarm, taking a camera snapshot, etc.

Just change the implementation of the [notify(door_state)](DoorChecker.py#L36) function to something more elaborate.

## Acknowledgements

* [A circuit for the Raspberry Pi to use the Reed Switch](http://rocode.com/sensors/#ReedSwitch)
* [Sending emails from the Raspberry Pi](http://iqjar.com/jar/sending-emails-from-the-raspberry-pi/)
* [My door sends me emails](https://blog.haschek.at/post/fb64f)
* [Fritzing](http://fritzing.org/) for their awesome [desktop application](https://github.com/fritzing/fritzing-app) 
