"""
Functions to manipulate an integer representing a 2x2 rubiks cube.
"""
# TODO: Documentation

from .helpers import *
from enum import Enum, IntEnum
from functools import reduce
from random import randrange, choice
import numpy as np
from .tests import verify_cube

class Man(IntEnum):
    L = 0
    F = 1
    R = 2
    B = 3
    U = 4
    D = 5


dir_map = {"L":(Man.L.value, 1), "F":(Man.F.value, 1), "R":(Man.R.value, 1), "B":(Man.B.value, 1), "U":(Man.U.value, 1), "D":(Man.D.value, 1),
           "l":(Man.L.value, -1), "f":(Man.F.value, -1), "r":(Man.R.value, -1), "b":(Man.B.value, -1), "u":(Man.U.value, -1), "d":(Man.D.value, -1)}

SIZE = (2,2)

# STRSIZE  = (SIZE[1]*3, SIZE[0]*4)
# STRLEFT  = (slice(SIZE[1],   SIZE[1]*2),   slice(0,         SIZE[0]))
# STRFRONT = (slice(SIZE[1],   SIZE[1]*2),   slice(SIZE[0],   SIZE[0]*2))
# STRRIGHT = (slice(SIZE[1],   SIZE[1]*2),   slice(SIZE[0]*2, SIZE[0]*3))
# STRBACK  = (slice(SIZE[1],   SIZE[1]*2),   slice(SIZE[0]*3, SIZE[0]*4))
# STRUP    = (slice(0,         SIZE[1]),     slice(SIZE[0],   SIZE[0]*2))
# STRDOWN  = (slice(SIZE[1]*2, SIZE[1]*3),   slice(SIZE[0],   SIZE[0]*2))



class Color(IntEnum):
    ORANGE = 0     # 0b0000
    GREEN = 1      # 0b0001
    RED = 2        # 0b0010
    YELLOW = 3     # 0b0011
    WHITE = 4      # 0b0100
    BLUE = 5       # 0b0101

class ColorValue(Enum):
    ORANGE = "\u001b[35m\u25a0\u001b[0m"  #[31;1m
    GREEN = "\u001b[32m\u25a0\u001b[0m"
    RED = "\u001b[31m\u25a0\u001b[0m"
    YELLOW = "\u001b[33m\u25a0\u001b[0m"
    WHITE = "\u001b[37m\u25a0\u001b[0m"
    BLUE = "\u001b[34m\u25a0\u001b[0m"

BIN_MAP = {Color.ORANGE: '0000', Color.GREEN: '0001', Color.RED: '0010',
            Color.YELLOW: '0011', Color.WHITE: '0100', Color.BLUE: '0101'}


def roll(cube, face, direction):
    """
    Perform a roll operation on a specific face of the rubiks cube.

    See also roll_str, which is a simpler alternative to this function.

    :param face: An integer that represents the face to be rotated
    :param direction: The number of 90 degree clockwise rotations
                      performed on the cube. Negative numbers
                      represent anticlockwise rotations.
    """
    if face == Man.F.value:
        cube = bit_roll(cube, direction, 16, 20)
        if direction > 0:
            cube = bit_swap(cube, 2, 4, 21, 23)
            cube = bit_swap(cube, 2, 4, 4, 6)
            cube = bit_swap(cube, 2, 3, 15, 16)
            cube = bit_swap(cube, 3, 4, 12, 13)
            return cube
        cube = bit_swap(cube, 4, 6, 21, 23)
        cube = bit_swap(cube, 4, 6, 2, 4)
        cube = bit_swap(cube, 5, 6, 12, 13)
        cube = bit_swap(cube, 4, 5, 15, 16)
        return cube

    if face == Man.L.value:
        cube = bit_roll(cube, direction, 20, 24)
        if direction > 0:
            cube = bit_swap(cube, 0, 1, 10, 11)
            cube = bit_swap(cube, 3, 4, 9, 10)
            cube = bit_swap(cube, 0, 1, 4, 5)
            cube = bit_swap(cube, 3, 4, 7, 8)
            cube = bit_swap(cube, 0, 1, 16, 17)
            cube = bit_swap(cube, 3, 4, 19, 20)
            return cube
        cube = bit_swap(cube, 0, 1, 16, 17)
        cube = bit_swap(cube, 3, 4, 19, 20)
        cube = bit_swap(cube, 0, 1, 4, 5)
        cube = bit_swap(cube, 3, 4, 7, 8)
        cube = bit_swap(cube, 0, 1, 10, 11)
        cube = bit_swap(cube, 3, 4, 9, 10)
        return cube

    if face == Man.U.value:
        cube = bit_roll(cube, direction, 4, 8)
        if direction > 0:
            cube = bit_swap(cube, 5, 6, 7, 8, bit_unit=8)
            cube = bit_swap(cube, 5, 6, 9, 10, bit_unit=8)
            cube = bit_swap(cube, 5, 6, 11, 12, bit_unit=8)
            return cube
        cube = bit_swap(cube, 5, 6, 11, 12, bit_unit=8)
        cube = bit_swap(cube, 5, 6, 9, 10, bit_unit=8)
        cube = bit_swap(cube, 5, 6, 7, 8, bit_unit=8)
        return cube

def roll_str(cube, string):
    """
    Perform roll operations on the cube based on a sequence of characters in a string.

    The function reads each character of a string and performs an operation on the face
    specified by the character in sequence.

    F, B, L, R, U, D represents a clockwise rotation to the Front, Back, Left, Right,
    Upward, Downward faces of the cube respectively.
    f, b, l, r, u, d represents an anticlockwise rotation to the front, back, left, right,
    upward, downward faces of the cube respectively.

    :param string: A string where each character represents a roll operation on the cube.
                   Cannot contain any other characters other than the 12 specified above.
    """
    for i in string:
        cube = roll(cube, *dir_map[i])
    return cube

ROT_SWAPS = {Man.F.value: ((5, 6), (1, 2), (3, 4), (0, 1)),
             Man.L.value: ((0, 1), (2, 3), (1, 2), (4, 5)),
             Man.U.value: ((2, 3), (3, 4), (4, 5), (5, 6))}

def rot(cube, face, direction):
    """
    Rotate the cube 90 degrees in relation to one of the faces of the cube.

    See also rot_str, which is a simpler alternative to this function

    :param face: An intiger representing a face which specifies
                 the axis which the cube is rotated along
    :param direction: The number of 90 degrees clockwise rotations performed
                      on the cube. Negative numbers represent anticlockwise
                      rotations.
    """
    if face == Man.F.value:
        cube = bit_roll(cube, direction, 0, 4)
        cube = bit_roll(cube, direction, 4, 8)
        cube = bit_roll(cube, -direction, 8, 12)
        cube = bit_roll(cube, direction, 12, 16)
        cube = bit_roll(cube, direction, 16, 20)
        cube = bit_roll(cube, direction, 20, 24)
        for i in (range(1, 4) if direction > 0 else range(3, 0, -1)):
            cube = bit_swap(cube, *ROT_SWAPS[Man.F.value][0], *ROT_SWAPS[Man.F.value][i], bit_unit=16)
        return cube

    if face == Man.L.value:
        cube = bit_roll(cube, -direction, 12, 16)
        cube = bit_roll(cube, direction, 20, 24)
        for i in (range(1, 4) if direction > 0 else range(3, 0, -1)):
            cube = bit_swap(cube, *ROT_SWAPS[Man.L.value][0], *ROT_SWAPS[Man.L.value][i], bit_unit=16)
        cube = bit_swap(cube, 4, 5, 5, 6, bit_unit=8)
        cube = bit_swap(cube, 2, 3, 3, 4, bit_unit=8) if direction > 0 else bit_swap(cube, 0, 1, 2, 3, bit_unit=8)
        return cube

    if face == Man.U.value:
        cube = bit_roll(cube, direction, 4, 8)
        cube = bit_roll(cube, -direction, 0, 4)
        for i in (range(1, 4) if direction > 0 else range(3, 0, -1)):
            cube = bit_swap(cube, *ROT_SWAPS[Man.U.value][0], *ROT_SWAPS[Man.U.value][i], bit_unit=16)
        return cube

def rot_str(cube, string):
    """
    Perform rotation operations on the cube based on a sequence of characters in a string.

    The function reads each character of a string and performs an operation along the face
    specified by the character in sequence.

    U, L, F represents a clockwise rotation along the Upward, Leftward, Frontward faces of the
    cube respectively.
    u, l, f represents an anticlockwise rotation along the upward, leftward, frontward
    faces of the cube respectively.

    :param string: A string where each character represents a rotation operation on the cube.
                   Cannot contain any other characters other than the 6 specified above.
    """
    for i in string:
        cube = rot(cube, *dir_map[i])
    return cube


def randomize(cube, moves=500):
    """
    Randomizes the rubiks cube.

    :param moves: Integer representing the number of random moves to be applied to the cube
    """
    for i in range(randrange(moves)):
        c = choice([Man.L.value, Man.F.value, Man.U.value])
        r = choice([1, -1])
        cube = roll(cube, c, r)
        # verify_cube(cube)
    return cube

NEW = 80596284442678810400085
def new_cube(random=False):
    """
    Create a 6x2x2 array that represents a rubiks cube.

    :param random: Boolean option to randomize cube on init
    :returns: 6x2x2 numpy array representing a rubiks cube
    """

    # side = [or_sum((s << 4*z for z in range(0, SIZE[0]*SIZE[1]))) for s in Man]
    # cube = or_sum((side[5-z] << 16*z for z in range(0, 6)))

    if random:
        return randomize(NEW)
    return NEW


masks = [ones(8) << 24, ones(8) << 16,
         or_sum((0b1111_1111_0000_0000 << 16*z for z in range(0, 4))) << 32,
         or_sum((0b0000_0000_1111_1111 << 16*z for z in range(0, 4))) << 32,
         ones(8) << 8, ones(8)]

def cube_str(cube):
    """
    Return a ascii color coded string representation of a cube.

    The string takes on the following form, where x and o characters
    represents different sides of the cube:
      xx
      xx
    xxooxxoo
    xxooxxoo
      xx
      xx

    :returns: String representation of the rubiks cube
    """
    lines = []

    lines.append(f'  {bit_repr((masks[0] & cube) >> 24, 8)}')
    lines.append(f'  {bit_repr(bit_roll(((masks[1] & cube) >> 16), 1, 0, 2), 8)}')

    t = (masks[2] & cube) >> 40
    for i in range(2, 8, 2):
        t = bit_strip(t, i, i+2)
    lines.append(bit_repr(t, 32))


    t = (masks[3] & cube) >> 32
    for i in range(0, 8, 2):
        t = bit_strip(t, i+2, i+4)
        t = bit_roll(t, 1, i, i+2)
    lines.append(bit_repr(t, 32))

    lines.append(f'  {bit_repr((masks[4] & cube) >> 8, 8)}')
    lines.append(f'  {bit_repr(bit_roll(((masks[5] & cube)), 1, 0, 2), 8)}')
    # print(lines)

    for i, l in enumerate(lines):
        l = l.replace('0b', '')
        for c in Color:
            l = l.replace(BIN_MAP[c], ColorValue[c.name].value)
        l = l.replace('_', '')
        lines[i] = l

    return "\n".join(lines)


def hash_cube(cube):
    """Hashes the current state of the cube."""
    return cube

def print_cube(cube):
    print(cube_str(cube))
