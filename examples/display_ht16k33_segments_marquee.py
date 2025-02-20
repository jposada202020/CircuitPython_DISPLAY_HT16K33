# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import board
import displayio
from display_ht16k33.segments import SEG14x4

display = board.DISPLAY
group = displayio.Group()

my_segment = SEG14x4(40, 40)

group.append(my_segment.group)
display.root_group = group
my_segment.marquee("This is an example :)", delay=0.35, loop=True)
