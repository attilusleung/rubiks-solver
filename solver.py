from manipulations import *
import numpy as np


class Solver:
    op = ["L", "l", "F", "f", "R", "r", "B", "b", "U", "u", "D", "d"]
    def __init__(self, cube):
        self.queue = [cube]
        self.visited = {hash_cube(cube): (None, "")}
        self.type = cube.shape
        self._init_final()
    
    def _init_final(self):
        self.final = []
        # acc = 0
        for i in ["", "L", "l", "F", "f", "LL"]:
            c = rot_str(new_cube(), i)
            for j in range(0,4):
                cc = rot(c, Man.U, j)
                self.final.append(hash_cube(cc))

    def solve(self):
        if hash_cube(self.queue[0]) in self.final: return ""
        while self.queue:
            s = self.search()
            if s is not None: return s

    def search(self):
        step = self.queue.pop(0)
        for s in self.op:
            manstep = roll_str(step, s)
            h = hash_cube(manstep)
            try:
                self.visited[h]
            except KeyError:
                hc = hash_cube(step)
                self.visited[h] = (hc, self.visited[hc][1] + s)
                if h in self.final:
                    return self.visited[h][1]
                print(self.visited[h][1])
                    #return self.backtrack(h)
                self.queue.append(manstep)


    def backtrack(self, h):
        node = self.visited[h]
        ret = ""
        while node[0] is not None:
            ret = node[1] + ret 
            node = self.visited[node[0]]
        return ret

