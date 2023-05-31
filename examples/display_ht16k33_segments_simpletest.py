# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
# Copied and adapted from the examples in the
# Adafruit_ht16k33 library here:
# https://github.com/adafruit/Adafruit_CircuitPython_HT16K33

import time
import board
from display_ht16k33.segments import SEG7x4

display = board.DISPLAY

my_segment = SEG7x4(40, 40)

display.show(my_segment.group)

# Clear the display.
my_segment.fill(0)

# Can just print a number
my_segment.print(42)
time.sleep(2)

# Or, print the time
my_segment.print("12:30")
time.sleep(2)

my_segment.colon = False

# Or, can set indivdual digits / characters
# Set the first character to '1':
my_segment[0] = "1"
# Set the second character to '2':
my_segment[1] = "2"
# Set the third character to 'A':
my_segment[2] = "A"
# Set the forth character to 'B':
my_segment[3] = "B"
time.sleep(2)

# Or, can even set the segments to make up characters
if isinstance(my_segment, SEG7x4):
    # 7-segment raw digits
    my_segment.set_digit_raw(0, 0xFF)
    my_segment.set_digit_raw(1, 0b11111111)
    my_segment.set_digit_raw(2, 0x79)
    my_segment.set_digit_raw(3, 0b01111001)
