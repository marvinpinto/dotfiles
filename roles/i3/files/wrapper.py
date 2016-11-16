#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script is a simple wrapper which prefixes each i3status line with custom
# information. It is a python reimplementation of:
# http://code.stapelberg.de/git/i3status/tree/contrib/wrapper.pl
#
# To use it, ensure your ~/.i3status.conf contains this line:
#     output_format = "i3bar"
# in the 'general' section.
# Then, in your ~/.i3/config, use:
#     status_command i3status | ~/i3status/contrib/wrapper.py
# In the 'bar' section.

import sys
import json
import os
import time
from datetime import datetime

TWO_DAYS = 172800  # seconds
COLORS = {
  'GOOD': '#00FF00',
  'DEGRADED': '#FFFF00',
  'BAD': '#FF0000'
}

backup_status_file = "/tmp/backup-timestamp.txt"

def get_backup_status():
    """ Get the status of the Amazon Cloud Drive backup status. """
    backup_status = {
      'name': 'backups'
    }

    try:
      last_backup_time = os.path.getmtime(backup_status_file)
    except OSError:
      backup_status['full_text'] = "Backups: ERROR"
      backup_status['color'] = COLORS['BAD']
      return backup_status

    backup_str = "Backups: %s" % datetime.fromtimestamp(last_backup_time).strftime("%Y-%m-%d")
    current_time = int(time.time())
    datetime.fromtimestamp(last_backup_time).strftime("%Y-%m-%d")

    if ((current_time - last_backup_time) >= TWO_DAYS):
      backup_status['full_text'] = backup_str
      backup_status['color'] = COLORS['DEGRADED']
      return backup_status

    backup_status['full_text'] = backup_str
    backup_status['color'] = COLORS['GOOD']
    return backup_status


def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()


def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    while True:
        line, prefix = read_line(), ''
        # ignore comma at start of lines
        if line.startswith(','):
            line, prefix = line[1:], ','

        j = json.loads(line)
        j.insert(1, get_backup_status())
        print_line(prefix+json.dumps(j))