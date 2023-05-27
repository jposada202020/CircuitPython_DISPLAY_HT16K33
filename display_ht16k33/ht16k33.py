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
from vectorio import Circle
import displayio
import ulab.numpy as np


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_DISPLAY_HT16K33.git"


# pylint: disable=too-many-arguments, too-many-instance-attributes
class HT16K33:
    """
    Main class
    """

    def __init__(
        self,
        x,
        y,
        radius=10,
        text=False,
        num_led_x: int = 16,
        num_led_y: int = 8,
        register_width: int = 2,
    ) -> None:
        self.x = x
        self.y = y
        self.cols = num_led_x
        self.rows = num_led_y
        self.radius = radius

        self.bit_mask = ((1 << self.cols) - 1) << 0

        self.buffer_rows = []
        for _ in range(self.rows):
            self.buffer_rows.append(bytearray(register_width))

        self.buffer = bytearray(register_width)
        self.array = np.ndarray(np.empty((self.rows, self.cols)), dtype=np.uint8)

        self.length = register_width

        self.group = displayio.Group()

        palette = displayio.Palette(3)
        palette[0] = 0x2263A4
        palette[1] = 0x101010
        palette[2] = 0xFF5500

        self.matrix = []

        if text:
            y_range = range(1, self.rows + 1)
        else:
            y_range = range(self.rows + 1, 1, -1)

        for j in y_range:
            row_buff = []
            for coord_x in range(1, self.cols + 1):
                value = Circle(
                    pixel_shader=palette,
                    radius=self.radius,
                    x=self.x + coord_x * (self.radius * 2 + self.radius // 2),
                    y=self.y + j * (self.radius * 2 + self.radius // 2),
                    color_index=1,
                )
                row_buff.append(value)
                self.group.append(value)
            self.matrix.append(row_buff)

    @property
    def value(self) -> bytearray:
        """
        Value of the buffer
        """
        return self.buffer

    def set(self, y, new_value: int) -> None:
        """
        Set a particular value in an specific row defined by y
        """
        reg = 0

        order = range(0, self.length)

        for ind in order:
            reg = (reg << 8) | self.buffer_rows[y][ind]

        reg &= ~self.bit_mask
        reg |= new_value

        for ind2 in order:
            self.buffer_rows[y][ind2] = reg & 0xFF
            reg >>= 8
        self.convert_to_leds(y)

    def pixel(self, x: int, y: int, color=True) -> None:
        """
        Set a specific pixel in the matrix
        """
        reg = 0
        order = range(0, self.length)

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

    def update(self, y) -> None:
        """
        Update a particular Row
        """

        for i, _ in enumerate(self.matrix[y]):
            if self.array[y][i]:
                self.matrix[y][i].color_index = 2
            else:
                self.matrix[y][i].color_index = 1

    def update_all(self):
        """
        Update all the matrix
        """
        for row in range(self.rows):
            self.update(row)

    def shift(self, x: int, y: int, rotate: bool = True) -> None:
        """
        Shift Matrix by x and y

        :param int x: pixel x coordinate
        :param int y: pixel x coordinate
        """
        if rotate:
            pass
        self.array = np.roll(self.array, y, axis=0)
        self.array = np.roll(self.array, x, axis=1)

        self.update_all()
        # gc.collect()

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

    def fill(self, color: bool) -> None:
        """
        fill the entire matrix
        """
        if color:
            new_value = 0xFF
        else:
            new_value = 0x00
        for ele in range(self.rows):
            self.set(ele, new_value)
