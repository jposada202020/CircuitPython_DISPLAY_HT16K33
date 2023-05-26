# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import board
from display_ht16k33.segments import SEG7x4

display = board.DISPLAY

my_segment = SEG7x4(40, 40)

display.show(my_segment.group)

my_segment.print(1234)
