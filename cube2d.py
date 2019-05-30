from cube import Cube
import numpy as np

class Cube2D(Cube):
    SIZE = (2,2)

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

    # def std_rot(self):
    #     corners = {{a[0,0,1], a[1,0,0], a[4,1,0]}, {a[0,1,1], a[1,1,0], a[5,0,0]}, {a[1,0,1], a[4,1,1], a[2,0,0]},
    #                {a[1,1,1], a[2,1,0], a[5,0,1]}, {a[2,0,1], a[3,0,0], a[4,0,1]}, {a[2,1,1], a[3,1,0], a[5,1,1]},
    #                {a[3,0,1], a[4,0,0], a[0,0,0]}, {a[3,1,1], a[5,1,0], a[0,1,0]}}

    def hash_state(self):
        it = np.nditer(self.array, flags=["common_dtype"])
        ret = "".join((i.item() for i in it))
        for k, v in self.color_map.items():
            ret = ret.replace(k, v)
        return ret
 
    def __eq__(self, obj):
        if not isinstance(obj, Cube): return False
        return np.array_equal(obj.array, self.array)

a = Cube2D()

b = Cube2D()
b.roll_str("U")

c = Cube2D()
c.roll_str("FUL")
