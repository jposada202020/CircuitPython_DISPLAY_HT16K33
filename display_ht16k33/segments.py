# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`display_ht16k33.segments`
================================================================================

On Display Simulation for an HT16K33 driver. Works with 7x4 Segments.

Based on some code from https://github.com/adafruit/Adafruit_CircuitPython_HT16K33.git
Authors: Radomir Dopieralski and Tony DiCola License: MIT

* Author(s): Jose D. Montoya


"""
from vectorio import Polygon
import displayio

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_DISPLAY_HT16K33.git"


NUMBERS = (
    0x3F,  # 0
    0x06,  # 1
    0x5B,  # 2
    0x4F,  # 3
    0x66,  # 4
    0x6D,  # 5
    0x7D,  # 6
    0x07,  # 7
    0x7F,  # 8
    0x6F,  # 9
    0x77,  # a
    0x7C,  # b
    0x39,  # C
    0x5E,  # d
    0x79,  # E
    0x71,  # F
    0x3D,  # G
    0x76,  # H
    0x30,  # I
    0x1E,  # J
    0x40,  # -
    0x38,  # L
    0x40,  # -
    0x54,  # n
    0x5C,  # o
    0x73,  # P
    0x67,  # q
    0x50,  # R
    0x6D,  # S
    0x78,  # t
    0x3E,  # U
    0x1C,  # v
    0x40,  # -
    0x40,  # -
    0x6E,  # y
    0x40,  # -
    0x40,  # -
    0x00,  # Null
)


class SEG7x4:
    """
    Main class
    """

    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:
        self._x = x
        self.y = y

        self._digits = [None, None, None, None]
        self.group = displayio.Group()

        self._palette = displayio.Palette(3)
        self._palette[0] = 0x123456
        self._palette[1] = 0x123456
        self._palette[2] = 0xFF5500
        self._stroke = 4
        self._length = 40
        self._height = 40

        self._pointsh = [
            (0, 0),
            (self._stroke, self._stroke // 2),
            (self._length - self._stroke, self._stroke // 2),
            (self._length, 0),
            (self._length - self._stroke, -self._stroke // 2),
            (self._stroke, -self._stroke // 2),
        ]

        self._pointsv = [
            (0, 0),
            (-self._stroke // 2, self._stroke),
            (-self._stroke // 2, self._height - self._stroke),
            (0, self._height),
            (self._stroke // 2, self._height - self._stroke),
            (self._stroke // 2, self._stroke),
        ]

        self._draw_digits(40, 3)
        self._draw_digits(105, 2)
        self._draw_digits(170, 1)
        self._draw_digits(235, 0)

    def _draw_digits(self, x, pos):
        posx = x

        segments = []

        # Segment A
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsh,
            x=posx,
            y=self.y,
            color_index=1,
        )
        segments.append(value)
        self.group.append(value)

        # Segment B
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsv,
            x=posx + self._length - self._stroke // 2,
            y=self.y,
            color_index=1,
        )
        segments.append(value)
        self.group.append(value)

        # Segment C
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsv,
            x=posx + self._length - self._stroke // 2,
            y=self.y + self._height,
            color_index=1,
        )
        segments.append(value)
        self.group.append(value)

        # Segment D
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsh,
            x=posx,
            y=self.y + self._length * 2,
            color_index=1,
        )
        segments.append(value)
        self.group.append(value)

        # Segment E
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsv,
            x=posx,
            y=self.y + self._height,
            color_index=1,
        )
        segments.append(value)
        self.group.append(value)

        # Segment F
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsv,
            x=posx,
            y=self.y,
            color_index=1,
        )
        segments.append(value)
        self.group.append(value)

        # Segment G
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsh,
            x=posx,
            y=self.y + self._height,
            color_index=1,
        )
        segments.append(value)
        self.group.append(value)
        self._digits[pos] = segments

        value = Circle(pixel_shader=self._palette, radius=self._height//8, x=posx+self._length + (self._height //4), y=self.y+ 2 *self._height - (self._height//8), color_index=1)
        self.group.append(value)

    def print(self, value):
        """
        print the value given. for the time being only works with ints
        """
        self.clear()
        value_string = str(value)
        for i in range(len(value_string)):
            self.print_digit(i, value_string[len(value_string) - 1 - i])

    def print_digit(self, pos, char):
        # print(ord(char))
        if char in "abcdefghijklmnopqrstuvwxy":
            character = ord(char) - 97 + 10
        elif char == "-":
            character = 36
        elif char in "0123456789":
            character = ord(char) - 48
        elif char == "*":
            character = 37

        new_value = NUMBERS[character]

        for i in range(7):
            biff = new_value >> i & 1

            if biff:
                self._digits[pos][i].color_index = 2
            else:
                self._digits[pos][i].color_index = 1

    def clear(self):
        """
        Clear the digits
        """
        for i in range(4):
            self.print_digit(i, "*")
