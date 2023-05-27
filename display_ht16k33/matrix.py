# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`display_ht16k33.matrix`
================================================================================

On Display Simulation for an HT16K33 driver. Works with 16x8 and 8x8 matrices.

Based on some code from https://github.com/adafruit/Adafruit_CircuitPython_HT16K33.git
Authors: Radomir Dopieralski and Tony DiCola License: MIT

* Author(s): Jose D. Montoya


"""

from display_ht16k33.ht16k33 import HT16K33

try:
    from typing import Optional, Tuple
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_DISPLAY_HT16K33.git"


class Matrix8x8(HT16K33):
    """A single matrix."""

    def __init__(self, x, y, radius, text):
        super().__init__(
            x=x,
            y=y,
            radius=radius,
            text=text,
            num_led_x=8,
            num_led_y=8,
            register_width=1,
        )

    def __getitem__(self, key: Tuple[int, int]) -> Optional[bool]:
        x, y = key
        return self.pixel(x, y)

    def __setitem__(self, key: Tuple[int, int], value: Optional[bool]) -> None:
        x, y = key
        self.pixel(x, y, value)


class Matrix16x8(HT16K33):
    """A single matrix."""

    def __init__(self, x, y, radius, text):

        super().__init__(
            x=x,
            y=y,
            radius=radius,
            text=text,
            num_led_x=16,
            num_led_y=8,
            register_width=2,
        )

    def __getitem__(self, key: Tuple[int, int]) -> Optional[bool]:
        x, y = key
        return self.pixel(x, y)

    def __setitem__(self, key: Tuple[int, int], value: Optional[bool]) -> None:
        x, y = key
        self.pixel(x, y, value)
