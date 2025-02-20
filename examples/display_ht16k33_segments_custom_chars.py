# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

# Copied and adapted in ht16k33_segments_7x4customchars.pyexample
# for the Adafruit_ht16k33 library here:
# https://github.com/adafruit/Adafruit_CircuitPython_HT16K33/blob/main/examples/ht16k33_segments_7x4customchars.py

import board
from display_ht16k33.segments import SEG7x4

display = board.DISPLAY

custom_chars = {}

# Add the custom characters you want
custom_chars["s"] = 0b01101101
custom_chars["r"] = 0b01010000
custom_chars["o"] = 0b00111111
custom_chars["l"] = 0b00110000
custom_chars["i"] = 0b00010000
custom_chars["n"] = 0b01010100
custom_chars["g"] = 0b01101111

my_segment = SEG7x4(40, 40, char_dict=custom_chars)

display.root_group = my_segment.group
my_segment.print("sing")
