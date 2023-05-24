# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`display_ht16k33.ht16k33`
================================================================================

On Display Simulation for an HT16K33 driver. Works with 16x8 and 8x8 matrices.

Based on some code from https://github.com/adafruit/Adafruit_CircuitPython_HT16K33.git
Authors: Radomir Dopieralski and Tony DiCola License: MIT

* Author(s): Jose D. Montoya


"""

import time
from vectorio import Circle
import displayio
import ulab.numpy as np


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_DISPLAY_HT16K33.git"


class HT16K33:
    """ """
    def __init__(
        self,
        num_led_x: int = 16,
        num_led_y: int = 8,
        register_width: int = 2,
    ) -> None:
        self.cols = num_led_x
        self.rows = num_led_y

        self.bit_mask = ((1 << self.cols) - 1) << 0

        self.buffer_rows = []
        for _ in range(self.rows):
            self.buffer_rows.append(bytearray(register_width))

        self.buffer = bytearray(register_width)
        self.array = np.ndarray(np.empty((self.rows, self.cols)), dtype=np.uint8)

        self.length = register_width

        self.group = displayio.Group()

        palette = displayio.Palette(3)
        palette[0] = 0x123456
        palette[1] = 0x00000
        palette[2] = 0xFF5500

        self.matrix = []
        for j in range(1, self.rows +1):
            row_buff = []
            for coord_x in range(1, self.cols +1):
                value = Circle(pixel_shader=palette, radius=10, x=coord_x * 25, y=j * 25, color_index=1)
                row_buff.append(value)
                self.group.append(value)
            self.matrix.append(row_buff)

    @property
    def value(self) -> bytearray:
        return self.buffer

    def set(self, y, new_value: int) -> None:
        reg = 0

        if self.length == 2:
            order = range(self.length - 1, 0, -1)
        if self.length ==1:
            order = range(0,1)

        for ind in order:
            reg = (reg << 8) | self.buffer_rows[y][ind]

        reg &= ~self.bit_mask
        reg |= new_value

        for ind2 in order:
            self.buffer_rows[y][ind2] = reg & 0xFF
            reg >>= 8

        self.convert_to_leds(y)
        self.update(y)

    def pixel(self, x, y, color=True):
        reg = 0
        order = range(0, len(self.buffer))

        for i in order:
            reg = (reg << 8) | self.buffer_rows[y][i]

        mask = 1 << x

        if color:
            buff = reg | mask
        else:
            buff = reg & ~mask
        for i in reversed(order):
            self.buffer_rows[y][i] = buff & 0xFF
            buff >>= 8
        self.convert_to_leds(y)
        self.update(y)

    def convert_to_leds(self, y) -> None:
        """
        :return:
        """
        index = 0
        for i in range(0, self.length):
            val = self.buffer_rows[y][i]
            for j in range(7, -1, -1):
                buffval = val >> j & 1
                self.array[y][index] = buffval
                index = index + 1

    def update(self,y):
        for i, ele in enumerate(self.matrix[y]):
            if self.array[y][i]:
                self.matrix[y][i].color_index = 2
            else:
                self.matrix[y][i].color_index = 1

    def update_all(self):
        for row in range(self.rows):
            self.update(row)

    def shift(self, x: int, y: int, rotate: bool = True) -> None:
        """
        Shift Matrix by x and y

        :param int x: pixel x coordinate
        :param int y: pixel x coordinate
        """
        self.array = np.roll(self.array, y, axis=0)
        self.array = np.roll(self.array, x, axis=1)

        self.update_all()

    def shift_right(self, rotate: bool = False) -> None:
        """
        Shift all pixels right

        :param rotate: (Optional) Rotate the shifted pixels to the left side (default=False)
        """
        self.shift(1, 0, rotate)

    def shift_left(self, rotate: bool = False) -> None:
        """
        Shift all pixels left

        :param rotate: (Optional) Rotate the shifted pixels to the right side (default=False)
        """
        self.shift(-1, 0, rotate)

    def shift_up(self, rotate: bool = False) -> None:
        """
        Shift all pixels up

        :param rotate: (Optional) Rotate the shifted pixels to bottom (default=False)
        """
        self.shift(0, 1, rotate)

    def shift_down(self, rotate: bool = False) -> None:
        """
        Shift all pixels down

        :param rotate: (Optional) Rotate the shifted pixels to top (default=False)
        """
        self.shift(0, -1, rotate)
