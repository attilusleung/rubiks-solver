from .helpers import *

corners = [(0, 9, 20), (1, 8, 13), (2, 17,12), (3, 16, 21), (4, 19, 22), (5, 18, 15), (6, 11, 14), (7, 10, 23)]

O = 0
G = 1
R = 2
Y = 3
W = 4
B = 5

def get_corner(cube, pos1, pos2, pos3, bit_unit=4):
    pos1 *= bit_unit
    pos2 *= bit_unit
    pos3 *= bit_unit

    tmp = ones(bit_unit)
    i = tmp << pos1
    j = tmp << pos2
    k = tmp << pos3
    return {(i & cube) >> pos1, (j & cube) >> pos2, (k & cube) >> pos3}

def verify_cube(cube):
    legit_corners = [{W, O, G}, {O, G, B}, {G, R, B}, {W, G, R}, {W, R, Y}, {R, Y, B}, {Y, W, O}, {Y, B, O}]
    for c in corners:
        c = get_corner(cube, *c)
        print(c)
        legit_corners.remove(c)

a = 1340869702201399720993226835
# def test():
