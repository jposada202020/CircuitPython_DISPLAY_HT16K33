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
import time
from vectorio import Polygon, Circle
import displayio

try:
    from typing import Optional, Dict, Tuple, Union
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_DISPLAY_HT16K33.git"


# fmt: off
CHARS = (
    0b00000000, 0b00000000,  #
    0b01000000, 0b00000110,  # !
    0b00000010, 0b00100000,  # "
    0b00010010, 0b11001110,  # #
    0b00010010, 0b11101101,  # $
    0b00001100, 0b00100100,  # %
    0b00100011, 0b01011101,  # &
    0b00000100, 0b00000000,  # '
    0b00100100, 0b00000000,  # (
    0b00001001, 0b00000000,  # )
    0b00111111, 0b11000000,  # *
    0b00010010, 0b11000000,  # +
    0b00001000, 0b00000000,  # ,
    0b00000000, 0b11000000,  # -
    0b00000000, 0b00000000,  # .
    0b00001100, 0b00000000,  # /
    0b00001100, 0b00111111,  # 0
    0b00000000, 0b00000110,  # 1
    0b00000000, 0b11011011,  # 2
    0b00000000, 0b10001111,  # 3
    0b00000000, 0b11100110,  # 4
    0b00100000, 0b01101001,  # 5
    0b00000000, 0b11111101,  # 6
    0b00000000, 0b00000111,  # 7
    0b00000000, 0b11111111,  # 8
    0b00000000, 0b11101111,  # 9
    0b00010010, 0b00000000,  # :
    0b00001010, 0b00000000,  # ;
    0b00100100, 0b01000000,  # <
    0b00000000, 0b11001000,  # =
    0b00001001, 0b10000000,  # >
    0b01100000, 0b10100011,  # ?
    0b00000010, 0b10111011,  # @
    0b00000000, 0b11110111,  # A
    0b00010010, 0b10001111,  # B
    0b00000000, 0b00111001,  # C
    0b00010010, 0b00001111,  # D
    0b00000000, 0b11111001,  # E
    0b00000000, 0b01110001,  # F
    0b00000000, 0b10111101,  # G
    0b00000000, 0b11110110,  # H
    0b00010010, 0b00000000,  # I
    0b00000000, 0b00011110,  # J
    0b00100100, 0b01110000,  # K
    0b00000000, 0b00111000,  # L
    0b00000101, 0b00110110,  # M
    0b00100001, 0b00110110,  # N
    0b00000000, 0b00111111,  # O
    0b00000000, 0b11110011,  # P
    0b00100000, 0b00111111,  # Q
    0b00100000, 0b11110011,  # R
    0b00000000, 0b11101101,  # S
    0b00010010, 0b00000001,  # T
    0b00000000, 0b00111110,  # U
    0b00001100, 0b00110000,  # V
    0b00101000, 0b00110110,  # W
    0b00101101, 0b00000000,  # X
    0b00010101, 0b00000000,  # Y
    0b00001100, 0b00001001,  # Z
    0b00000000, 0b00111001,  # [
    0b00100001, 0b00000000,  # \
    0b00000000, 0b00001111,  # ]
    0b00001100, 0b00000011,  # ^
    0b00000000, 0b00001000,  # _
    0b00000001, 0b00000000,  # `
    0b00010000, 0b01011000,  # a
    0b00100000, 0b01111000,  # b
    0b00000000, 0b11011000,  # c
    0b00001000, 0b10001110,  # d
    0b00001000, 0b01011000,  # e
    0b00000000, 0b01110001,  # f
    0b00000100, 0b10001110,  # g
    0b00010000, 0b01110000,  # h
    0b00010000, 0b00000000,  # i
    0b00000000, 0b00001110,  # j
    0b00110110, 0b00000000,  # k
    0b00000000, 0b00110000,  # l
    0b00010000, 0b11010100,  # m
    0b00010000, 0b01010000,  # n
    0b00000000, 0b11011100,  # o
    0b00000001, 0b01110000,  # p
    0b00000100, 0b10000110,  # q
    0b00000000, 0b01010000,  # r
    0b00100000, 0b10001000,  # s
    0b00000000, 0b01111000,  # t
    0b00000000, 0b00011100,  # u
    0b00100000, 0b00000100,  # v
    0b00101000, 0b00010100,  # w
    0b00101000, 0b11000000,  # x
    0b00100000, 0b00001100,  # y
    0b00001000, 0b01001000,  # z
    0b00001001, 0b01001001,  # {
    0b00010010, 0b00000000,  # |
    0b00100100, 0b10001001,  # }
    0b00000101, 0b00100000,  # ~
    0b00111111, 0b11111111,
)
# fmt: on

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
    Main class to display the 7x4 segments on the screen

    :param int x: x coordinates in pixels for the segment to start. This is the top
     left corner of the first digit
    :param int y: y coordinates in pixels for the segment to start. This is the top
     left corner of the first digit

    :param int height: segment height in pixels. Defaults to :const:`40` pixels
    :param int length: segment length in pixels. Defaults to :const:`40` pixels
    :param int stroke: segment width in pixels. Defaults to :const:`4` pixels

    :param int|tuple color_off: (*RGB tuple or 24-bit hex value*) segment fill color
     when segment is on. Defaults to :const:`0x123456` Blue.
    :param int|tuple color_on: (*RGB tuple or 24-bit hex value*) segment fill color
     when segment is on. Defaults to :const:`0xFF5500` orange.

    :param dict char_dict: An optional dictionary mapping strings to bit settings
     integers used for defining how to display custom letters

    """

    def __init__(
        self,
        x: int,
        y: int,
        height: int = 40,
        length: int = 40,
        space: int = 70,
        stroke: int = 4,
        color_off: Union[int, Tuple] = 0x123456,
        color_on: Union[int, Tuple] = 0xFF5500,
        char_dict: Optional[Dict[str, int]] = None,
    ) -> None:
        self._x = x
        self.y = y

        self._digits = [None, None, None, None]
        self._two_points_container = []
        self._colon = False

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

    def _draw_two_points(self) -> None:
        """
        Internal function to draw the two points hour indicators
        """
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

    def _draw_digits(self, x: int, pos: int) -> None:
        """
        Internal function to draw the segments

        :param int x: digits x distance in pixels
        :param int pos: digit's position

        """
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

    def print(self, value: Union[int, str]) -> None:
        """
        Print the value given. Only work with strings

        :param int|str value: String to be put in the 7x4 segment
        """
        self.clear()
        if isinstance(value, int):
            value = str(value)
        if ":" in value:
            value = value.replace(":", "")
            self._two_points(True)

        value_string = str(value)
        for i in range(len(value_string)):
            self.print_digit(i, value_string[len(value_string) - 1 - i])

    def print_digit(self, pos: int, char: str) -> None:
        """
        Print a specific digit

        :param int pos: position in the 7x4 segment
        :param str char: character to be printed

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
        elif char == " ":
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

    def set_digit_raw(self, pos, value):

        new_value = value & 0x7F

        for i in range(7):

            biff = new_value >> i & 1

            if biff:
                self._digits[pos][i].color_index = 2
            else:
                self._digits[pos][i].color_index = 1

    def clear(self) -> None:
        """
        Clear the digits
        """
        for i in range(4):
            self.print_digit(i, "*")
        self._two_points(False)

    def __setitem__(self, key: int, value: str) -> None:
        self.print_digit(key, value)

    def _two_points(self, show: bool = True):
        if show:
            for i in range(2):
                self._two_points_container[i].color_index = 2
        else:
            for i in range(2):
                self._two_points_container[i].color_index = 1

    def fill(self, value: int) -> None:
        """
        Fill function. to be compatible with the Hardware version
        of the library
        """
        if value:
            pass
        self.clear()

    @property
    def colon(self):
        return self._colon

    @colon.setter
    def colon(self, value: bool):
        self._two_points(value)

    def marquee(self, text: str, delay: float = 0.25, loop: bool = True) -> None:
        """
        Automatically scroll the text at the specified delay between characters

        :param str text: Text to display
        :param float delay: Delay in seconds to pause before scrolling to the next
         character. Defaults to 0.25 seconds
        :param bool loop: Whether to endlessly loop the text. Defaults to `True`

        """

        def cycle(text, delay):
            for i in range(len(text)):
                self.print(text[i : 4 + i])
                time.sleep(delay)

        text = text + " " * 4

        if loop:
            while True:
                cycle(text, delay)
        else:
            cycle(text, delay)

class SEG14x4:
    """
    Main class to display the 14x4 segments on the screen

    :param int x: x coordinates in pixels for the segment to start. This is the top left
     corner of the first digit
    :param int y: y coordinates in pixels for the segment to start. This is the top left
     corner of the first digit

    :param int height: segment height in pixels. Defaults to :const:`40` pixels
    :param int length: segment length in pixels. Defaults to :const:`40` pixels
    :param int stroke: segment width in pixels. Defaults to :const:`4` pixels

    :param int|tuple color_off: (*RGB tuple or 24-bit hex value*) segment fill color when segment
     is on. Defaults to :const:`0x123456` Blue.
    :param int|tuple color_on: (*RGB tuple or 24-bit hex value*) segment fill color when segment
     is on. Defaults to :const:`0xFF5500` orange.

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
        self._digits_high = [None, None, None, None]
        self._two_points_container = []

        self._chardict = char_dict
        self.buffer = [None, None, None, None]
        self.value_string = None

        self.group = displayio.Group()

        self._palette = displayio.Palette(3)
        self._palette.make_transparent(0)
        self._palette[1] = color_off
        self._palette[2] = color_on
        self._stroke = stroke
        self._length = length
        self._height = height
        self._space = space

        self._index = 0
        self._delay = 0.25
        self._last_nb_scroll_time = -1
        self.marquee_text = None
        self.loop = True

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
        xfinal = self._length // 2 - 2 * self._stroke
        yfinal = -self._height + 2 * stroke
        self._pointsd_right_bot = [
            (0, 0),
            (0, -2 * self._stroke),
            (
                xfinal - self._stroke,
                yfinal,
            ),
            (xfinal, yfinal),
            (
                xfinal,
                yfinal + self._stroke,
            ),
            (self._stroke, 0),
        ]

        self._pointsd_left_bot = [
            (0, 0),
            (0, -2 * self._stroke),
            (
                -xfinal + self._stroke,
                yfinal,
            ),
            (-xfinal + self._stroke // 2, yfinal),
            (
                -xfinal + self._stroke // 2,
                yfinal + self._stroke,
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
        """
        Internal function to draw the segments

        :param int x: digits x distance in pixels
        :param int pos: digit's position

        """
        posx = x

        segments = []
        segments_high = []

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

        segments_high.append(value)
        self.group.append(value)

        # Segment J
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsv_half,
            x=posx + self._length // 2,
            y=self.y + self._stroke // 2,
            color_index=1,
        )

        segments_high.append(value)
        self.group.append(value)

        # Segment K
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsd_left_up,
            x=posx + self._length - self._stroke - self._stroke // 2,
            y=self.y + self._stroke,
            color_index=1,
        )

        segments_high.append(value)
        self.group.append(value)

        # Segment L
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsd_right_bot,
            x=posx + self._stroke,
            y=self.y + self._height * 2 - self._stroke,
            color_index=1,
        )

        segments_high.append(value)
        self.group.append(value)

        # Segment M
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsv_half,
            x=posx + self._length // 2,
            y=self.y + self._height + self._stroke // 2,
            color_index=1,
        )

        segments_high.append(value)
        self.group.append(value)

        # Segment N
        value = Polygon(
            pixel_shader=self._palette,
            points=self._pointsd_left_bot,
            x=posx + self._length - self._stroke - self._stroke // 2,
            y=self.y + self._height * 2 - self._stroke,
            color_index=1,
        )

        segments_high.append(value)
        self.group.append(value)

        self._digits[pos] = segments
        self._digits_high[pos] = segments_high

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
        """
        Internal function to draw the two points hour indicators
        """
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

    def print_digit(self, pos, char):
        """
        Print a specific digit
        """
        character = ord(char) * 2 - 64
        if char == "*":
            character = 37

        new_value_high = CHARS[character]
        new_value_low = CHARS[character + 1]

        for i in range(8):
            biff_low = new_value_low >> i & 1

            if biff_low:
                self._digits[pos][i].color_index = 2
            else:
                self._digits[pos][i].color_index = 1

        for i in range(6):
            biff_high = new_value_high >> i & 1
            if biff_high:
                self._digits_high[pos][i].color_index = 2
            else:
                self._digits_high[pos][i].color_index = 1

    def print(self, value):
        """
        Print the value given. Only work with strings

        :param str value: String to be put in the 7x4 segment
        """
        self.clear()
        if ":" in value:
            value = value.replace(":", "")
            self._two_points(True)

        self.value_string = str(value)

        for i in range(len(self.value_string)):
            self.print_digit(i, self.value_string[len(self.value_string) - 1 - i])

    def clear(self):
        """
        Clear the digits
        """
        for i in range(4):
            self.print_digit(i, ".")
        self._two_points(False)

    def __setitem__(self, key: int, value: str) -> None:
        self.print_digit(key, value)

    def scroll(self, count: int = 1) -> None:
        """Scroll the display by specified number of places.

        :param int count: The number of places to scroll
        """
        self.clear()

        for i in range(len(self.value_string)):
            if i + count > 3:
                pass
            else:
                self.print_digit(
                    i + count, self.value_string[len(self.value_string) - 1 - i]
                )

    def marquee(self, text: str, delay: float = 0.25, loop: bool = True) -> None:
        """
        Automatically scroll the text at the specified delay between characters

        :param str text: Text to display
        :param float delay: Delay in seconds to pause before scrolling to the next
         character. Defaults to 0.25 seconds
        :param bool loop: Whether to endlessly loop the text. Defaults to `True`

        """

        def cycle(text, delay):
            for i in range(len(text)):
                self.print(text[i : 4 + i])
                time.sleep(delay)

        text = text + " " * 4

        if loop:
            while True:
                cycle(text, delay)
        else:
            cycle(text, delay)

    def non_blocking_marquee(
        self, text: str, delay: float = 0.25, loop: bool = True
    ) -> None:
        """
        Non Blocking Marquee Definition function

        :param str text: Text to display
        :param float delay: Delay in seconds to pause before scrolling to the next
         character. Defaults to 0.25 seconds
        :param bool loop: Whether to endlessly loop the text. Defaults to `True`
        """

        self.marquee_text = text + " " * 4
        self.loop = loop
        self._index = 0
        self._delay = delay

    def non_blocking_marquee_update(self):
        """
        Non Blocking Marquee update function
        """
        if self.loop:
            now = time.monotonic()
            if now >= self._last_nb_scroll_time + self._delay:
                self._last_nb_scroll_time = now
                self.print(self.marquee_text[self._index : 4 + self._index])
                self._index = self._index + 1
            if self._index > len(self.marquee_text) - 4:
                self._index = 0
