import numpy as np
from random import randrange, choice


# LVIEW = np.array([F,D,B,U])
# UVIEW = slice(0, 4)
# FVIEW = np.array([U,L,D,R])

class Cube:
    CWHITE  = "\u001b[37m"
    CRED    = "\u001b[31m"
    CBLUE   = "\u001b[34m"
    CORANGE = "\u001b[31;1m"
    CGREEN  = "\u001b[32m"
    CYELLOW = "\u001b[33m"
    CRESET = "\u001b[0m"
    
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
    
    SIZE     = (3,3)

    dir_map = {"L":(L, 1), "F":(F, 1), "R":(R, 1), "B":(B, 1), "U":(U, 1), "D":(D, 1),
               "l":(L, -1), "f":(F, -1), "r":(R, -1), "b":(B, -1), "u":(U, -1), "d":(D, -1)}
    color_map = {WHITE: "0", RED: "1", BLUE: "2", ORANGE: "3", GREEN: "4", YELLOW:"5"}

    def _init_consts(self):
        self.STRSIZE  = (self.SIZE[1]*3, self.SIZE[0]*4)
        self.STRLEFT  = (slice(self.SIZE[1],   self.SIZE[1]*2),   slice(0,         self.SIZE[0]))
        self.STRFRONT = (slice(self.SIZE[1],   self.SIZE[1]*2),   slice(self.SIZE[0],   self.SIZE[0]*2))
        self.STRRIGHT = (slice(self.SIZE[1],   self.SIZE[1]*2),   slice(self.SIZE[0]*2, self.SIZE[0]*3))
        self.STRBACK  = (slice(self.SIZE[1],   self.SIZE[1]*2),   slice(self.SIZE[0]*3, self.SIZE[0]*4))
        self.STRUP    = (slice(0,         self.SIZE[1]),     slice(self.SIZE[0],   self.SIZE[0]*2))
        self.STRDOWN  = (slice(self.SIZE[1]*2, self.SIZE[1]*3),   slice(self.SIZE[0],   self.SIZE[0]*2))

    def __init__(self, randomize = False):
        self._init_consts()
        self.array = np.array([[[x for i in range(self.SIZE[0])] for j in range(self.SIZE[1])] 
                                   for x in [self.ORANGE, self.GREEN, self.RED, self.YELLOW, self.WHITE, self.BLUE]])
        if bool(randomize):
            self.randomize()

    def _assert_count(self, a):
        unique, counts = np.unique(a, return_counts=True)
        for i in counts:
            assert i == self.SIZE[0] * self.SIZE[1]

    def _verify_cube(self):
        raise NotImplementedError("I'm too lazy to implement this in 3x3 but should be implemented in 2x2")

    def randomize(self):
        for i in range(randrange(500)):
            #self._assert_count(self.array)
            try:
                self._verify_cube()
            except NotImplementedError:
                print("skipping asserts because _verify_cube is not implemented")
            c = choice([self.L, self.F, self.R, self.B, self.U , self.D])
            r = randrange(1,3)
            self.roll(c, r)

    def __eq__(self):
        raise NotImplementedError("I'm also too lazy to do this for 3x3")
    
    def hash_state(self):
        raise NotImplementedError("2x2 implemented only")

    def __str__(self):
        ret = np.full(self.STRSIZE, " ", dtype=np.dtype('U16'))
        ret[self.STRLEFT] = self.array[0]
        #print(self.array[0])
        ret[self.STRFRONT] = self.array[1]
        ret[self.STRRIGHT] = self.array[2]
        ret[self.STRBACK] = self.array[3]
        ret[self.STRUP] = self.array[4]
        ret[self.STRDOWN] = self.array[5]
        # print(repr(ret))
        return "\n".join([''.join([ret[i, x] for x in range(0,self.STRSIZE[1])]) for i in range(0, self.STRSIZE[0])])
        # for i in range(0, STRSIZE[0]):
        #     for j in range(0, STRSIZE[1]):
        #         print(ret[i,j], end = "")
        #     print()


    def __repr__(self):
        return super().__repr__() + "\n" + self.__str__()
        

    def roll(self, face, direction):
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
            sl = np.array([self.array[self.U, 0, :], self.array[self.R, :, -1], self.array[self.D, -1, ::-1], self.array[self.L, ::-1, 0]])
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
        for i in string:
            self.roll(*self.dir_map[i])
    

    def rot(self, face, direction): #TODO: only U is correct
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
            sl = np.rot90(sl, k = -direction, axes=(1,2))
            sl = np.roll(sl, direction, axis=0)
            self.array[self.U] = sl[0]
            self.array[self.R] = sl[1]
            self.array[self.D] = sl[2]
            self.array[self.L] = sl[3]
            self.array[self.F] = np.rot90(self.array[self.F], k=-direction)
            self.array[self.B] = np.rot90(self.array[self.B], k=direction)

    def rot_str(self, string):
        for i in string:
            self.rot(*self.dir_map[i])


a = Cube()

