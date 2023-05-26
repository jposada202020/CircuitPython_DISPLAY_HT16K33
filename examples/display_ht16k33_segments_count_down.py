# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
from display_ht16k33.segments import SEG7x4

display = board.DISPLAY

my_segment = SEG7x4(40, 40)

display.show(my_segment.group)

for i in range(100, 0, -1):
    my_segment.print(i)
    time.sleep(1)
