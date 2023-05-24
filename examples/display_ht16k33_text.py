# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

# Copied and adapted in ht16k33_matrix_text.py example for the Adafruit_ht16k33 library here:

import board
import adafruit_framebuf
from display_ht16k33 import matrix

matrix = matrix.Matrix16x8()
display = board.DISPLAY
display.show(matrix.group)

buf = bytearray(16)
text_to_show = "Hello :)"
fb = adafruit_framebuf.FrameBuffer(buf, 16, 8, adafruit_framebuf.MVLSB)


while True:
    for i in range(len(text_to_show) * 8):
        fb.fill(0)
        fb.text(text_to_show, -i + 16, 0, color=1)
        matrix.fill(0)
        for x in range(16):
            bite = buf[x]
            for y in range(8):
                bit = 1 << y & bite
                if bit:
                    matrix[16 - x, y + 1] = 1
