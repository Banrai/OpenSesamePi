#!/usr/bin/env python

"""
This file defines the configuration settings for doorchecker.py
change them according to your environment, or use a local_settings.py
file which is excluded from source control.

"""

DOOR_PIN   = 17
SLEEP_TIME = 2.0

NOTIFY_LIST = ['me@example.org', 'you@example.com']

# Override any of the above settings for your local environment in a
# separate local_settings.py file which is *not* checked into  source
# control

try:
    from local_settings import *
except ImportError:
    pass
