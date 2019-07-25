from cube import Cube
from cube2d import Cube2D
from copy import deepcopy


class Node:
    """A node object representing a single cube state for bfs."""
    def __init__(self, cube, bk = [], edges = {}, final = False):
        self._cube = deepcopy(cube)
        self.edges = {}
        self.final = final
        self.bk = bk

    @property
    def cube(self):
        return deepcopy(self._cube)

class Solver:
    """
    A object-oriented rubiks cube solver based on bfs.

    This implementation uses objects to represent cubes and nodes, which
    uses a lot of memory and is thus very slow.
    """

    def __init__(self, cube):
        """
        Initialize a solver for a specific cube.

        :param cube: The Cube object to be solved.
        """
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
        """
        Initializes the final nodes of the graph.

        As the cube is not rotation invariant,
        several final nodes are required for every
        different rotation of the completed cube.
        """
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
        """
        Find the minimal operations required to solve the rubiks cube.

        :returns: The string sequence of operations that solves the cube.
        """
        print("starting solve")
        while self.queue:
            s = self.search()
            if s is not None: return s
            #print("finish while")
        #print("what")

    def search(self):
        """
        Performs an iteration of the depth first search.

        It generates and searches all adjacent nodes to the queued node
        and searches it for the finished state.
        In this case, an adjcaent node is a cube state that is reachable
        by performing a single roll operation.
        """
        op = ["L", "l", "F", "f", "R", "r", "B", "b", "U", "u", "D", "d"]
        node = self.queue.pop(0)
        #print("searching %s" % node.cube.hash_state())
        #print("original \n" + str(node.cube))
        for s in op:
            cu = node.cube
            cu.roll_str(s)
            try:  # TODO: Make it more efficient
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
        """
        Find the minimum operations required to solve the rubiks cube until it reaches a maximum depth.

        :param i: An integer representing the maximum depth of the search.
        :returns: The string sequence of operations that solves the cube.
        """
        while len(self.queue[0].bk) <= i:
            s = self.search()
            if s is not None:
                print(s)
                return s
