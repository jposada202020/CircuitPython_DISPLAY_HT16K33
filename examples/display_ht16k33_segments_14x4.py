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
my_segment.print("12:30")

display.show(group)
