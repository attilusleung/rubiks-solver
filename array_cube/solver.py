import numpy as np
from manipulations import *


class Solver:
    """
    A rubiks cube solver implemented using only arrays based on bfs.

    This is significantly faster than the object orientated approach,
    as it reduces the memory required due to less objects being created.
    """
    op = ["L", "l", "F", "f", "R", "r", "B", "b", "U", "u", "D", "d"]
    def __init__(self, cube):
        """
        Initializes a solver for a specific cube.

        :param cube: The Cube object to be solved.
        """
        self.queue = [cube]
        self.visited = {hash_cube(cube): (None, "")}
        self.type = cube.shape
        self._init_final()

    def _init_final(self):
        """
        Initializes the final nodes of the graph.

        As the cube is not rotation invariant,
        several final nodes are required for every
        different rotation of the completed cube.
        """
        self.final = []
        # acc = 0
        for i in ["", "L", "l", "F", "f", "LL"]:
            c = rot_str(new_cube(), i)
            for j in range(0,4):
                cc = rot(c, Man.U, j)
                self.final.append(hash_cube(cc))

    def solve(self):
        """
        Find the minimal operations required to solve the rubiks cube.

        :returns: The string sequence of operations that solves the cube.
        """
        if hash_cube(self.queue[0]) in self.final: return ""
        while self.queue:
            s = self.search()
            if s is not None: return s

    def search(self):
        """
        Performs an iteration of the depth first search.

        It generates and searches all adjacent nodes to the queued node
        and searches it for the finished state.
        In this case, an adjcaent node is a cube state that is reachable
        by performing a single roll operation.
        """
        step = self.queue.pop(0)
        for s in self.op:
            manstep = roll_str(step, s)
            h = hash_cube(manstep)
            if h not in self.visited:
                hc = hash_cube(step)
                self.visited[h] = (hc, self.visited[hc][1] + s)
                if h in self.final:
                    return self.visited[h][1]
                print(self.visited[h][1])
                self.queue.append(manstep)
