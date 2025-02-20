# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

# Copied and adapted in ht16k33_matrix_simpletest.py example for the Adafruit_ht16k33 library here:

import time
import board
import displayio
from display_ht16k33.matrix import Matrix8x8
from display_ht16k33.segments import SEG7x4, SEG14x4


display = board.DISPLAY
general_group = displayio.Group()
my_matrix = Matrix8x8(30, 25, 5, False)
my_segment2 = SEG14x4(30, 150, color_on=0x40B080, color_off=0x121212)
my_segment = SEG7x4(150, 40, height=20, length=20, space=35, color_on=0x00FF10)

general_group.append(my_matrix.group)
general_group.append(my_segment2.group)
general_group.append(my_segment.group)
display.root_group = general_group

for row in range(2, 6):
    my_matrix[row, 0] = 1
    my_matrix[row, 7] = 1

for column in range(2, 6):
    my_matrix[0, column] = 1
    my_matrix[7, column] = 1

my_matrix[1, 1] = 1
my_matrix[1, 6] = 1
my_matrix[6, 1] = 1
my_matrix[6, 6] = 1
my_matrix[2, 5] = 1
my_matrix[5, 5] = 1
my_matrix[2, 3] = 1
my_matrix[5, 3] = 1
my_matrix[3, 2] = 1
my_matrix[4, 2] = 1

my_segment2.non_blocking_marquee("   This is an example", delay=0.35, loop=True)

# Move the Smiley Face Around
while True:
    for frame in range(0, 8):
        my_matrix.shift_right(True)
        time.sleep(0.05)
    my_segment.print(1111)
    my_segment2.non_blocking_marquee_update()
    for frame in range(0, 8):
        my_matrix.shift_down(True)
        time.sleep(0.05)
    my_segment.print(2222)
    my_segment2.non_blocking_marquee_update()
    for frame in range(0, 8):
        my_matrix.shift_left(True)
        time.sleep(0.05)
    my_segment.print(3333)
    my_segment2.non_blocking_marquee_update()
    for frame in range(0, 8):
        my_matrix.shift_up(True)
        time.sleep(0.05)
    my_segment.print(4444)
    my_segment2.non_blocking_marquee_update()
