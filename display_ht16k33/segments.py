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

from vectorio import Polygon, Circle
import displayio


try:
    from typing import Optional, Dict
except ImportError:
    pass

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

# pylint: disable=too-many-arguments, too-many-instance-attributes, too-few-public-methods


class SEG7x4:
    """
    Main class

    :param dict char_dict: An optional dictionary mapping strings to bit settings integers used
        for defining how to display custom letters
    """

    def __init__(
        self,
        x: int,
        y: int,
        height: int = 40,
        length: int = 40,
        space: int = 70,
        stroke: int = 4,
        color_off: int = 0x123456,
        color_on: int = 0xFF5500,
        char_dict: Optional[Dict[str, int]] = None,
    ) -> None:
        self._x = x
        self.y = y

        self._digits = [None, None, None, None]
        self.buffer = [None, None, None, None]
        self._two_points_container = []

        self._chardict = char_dict

        self.group = displayio.Group()

        self._palette = displayio.Palette(3)
        self._palette.make_transparent(0)
        self._palette[1] = color_off
        self._palette[2] = color_on
        self._stroke = stroke
        self._length = length
        self._height = height
        self._space = space

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

        self._draw_digits(self._x, 3)
        self._draw_digits(self._x + self._space, 2)
        self._draw_digits(self._x + self._space * 2, 1)
        self._draw_digits(self._x + self._space * 3, 0)
        self._draw_two_points()

    def _draw_two_points(self):
        value = Circle(
            pixel_shader=self._palette,
            radius=self._height // 8,
            x=self._x + self._space + self._length + (self._space - self._length) // 2,
            y=self.y + self._height // 2 - (self._height // 16),
            color_index=1,
        )
        self.group.append(value)
        self._two_points_container.append(value)
        value = Circle(
            pixel_shader=self._palette,
            radius=self._height // 8,
            x=self._x + self._space + self._length + (self._space - self._length) // 2,
            y=self.y + self._height + self._height // 2 - (self._height // 16),
            color_index=1,
        )
        self.group.append(value)
        self._two_points_container.append(value)

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

        value = Circle(
            pixel_shader=self._palette,
            radius=self._height // 8,
            x=posx + self._length + (self._height // 4),
            y=self.y + 2 * self._height - (self._height // 8),
            color_index=1,
        )
        self.group.append(value)

    def print(self, value):
        """
        print the value given. for the time being only works with ints
        """
        self.clear()
        if ":" in value:
            value = value.replace(":", "")
            self._two_points(True)

        value_string = str(value)
        for i in range(len(value_string)):
            self.print_digit(i, value_string[len(value_string) - 1 - i])

    def print_digit(self, pos, char):
        """
        Print a specific digit
        """
        char = char.lower()
        if char in "abcdefghijklmnopqrstuvwxy":
            character = ord(char) - 97 + 10
        elif char == "-":
            character = 36
        elif char in "0123456789":
            character = ord(char) - 48
        elif char == "*":
            character = 37

        if self._chardict and char in self._chardict:
            new_value = self._chardict[char]
        else:
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
        self._two_points(False)

    def __setitem__(self, key: int, value: str) -> None:
        self.print_digit(key, value)

    def _two_points(self, show=True):
        if show:
            for i in range(2):
                self._two_points_container[i].color_index = 2
        else:
            for i in range(2):
                self._two_points_container[i].color_index = 1

    def fill(self, value):
        """
        Fill function. to be compatible with the Hardware version
        of the library
        """
        if value:
            pass
        self.clear()


class SEG14x4:
    """
    Segment 14 x 4 Class
    """

    def __init__(
        self,
        x: int,
        y: int,
        height: int = 40,
        length: int = 40,
        space: int = 70,
        stroke: int = 4,
        color_off: int = 0x123456,
        color_on: int = 0xFF5500,
        char_dict: Optional[Dict[str, int]] = None,
    ) -> None:
        self._x = x
        self.y = y

        self._digits = [None, None, None, None]
        self.buffer = [None, None, None, None]
        self._two_points_container = []

        self._chardict = char_dict

        self.group = displayio.Group()

        self._palette = displayio.Palette(3)
        self._palette.make_transparent(0)
        self._palette[1] = color_off
        self._palette[2] = color_on
        self._stroke = stroke
        self._length = length
        self._height = height
        self._space = space

        self._pointsh = [
            (0, 0),
            (self._stroke, self._stroke // 2),
            (self._length - self._stroke, self._stroke // 2),
            (self._length, 0),
            (self._length - self._stroke, -self._stroke // 2),
            (self._stroke, -self._stroke // 2),
        ]

        self._pointsh_half = [
            (0, 0),
            (self._stroke, self._stroke // 2),
            (self._length // 2 - self._stroke, self._stroke // 2),
            (self._length // 2, 0),
            (self._length // 2 - self._stroke, -self._stroke // 2),
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

        self._pointsv_half = [
            (0, 0),
            (-self._stroke // 2, self._stroke),
            (-self._stroke // 2, self._height - self._stroke - self._stroke),
            (0, self._height - self._stroke),
            (self._stroke // 2, self._height - self._stroke - self._stroke),
            (self._stroke // 2, self._stroke),
        ]
        self._pointsd_right_bot = [
            (0, 0),
            (0, -2 * self._stroke),
            (
                self._length // 2 - 2 * self._stroke - self._stroke,
                -self._height + 2 * self._stroke,
            ),
            (
                self._length // 2 - 2 * self._stroke,
                -self._height + 2 * self._stroke + self._stroke,
            ),
            (self._stroke, 0),
        ]

        self._pointsd_left_bot = [
            (0, 0),
            (0, -2 * self._stroke),
            (
                -self._length // 2 + self._stroke + 2 * self._stroke,
                -self._height + 2 * self._stroke,
            ),
            (
                -self._length // 2 + 2 * self._stroke,
                -self._height + 2 * self._stroke + self._stroke,
            ),
            (-self._stroke, 0),
        ]

        self._pointsd_right_up = [
            (0, 0),
            (0, 2 * self._stroke),
            (
                self._length // 2 - 2 * self._stroke - self._stroke,
                self._height - 2 * self._stroke,
            ),
            (
                self._length // 2 - 2 * self._stroke,
                self._height - 2 * self._stroke - self._stroke,
            ),
            (self._stroke, 0),
        ]

        self._pointsd_left_up = [
            (0, 0),
            (0, 2 * self._stroke),
            (
                -self._length // 2 + 2 * self._stroke + self._stroke,
                self._height - 2 * self._stroke,
            ),
            (
                -self._length // 2 + 2 * self._stroke,
                self._height - 2 * self._stroke - self._stroke,
            ),
            (-self._stroke, 0),
        ]

        # h= height - 2 * stroke
        self._draw_digits(self._x, 3)
        self._draw_digits(self._x + self._space, 2)
        self._draw_digits(self._x + self._space * 2, 1)
        self._draw_digits(self._x + self._space * 3, 0)
        self._draw_two_points()

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

        # Segment G1
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsh_half,
            x=posx,
            y=self.y + self._height,
            color_index=1,
        )
        segments.append(value)
        self.group.append(value)

        # Segment G2
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsh_half,
            x=posx + self._length // 2,
            y=self.y + self._height,
            color_index=1,
        )

        segments.append(value)
        self.group.append(value)

        # Segment H
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsd_right_up,
            x=posx + self._stroke,
            y=self.y + self._stroke,
            color_index=1,
        )

        segments.append(value)
        self.group.append(value)

        # Segment J
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsv_half,
            x=posx + self._length // 2,
            y=self.y + self._stroke // 2,
            color_index=1,
        )

        segments.append(value)
        self.group.append(value)

        # Segment K
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsd_left_up,
            x=posx + self._length - self._stroke,
            y=self.y + self._stroke,
            color_index=1,
        )

        segments.append(value)
        self.group.append(value)

        # Segment L
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsd_right_bot,
            x=posx + self._stroke,
            y=self.y + self._height * 2 - self._stroke,
            color_index=1,
        )

        segments.append(value)
        self.group.append(value)

        # Segment M
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsv_half,
            x=posx + self._length // 2,
            y=self.y + self._height + self._stroke // 2,
            color_index=1,
        )

        segments.append(value)
        self.group.append(value)

        # Segment N
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsd_left_bot,
            x=posx + self._length - self._stroke,
            y=self.y + self._height * 2 - self._stroke,
            color_index=1,
        )

        segments.append(value)
        self.group.append(value)

        self._digits[pos] = segments

        value = Circle(
            pixel_shader=self._palette,
            radius=self._height // 8,
            x=posx + self._length + (self._height // 4),
            y=self.y + 2 * self._height - (self._height // 8),
            color_index=1,
        )
        self.group.append(value)

    def _two_points(self, show=True):
        if show:
            for i in range(2):
                self._two_points_container[i].color_index = 2
        else:
            for i in range(2):
                self._two_points_container[i].color_index = 1

    def _draw_two_points(self):
        value = Circle(
            pixel_shader=self._palette,
            radius=self._height // 8,
            x=self._x + self._space + self._length + (self._space - self._length) // 2,
            y=self.y + self._height // 2 - (self._height // 16),
            color_index=1,
        )
        self.group.append(value)
        self._two_points_container.append(value)
        value = Circle(
            pixel_shader=self._palette,
            radius=self._height // 8,
            x=self._x + self._space + self._length + (self._space - self._length) // 2,
            y=self.y + self._height + self._height // 2 - (self._height // 16),
            color_index=1,
        )
        self.group.append(value)
        self._two_points_container.append(value)
