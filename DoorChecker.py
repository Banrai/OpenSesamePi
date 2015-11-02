#!/usr/bin/env python

"""
DoorChecker.py

This is primary reed switch checking logic, designed to detect when the
switch (door) is opened or closed, and to react accordingly.

The GPIO pin corresponding to the switch attached to the door, which is
defined in the corresponding settings.py file.

"""

from settings import DOOR_PIN, SLEEP_TIME, NOTIFY_LIST

import time
from datetime import datetime
import subprocess
from string import Template

#
# Notification by email

def current_date (fmt="%a %d-%m-%Y @ %H:%M:%S"):
    """Return the current time and date as a string, 
       for the email notification message.

       The default format returns a string like this:
       'Sun 01-11-2015 @ 14:50:50'
    """       

    return datetime.strftime(datetime.now(), fmt)

NOTIFY_CMD = Template("""echo "$date door $state" | mail -s "Pi: door $state" $email""")

def notify (door_state):
    """Send each of the email addresses in NOTIFY_LIST a message"""

    for email in NOTIFY_LIST:
        shell_cmd = NOTIFY_CMD.substitute(date=current_date(),
                                          state=door_state,
                                          email=email)
        proc = subprocess.Popen(shell_cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout_value, stderr_value = proc.communicate()


#
# GPIO logic

import RPi.GPIO as io
io.setmode(io.BCM)

io.setup(DOOR_PIN, io.IN,
         pull_up_down=io.PUD_UP) # activate the reed input with PullUp

STATES = {
    'current': 'closed',
    'prior'  : 'closed'
}

while True:
    if io.input(DOOR_PIN):
        # door is closed
        STATES['current'] = 'closed'
        if STATES['prior'] == 'opened':
            STATES['prior'] = 'closed'
            notify('closed')
    else:
        # door is open
        STATES['current'] = 'opened'
        if STATES['prior'] == 'closed':
            STATES['prior'] = 'opened'
            notify('opened')
        
    time.sleep(SLEEP_TIME)
