#Author(s): Owen Walbridge, 2023 |  

import sys
import os

import time
from datetime import datetime
import re

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def current_date():
    now = datetime.now()
    current_date = str(now.strftime("%d:%m:%Y"))
    return current_date

def current_time():
    now = datetime.now()
    current_time = str(now.strftime("%H:%M:%S"))
    return current_time

def is_valid_hex_code(hex_code):
    # Regular expression pattern for a valid hex code
    hex_pattern = re.compile(r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$')
    return bool(hex_pattern.match(hex_code))