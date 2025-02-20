# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""This example demonstrates the use of the display_ht16k33 library to display a pixelit image on a 8x8 matrix
To get some pixelit images you can go to the following address https://pixelit-project.github.io/PixelIt/webui/#/gallery
and copu the code for the bitmap. You can also create your own images and get the code for the bitmap.
"""

import board
from display_ht16k33 import matrix

display = board.DISPLAY
matrix = matrix.Matrix8x8()

display.root_group = matrix.group

# pixelit_example = [0,0,34192,34192,34192,34192,0,0,0,34192,65535,34192,34192,65535,34192,0,0,0,34192,34192,34192,34192,0,0,34192,34192,0,34192,34192,0,34192,34192,0,0,34192,53241,53241,34192,0,0,34192,34192,34192,53241,53241,34192,34192,34192,0,0,34192,34192,34192,34192,0,0,34192,34192,0,0,0,0,34192,34192]
# pixelit_example = [0,0,65504,65504,65504,64512,0,0,0,65504,65504,65504,65504,65504,64512,0,65504,65504,0,65504,65504,0,65504,64512,65504,65504,0,65504,65504,0,65504,64512,65504,65504,65504,65504,65504,65504,65504,64512,65504,65504,0,0,0,0,65504,64512,0,65504,65504,65504,65504,65504,64512,0,0,0,65504,65504,65504,64512,0,0]

# display the pixelit image
matrix.pixelit_helper(pixelit_example)
