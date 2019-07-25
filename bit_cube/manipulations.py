"""
Functions to manipulate an integer representing a 2x2 rubiks cube.
"""
# TODO: Documentation

from helpers import *
from enum import Enum, IntEnum
from functools import reduce
from random import randrange, choice
import numpy as np

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
    pass

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
    pass

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
        #verify_cube()
        c = choice([Man.L.value, Man.F.value, Man.R.value, Man.B.value, Man.U.value , Man.D.value])
        r = randrange(1, 3)
        cube = roll(cube, c, r)
    return cube

def new_cube(randomize=False):
    """
    Create a 6x2x2 array that represents a rubiks cube.

    :param randomize: Boolean option to randomize cube on init
    :returns: 6x2x2 numpy array representing a rubiks cube
    """

    side = [or_sum((s << 4*z for z in range(0, SIZE[0]*SIZE[1]))) for s in Man]
    cube = or_sum((side[5-z] << 16*z for z in range(0, 6)))

    if randomize:
        return cube.randomize()
    return cube

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
    for i in range(8, 32, 8):
        t = bit_strip(t, i, i+8)
    lines.append(bit_repr(t, 32))


    t = (masks[3] & cube) >> 32
    for i in range(8, 36, 8):
        t = bit_strip(t, i, i+8)
        t = bit_roll(t, 1, i, i+8)
    lines.append(bit_repr(t, 32))

    lines.append(f'  {bit_repr((masks[4] & cube) >> 8, 8)}')
    lines.append(f'  {bit_repr(bit_roll(((masks[5] & cube)), 1, 0, 2), 8)}')

    for i, l in enumerate(lines):
        l = l.replace('0b', '')
        for c in Color:
            l = l.replace(BIN_MAP[c], ColorValue[c.name].value)
        l = l.replace('_', '')
        lines[i] = l

    return "\n".join(lines)


    # return "\n".join(lines)
    # return "\n".join([''.join([ret[i, x] for x in range(0,STRSIZE[1])]) for i in range(0, STRSIZE[0])])


def hash_cube(cube):
    """Hashes the current state of the cube."""
    return cube
