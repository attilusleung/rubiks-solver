from cube import Cube
from cube2d import Cube2D
from copy import deepcopy

# class Edge:
#     def __init__(self, n1, n2, op):
#         pass


class Node:
    def __init__(self, cube, bk = [], edges = {}, final = False):
        self._cube = deepcopy(cube)
        self.edges = {}
        self.final = final
        self.bk = bk

    @property
    def cube(self):
        return deepcopy(self._cube)

class Solver:
    def __init__(self, cube):
        #assert isinstance(cube, Cube)
        self.nodes = {}
        self.type = type(cube)
        self._init_final()
        self.start = cube.hash_state()
        try:
            self.nodes[self.start]
        except KeyError:
            self.nodes[self.start] = Node(cube)
        self.queue = []
        self.queue.append(self.nodes[self.start])

    def _init_final(self):
        for i in ["", "L", "l", "F", "f", "LL"]:
            c = self.type()
            c.rot_str(i)
            for j in range(0,4):
                c.rot(c.U, 1)
                print(c.hash_state())
                self.nodes[c.hash_state()] = Node(c, final = True)
        #self._assert_unique(self.nodes.keys())

    def _assert_unique(self, cubes):
        seen = set()
        assert not any(i in seen or seen.add(i) for i in cubes)

    def solve(self):
        print("starting solve")
        while self.queue:
            s = self.search()
            if s is not None: return s
            #print("finish while")
        #print("what")

    def search(self):
        op = ["L", "l", "F", "f", "R", "r", "B", "b", "U", "u", "D", "d"]
        node = self.queue.pop(0)
        #print("searching %s" % node.cube.hash_state())
        #print("original \n" + str(node.cube))
        for s in op:
            cu = node.cube
            cu.roll_str(s)
            try:
                cunode = self.nodes[cu.hash_state()]
                if cunode.final: 
                    bk = node.bk
                    bk.append(s)
                    #print(bk)
                    return bk
                # node.edges[s] = cunode
                # print("visited")
                # print(cunode.bk)
            except KeyError:
                #print(s)
                bk = node.bk[:]
                bk.append(s)
                #print(bk)
                cunode = Node(cu, bk=bk)#, edges = {s.swapcase(): node})
                self.nodes[cu.hash_state()] = cunode
                node.edges[s] = cunode
                self.queue.append(cunode)

    def solve_by_depth(self, i):
        while len(self.queue[0].bk) <= i:
            s = self.search()
            if s is not None: 
                print(s)
                return s




