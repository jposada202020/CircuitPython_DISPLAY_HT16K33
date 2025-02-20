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


def rgb565_to_rgb(rgb565):
    """
    Convert RGB565 color to RGB format.

    :param int rgb565: RGB565 color
    :return: Tuple of (R, G, B)
    :rtype: tuple
    """
    r = (rgb565 >> 11) & 0x1F
    g = (rgb565 >> 5) & 0x3F
    b = rgb565 & 0x1F
    # Scale the values back to 8-bit range
    r = (r << 3) | (r >> 2)
    g = (g << 2) | (g >> 4)
    b = (b << 3) | (b >> 2)
    return (r << 16) | (g << 8) | b


# pylint: disable=too-many-arguments, too-many-instance-attributes
class HT16K33:
    """
    Main class
    :param int x: x coordinates in pixels for the matrix to start. This is the top
    left corner of the first digit
    :param int y: y coordinates in pixels for the matrix to start. This is the top
    left corner of the first digit

    :param int radius: led radius in pixels. Defaults to :const:`10` pixels

    :param bool text: define if the matrix will be used to display text. For reasons
     that are beyond my understanding :). The text and pixels examples work differently.
     displaying text will use framebuffer, and it will show in a different direction. will be
     good to review a PR if you found this situation a little too much for your OCD ;)

    :param int num_led_x: Led quantity in the x direction. Although you could select a different
     value than 8 or 16, library logic is tested with these value, so unexpected
     behaviour is expected, if these values are not used
    :param int num_led_y: Led quantity in the y direction. Although you could select a different
     value than 8, library logic is tested with this value, so unexpected behaviour is expected,
     if this value is not used

    :param register_width int:register width to be used. Defaults to :const:`2`
    """

    def __init__(
        self,
        x: int,
        y: int,
        radius: int = 8,
        text: bool = False,
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
        self.array = np.ndarray(np.empty((self.rows, self.cols)), dtype=np.int16)

        self.length = register_width

        self.group = displayio.Group()

        self.palette = displayio.Palette(256)
        self.palette[0] = 0x2263A4
        self.palette[1] = 0x101010
        self.palette[2] = 0xFF5500
        self._palette_helper = [0x2263A4, 0x101010, 0xFF5500, 0x000000]

        self._palette_counter = 4

        self.matrix = []

        self._pixel_buffer = None

        if text:
            y_range = range(1, self.rows + 1)
        else:
            y_range = range(self.rows + 1, 1, -1)

        for j in y_range:
            row_buff = []
            for coord_x in range(1, self.cols + 1):
                value = Circle(
                    pixel_shader=self.palette,
                    radius=self.radius,
                    x=self.x + coord_x * (self.radius * 2 + self.radius // 2),
                    y=self.y + j * (self.radius * 2 + self.radius // 2),
                    color_index=1,
                )
                row_buff.append(value)
                self.group.append(value)
            self.matrix.append(row_buff)

    def get_color_position_in_palette(self, color):
        """
        Get the color position in the palette
        :param int color: color to be checked
        :return: color position in the palette
        :rtype: int
        """

        if color not in self._palette_helper:
            self.palette[self._palette_counter] = color
            self._palette_helper.append(color)
            color_position_in_palette = self._palette_counter
            self._palette_counter += 1
        else:
            color_position_in_palette = self._palette_helper.index(color)
        return color_position_in_palette

    @property
    def value(self) -> bytearray:
        """
        Value of the buffer
        """
        return self.buffer

    def set(self, y: int, new_value: int) -> None:
        """
        Set a particular value in a specific row defined by y

        :param int y: row number
        :param int new_value: value to be set

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

    def pixel(self, x: int, y: int, shown=True) -> None:
        """
        Set a specific pixel in the matrix
        :param int x: pixel's x coordinate in the matrix
        :param int y: pixel's y coordinate in the matrix
        :param bool color: if the pixel is to be shown or not. Defaults to shown `True`
        """
        reg = 0
        order = range(0, self.length)

        for i in order:
            reg = (reg << 8) | self.buffer_rows[y][i]

        mask = 1 << x

        if shown:
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
        Internal function to convert values to a led on and off matrix
        :param int y: y row number
        :return: None
        """
        index = 0
        for i in range(0, self.length):
            val = self.buffer_rows[y][i]
            for j in range(7, -1, -1):
                buffval = val >> j & 1
                self.array[y][index] = buffval
                index = index + 1

    def pixelit_helper(self, values: list) -> None:
        """
        Helper function to set a list of values to the matrix

        :param list values: list of values to be set
        """
        inverted_list = values[::-1]
        chunks = []

        for i in range(0, len(inverted_list), 8):
            chunks.append(inverted_list[i : i + 8])
        for y in range(8):
            for j, color in enumerate(chunks[y]):
                converted_color = rgb565_to_rgb(color)
                index_buffer = self.get_color_position_in_palette(converted_color)
                self.matrix[y][j].color_index = index_buffer

    def update(self, y: int) -> None:
        """
        Update a particular Row

        :param int y: row y number
        """
        for i, _ in enumerate(self.matrix[y]):
            if self.array[y][i]:
                self.matrix[y][i].color_index = 2
            else:
                self.matrix[y][i].color_index = 1

    def update_all(self) -> None:
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
