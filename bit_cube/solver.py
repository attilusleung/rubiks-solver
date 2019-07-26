import numpy as np
from .manipulations import *


class Solver:
    """
    A rubiks cube solver implemented using only arrays based on bfs.

    This is significantly faster than the object orientated approach,
    as it reduces the memory required due to less objects being created.
    """
    op = ["L", "l", "F", "f", "U", "u"]
    def __init__(self, cube):
        """
        Initializes a solver for a specific cube.

        :param cube: The Cube object to be solved.
        """
        self.org = cube
        self.queue = [cube]
        self.visited = {cube: (None, "")}
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
                cc = rot_str(c, "U"*j)
                self.final.append(cc)

    def solve(self):
        """
        Find the minimal operations required to solve the rubiks cube.

        :returns: The string sequence of operations that solves the cube.
        """
        acc = 0
        if self.queue[0] in self.final: return ""
        while self.queue:
            print(acc)
            acc += 1
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
            if manstep not in self.visited:
                self.visited[manstep] = (step, s)
                if manstep in self.final:
                    return self.backtrack(manstep)
                self.queue.append(manstep)

    def backtrack(self, node):
        acc = ""
        # print(self.visited[node])
        while self.visited[node][0] is not None:
            # print(acc)
            acc = self.visited[node][1] + acc
            node = self.visited[node][0]
        return acc


    # def search_by_depth(self, i):
    #     c = True
    #     while c:
    #         s = self.search()
    #         if s is not None:
    #             print(s)
    #             return s
    #         c = len(self.visited[self.queue[0]][1]) <= i
    #     return 'search failed'
