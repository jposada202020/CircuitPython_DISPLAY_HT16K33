# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import board
import adafruit_framebuf
from display_ht16k33 import matrix


# col = 16
col = 8

if col == 16:
    matrix = matrix.Matrix16x8(50, 60, 8, True)
else:
    matrix = matrix.Matrix8x8(50, 60, 8, True)

display = board.DISPLAY
display.show(matrix.group)

buf = bytearray(col)
fb = adafruit_framebuf.FrameBuffer(buf, col, 16, adafruit_framebuf.MVLSB)

fb.line(0, 0, 0, 7, 0xFFFFFF)
fb.line(col - 1, 0, col - 1, 7, 0xFF0000)
fb.line(0, 7, col - 1, 7, 0xFF0000)
fb.line(0, 0, col - 1, 0, 0xFF0000)

fb.rect(col // 2 - 2, 3, 3, 3, 0xFF0000)
fb.rect(col // 2 + 1, 1, 2, 2, 0xFF0000)

for x in range(col):
    bite = buf[x]
    for y in range(8):
        bit = 1 << y & bite
        if bit:
            matrix[col - x - 1, y] = 1
