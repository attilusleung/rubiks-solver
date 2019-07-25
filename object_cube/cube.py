from random import choice, randrange
import numpy as np

class Cube:
    """
    A 2x2 Rubiks Cube implemented using arrays.
    """

    CWHITE  = "\u001b[37m"
    CRED    = "\u001b[31m"
    CBLUE   = "\u001b[34m"
    CORANGE = "\u001b[31;1m"
    CGREEN  = "\u001b[32m"
    CYELLOW = "\u001b[33m"
    CRESET  = "\u001b[0m"

    WHITE  = CWHITE + "\u25a0" + CRESET
    RED    = CRED + "\u25a0" + CRESET
    BLUE   = CBLUE + "\u25a0" + CRESET
    ORANGE = CORANGE + "\u25a0" + CRESET
    GREEN  = CGREEN + "\u25a0" + CRESET
    YELLOW = CYELLOW + "\u25a0" + CRESET

    L = 0
    F = 1
    R = 2
    B = 3
    U = 4
    D = 5

    SIZE = (2, 2)

    dir_map = {"L": (L, 1), "F": (F, 1), "R": (R, 1), "B": (B, 1), "U": (U, 1), "D": (D, 1),
               "l": (L, -1), "f": (F, -1), "r": (R, -1), "b": (B, -1), "u": (U, -1), "d": (D, -1)}
    color_map = {WHITE: "0", RED: "1", BLUE: "2", ORANGE: "3", GREEN: "4", YELLOW:"5"}

    def _init_consts(self):
        self.strsize  = (self.SIZE[1]*3, self.SIZE[0]*4)
        self.strleft  = (slice(self.SIZE[1],   self.SIZE[1]*2),   slice(0,         self.SIZE[0]))
        self.strfront = (slice(self.SIZE[1],   self.SIZE[1]*2),   slice(self.SIZE[0],   self.SIZE[0]*2))
        self.strright = (slice(self.SIZE[1],   self.SIZE[1]*2),   slice(self.SIZE[0]*2, self.SIZE[0]*3))
        self.strback  = (slice(self.SIZE[1],   self.SIZE[1]*2),   slice(self.SIZE[0]*3, self.SIZE[0]*4))
        self.strup    = (slice(0,         self.SIZE[1]),     slice(self.SIZE[0],   self.SIZE[0]*2))
        self.strdown  = (slice(self.SIZE[1]*2, self.SIZE[1]*3),   slice(self.SIZE[0],   self.SIZE[0]*2))

    def __init__(self, randomize=False):
        """
        Creates a new 2x2 rubiks cube.

        :param randomize: Boolean specifying whether to randomize
                          the cube on initialization
        """
        self._init_consts()
        self.array = np.array([[[x for i in range(self.SIZE[0])] for j in range(self.SIZE[1])]
                                   for x in [self.ORANGE, self.GREEN, self.RED, self.YELLOW, self.WHITE, self.BLUE]])
        if bool(randomize):
            self.randomize()

    def _assert_count(self, a):
        _, counts = np.unique(a, return_counts=True)
        for i in counts:
            assert i == self.SIZE[0] * self.SIZE[1]

    def _verify_cube(self):
        W = self.WHITE
        O = self.ORANGE
        G = self.GREEN
        B = self.BLUE
        R = self.RED
        Y = self.YELLOW
        a = self.array
        legit_corners = [{W, O, G}, {O, G, B}, {G, R, B}, {W, G, R}, {W, R, Y}, {R, Y, B}, {Y, W, O}, {Y, B, O}]
        corners = [{a[0,0,1], a[1,0,0], a[4,1,0]}, {a[0,1,1], a[1,1,0], a[5,0,0]}, {a[1,0,1], a[4,1,1], a[2,0,0]},
                   {a[1,1,1], a[2,1,0], a[5,0,1]}, {a[2,0,1], a[3,0,0], a[4,0,1]}, {a[2,1,1], a[3,1,0], a[5,1,1]},
                   {a[3,0,1], a[4,0,0], a[0,0,0]}, {a[3,1,1], a[5,1,0], a[0,1,0]}]
        for i in legit_corners:
            assert i in corners, i

    def hash_state(self):
        """Hashes the current state of the cube."""
        it = np.nditer(self.array, flags=["common_dtype"])
        ret = "".join((i.item() for i in it))
        for k, v in self.color_map.items():
            ret = ret.replace(k, v)
        return ret

    def __eq__(self, obj):
        """
        Check if obj is equal to the cube.

        Two cubes are equal if they are both instances of Cube and
        all color tiles on each side of the cube is the same.

        The rubiks cubes are not rotation invariant. Therefore, a rotated
        cube is not guarenteed to be equal to its original cube.

        :param obj: The object to check for equality
        :returns: The equality of the cube and obj
        """
        if not isinstance(obj, Cube): return False
        return np.array_equal(obj.array, self.array)

    def randomize(self, moves=500):
        """
        Randomizes the rubiks cube.

        :param moves: Integer representing the number of random moves to be applied to the cube
        """
        for i in range(randrange(moves)):
            # try:
            #     self._verify_cube()
            # except NotImplementedError:
            #     print("skipping asserts")
            c = choice([self.L, self.F, self.R, self.B, self.U ,self.D])
            r = randrange(1, 3)
            self.roll(c, r)

    def __str__(self):
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
        ret = np.full(self.strsize, " ", dtype=np.dtype('u16'))
        ret[self.strleft] = self.array[0]
        #print(self.array[0])
        ret[self.strfront] = self.array[1]
        ret[self.strright] = self.array[2]
        ret[self.strback] = self.array[3]
        ret[self.strup] = self.array[4]
        ret[self.strdown] = self.array[5]
        # print(repr(ret))
        return "\n".join([''.join([ret[i, x]
                          for x in range(0, self.strsize[1])])
                          for i in range(0, self.strsize[0])])
        # for i in range(0, STRSIZE[0]):
        #     for j in range(0, STRSIZE[1]):
        #         print(ret[i,j], end = "")
        #     print()


    def __repr__(self):
        """Return a printable representation of a cube based on its string representation"""
        return super().__repr__() + "\n" + self.__str__()


    def roll(self, face, direction):
        """
        Perform a roll operation on a specific face of the rubiks cube.

        See also roll_str, which is a simpler alternative to this function.

        :param face: An integer that represents the face to be rotated
        :param direction: The number of 90 degree clockwise rotations
                          performed on the cube. Negative numbers
                          represent anticlockwise rotations.
        """
        #print(["L", "F", "R", "B", "U", "D"][face] + str(direction))
        if face == self.U:
            self.array[0:4, 0] = np.roll(self.array[0:4, 0], -direction, axis=0)
            self.array[self.U] = np.rot90(self.array[self.U], k=-direction)
        elif face == self.D:
            self.array[0:4, -1] = np.roll(self.array[0:4, -1], direction, axis=0)
            self.array[self.D] = np.rot90(self.array[self.D], k=-direction)
        elif face == self.F:
            sl = np.array([self.array[self.U, -1, :], self.array[self.R, :, 0],
                           self.array[self.D, 0, ::-1], self.array[self.L, ::-1, -1]])
            sl = np.roll(sl, direction, axis=0)
            self.array[self.U, -1, :] = sl[0]
            self.array[self.R, :, 0] = sl[1]
            self.array[self.D, 0, ::-1] = sl[2]
            self.array[self.L, ::-1, -1] = sl[3]
            self.array[self.F] = np.rot90(self.array[self.F], k=-direction)#TODO: Use map function
        elif face == self.B:
            sl = np.array([self.array[self.U, 0, :], self.array[self.R, :, -1],
                           self.array[self.D, -1, ::-1], self.array[self.L, ::-1, 0]])
            sl = np.roll(sl, -direction, axis=0)
            self.array[self.U, 0, :] = sl[0]
            self.array[self.R, :, -1] = sl[1]
            self.array[self.D, -1, ::-1] = sl[2]
            self.array[self.L, ::-1, 0] = sl[3]
            self.array[self.B] = np.rot90(self.array[self.B], k=-direction)#TODO: Use map function
        elif face == self.L:
            sl = np.array([self.array[self.F, :, 0], self.array[self.D, :, 0], self.array[self.B, ::-1, -1], self.array[self.U, :, 0]])
            sl = np.roll(sl, direction, axis=0)
            self.array[self.F, :, 0] = sl[0]
            self.array[self.D, :, 0] = sl[1]
            self.array[self.B, ::-1, -1] = sl[2]
            self.array[self.U, :, 0] = sl[3]
            self.array[self.L] = np.rot90(self.array[self.L], k=-direction)
        elif face == self.R:
            sl = np.array([self.array[self.F, :, -1], self.array[self.D, :, -1], self.array[self.B, ::-1, 0], self.array[self.U, :, -1]])
            sl = np.roll(sl, -direction, axis=0)
            self.array[self.F, :, -1] = sl[0]
            self.array[self.D, :, -1] = sl[1]
            self.array[self.B, ::-1, 0] = sl[2]
            self.array[self.U, :, -1] = sl[3]
            self.array[self.R] = np.rot90(self.array[self.R], k=-direction)
        #print(self.__str__())


    def roll_str(self, string):
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
            self.roll(*self.dir_map[i])


    def rot(self, face, direction):
        """
        Rotate the cube 90 degrees in relation to one of the faces of the cube.

        See also rot_str, which is a simpler alternative to this function

        :param face: An intiger representing a face which specifies
                     the axis which the cube is rotated along
        :param direction: The number of 90 degrees clockwise rotations performed
                          on the cube. Negative numbers represent anticlockwise
                          rotations.
        """
        if face == self.U:
            self.array[0:4] = np.roll(self.array[0:4], -direction, axis=0)
            self.array[4] = np.rot90(self.array[4], k=-direction)
            self.array[5] = np.rot90(self.array[5], k=direction)
        elif face == self.L:
            sl = [self.array[self.F], self.array[self.D], self.array[self.B, ::-1], self.array[self.U]]
            sl = np.roll(sl, direction, axis=0)
            self.array[self.F] = sl[0]
            self.array[self.D] = sl[1]
            self.array[self.B, ::-1] = sl[2]
            self.array[self.U] = sl[3]
            self.array[self.L] = np.rot90(self.array[self.L], k=-direction)
            self.array[self.R] = np.rot90(self.array[self.R], k=direction)
        elif face == self.F:
            sl = np.array([self.array[self.U], self.array[self.R], self.array[self.D], self.array[self.L]])
            sl = np.rot90(sl, k=-direction, axes=(1, 2))
            sl = np.roll(sl, direction, axis=0)
            self.array[self.U] = sl[0]
            self.array[self.R] = sl[1]
            self.array[self.D] = sl[2]
            self.array[self.L] = sl[3]
            self.array[self.F] = np.rot90(self.array[self.F], k=-direction)
            self.array[self.B] = np.rot90(self.array[self.B], k=direction)

    def rot_str(self, string):
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
            self.rot(*self.dir_map[i])
