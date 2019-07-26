"""
Functions to manipulate a 6x2x2 array representing a 2x2 rubiks cube.

The array represents an unwrapped cube, where each 2x2 array represents
the leftward, frontward, rightward, backward, uupward, downward faces
of the rubiks cube respectively.
"""

from enum import Enum
import gc
import numpy as np
from random import randrange, choice

class Man(Enum):
    L = 0
    F = 1
    R = 2
    B = 3
    U = 4
    D = 5


dir_map = {"L":(Man.L.value, 1), "F":(Man.F.value, 1), "R":(Man.R.value, 1), "B":(Man.B.value, 1), "U":(Man.U.value, 1), "D":(Man.D.value, 1),
           "l":(Man.L.value, -1), "f":(Man.F.value, -1), "r":(Man.R.value, -1), "b":(Man.B.value, -1), "u":(Man.U.value, -1), "d":(Man.D.value, -1)}

SIZE = (2,2)

STRSIZE  = (SIZE[1]*3, SIZE[0]*4)
STRLEFT  = (slice(SIZE[1],   SIZE[1]*2),   slice(0,         SIZE[0]))
STRFRONT = (slice(SIZE[1],   SIZE[1]*2),   slice(SIZE[0],   SIZE[0]*2))
STRRIGHT = (slice(SIZE[1],   SIZE[1]*2),   slice(SIZE[0]*2, SIZE[0]*3))
STRBACK  = (slice(SIZE[1],   SIZE[1]*2),   slice(SIZE[0]*3, SIZE[0]*4))
STRUP    = (slice(0,         SIZE[1]),     slice(SIZE[0],   SIZE[0]*2))
STRDOWN  = (slice(SIZE[1]*2, SIZE[1]*3),   slice(SIZE[0],   SIZE[0]*2))



class Color(Enum):
    ORANGE = 0
    GREEN = 1
    RED = 2
    YELLOW = 3
    WHITE = 4
    BLUE = 5

class ColorValue(Enum):
    ORANGE = "\u001b[31;1m\u25a0\u001b[0m"
    GREEN = "\u001b[32m\u25a0\u001b[0m"
    RED = "\u001b[31m\u25a0\u001b[0m"
    YELLOW = "\u001b[33m\u25a0\u001b[0m"
    WHITE = "\u001b[37m\u25a0\u001b[0m"
    BLUE = "\u001b[34m\u25a0\u001b[0m"


def roll(cube, face, direction):
    """
    Perform a roll operation on a specific face of the rubiks cube.

    See also roll_str, which is a simpler alternative to this function.

    :param face: An integer that represents the face to be rotated
    :param direction: The number of 90 degree clockwise rotations
                      performed on the cube. Negative numbers
                      represent anticlockwise rotations.
    """
    #print(["L", "F", "R", "B", "U", "D"][face] + str(direction))
    cube = np.copy(cube)
    if face == Man.U.value:
        cube[0:4, 0] = np.roll(cube[0:4, 0], -direction, axis=0)
        cube[Man.U.value] = np.rot90(cube[Man.U.value], k=-direction)
    elif face == Man.D.value:
        cube[0:4, -1] = np.roll(cube[0:4, -1], direction, axis=0)
        cube[Man.D.value] = np.rot90(cube[Man.D.value], k=-direction)
    elif face == Man.F.value:
        sl = np.array([cube[Man.U.value, -1, :], cube[Man.R.value, :, 0],
                       cube[Man.D.value, 0, ::-1], cube[Man.L.value, ::-1, -1]])
        sl = np.roll(sl, direction, axis=0)
        cube[Man.U.value, -1, :] = sl[0]
        cube[Man.R.value, :, 0] = sl[1]
        cube[Man.D.value, 0, ::-1] = sl[2]
        cube[Man.L.value, ::-1, -1] = sl[3]
        cube[Man.F.value] = np.rot90(cube[Man.F.value], k=-direction)#TODO: Use map function
    elif face == Man.B.value:
        sl = np.array([cube[Man.U.value, 0, :], cube[Man.R.value, :, -1], cube[Man.D.value, -1, ::-1], cube[Man.L.value, ::-1, 0]])
        sl = np.roll(sl, -direction, axis=0)
        cube[Man.U.value, 0, :] = sl[0]
        cube[Man.R.value, :, -1] = sl[1]
        cube[Man.D.value, -1, ::-1] = sl[2]
        cube[Man.L.value, ::-1, 0] = sl[3]
        cube[Man.B.value] = np.rot90(cube[Man.B.value], k=-direction)#TODO: Use map function
    elif face == Man.L.value:
        sl = np.array([cube[Man.F.value, :, 0], cube[Man.D.value, :, 0], cube[Man.B.value, ::-1, -1], cube[Man.U.value, :, 0]])
        sl = np.roll(sl, direction, axis=0)
        cube[Man.F.value, :, 0] = sl[0]
        cube[Man.D.value, :, 0] = sl[1]
        cube[Man.B.value, ::-1, -1] = sl[2]
        cube[Man.U.value, :, 0] = sl[3]
        cube[Man.L.value] = np.rot90(cube[Man.L.value], k=-direction)
    elif face == Man.R.value:
        sl = np.array([cube[Man.F.value, :, -1], cube[Man.D.value, :, -1], cube[Man.B.value, ::-1, 0], cube[Man.U.value, :, -1]])
        sl = np.roll(sl, -direction, axis=0)
        cube[Man.F.value, :, -1] = sl[0]
        cube[Man.D.value, :, -1] = sl[1]
        cube[Man.B.value, ::-1, 0] = sl[2]
        cube[Man.U.value, :, -1] = sl[3]
        cube[Man.R.value] = np.rot90(cube[Man.R.value], k=-direction)
    return cube
    #print(Man.__str__())

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

    cube = np.copy(cube)
    if face == Man.U.value:
        cube[0:4] = np.roll(cube[0:4], -direction, axis=0)
        cube[4] = np.rot90(cube[4], k=-direction)
        cube[5] = np.rot90(cube[5], k=direction)
    elif face == Man.L.value:
        sl = [cube[Man.F.value], cube[Man.D.value], cube[Man.B.value, ::-1], cube[Man.U.value]]
        sl = np.roll(sl, direction, axis=0)
        cube[Man.F.value] = sl[0]
        cube[Man.D.value] = sl[1]
        cube[Man.B.value, ::-1] = sl[2]
        cube[Man.U.value] = sl[3]
        cube[Man.L.value] = np.rot90(cube[Man.L.value], k=-direction)
        cube[Man.R.value] = np.rot90(cube[Man.R.value], k=direction)
    elif face == Man.F.value:
        sl = np.array([cube[Man.U.value], cube[Man.R.value], cube[Man.D.value], cube[Man.L.value]])
        sl = np.rot90(sl, k = -direction, axes=(1,2))
        sl = np.roll(sl, direction, axis=0)
        cube[Man.U.value] = sl[0]
        cube[Man.R.value] = sl[1]
        cube[Man.D.value] = sl[2]
        cube[Man.L.value] = sl[3]
        cube[Man.F.value] = np.rot90(cube[Man.F.value], k=-direction)
        cube[Man.B.value] = np.rot90(cube[Man.B.value], k=direction)
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
    for i in range(moves):
        #verify_cube()
        c = choice([Man.L.value, Man.F.value, Man.R.value, Man.B.value, Man.U.value, Man.D.value])
        r = randrange(1, 3)
        cube = roll(cube, c, r)
    gc.collect()
    return cube

def new_cube(random=False):
    """
    Create a 6x2x2 array that represents a rubiks cube.

    :param random: Boolean option to randomize cube on init
    :returns: 6x2x2 numpy array representing a rubiks cube
    """
    cube = np.array([[[x for i in range(SIZE[0])] for j in range(SIZE[1])]
                        for x in [Color.ORANGE.value, Color.GREEN.value, Color.RED.value,
                                    Color.YELLOW.value, Color.WHITE.value, Color.BLUE.value]], dtype=np.int8)
    if random:
        return cube.randomize()
    return cube


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
    ret = np.full(STRSIZE, " ", dtype=np.dtype('U16'))
    ret[STRLEFT] = cube[0]
    ret[STRFRONT] = cube[1]
    ret[STRRIGHT] = cube[2]
    ret[STRBACK] = cube[3]
    ret[STRUP] = cube[4]
    ret[STRDOWN] = cube[5]
    for i in Color:
        ret = np.where(ret!=str(i.value), ret, ColorValue[i.name].value)
    return "\n".join([''.join([ret[i, x] for x in range(0,STRSIZE[1])]) for i in range(0, STRSIZE[0])])


def hash_cube(cube):
    """Hashes the current state of the cube."""
    it = np.nditer(cube, flags=["common_dtype"])
    ret = "".join((str(i.item()) for i in it))
    return ret
