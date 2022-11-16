import math
import copy
from pathlib import Path
import time


class Graph:
    # Helpers:
    def zero_to_inf(self):
        for i in range(0, self.verteces):
            for j in range(0, self.verteces):
                if self.graph[i][j] == 0:
                    self.graph[i][j] = math.inf

    def fill_matrix(self, f):
        for i in range(self.verteces):
            a = []
            line = f.readline().split()
            for j in range(self.verteces):
                a.append(int(line[j]))
            self.graph.append(a)

        self.zero_to_inf()

    def write_result(self, distances):
        outfile = Path('output.txt')
        outfile.touch(exist_ok=True)

        f = open(outfile, 'w')
        for i in range(0, self.verteces - 1):
            f.write(str(' '.join([str(distances[i])])) + ", ")
        f.write(str(' '.join([str(distances[self.verteces - 1])])) + "")
        f.close()

    def write_result_matrix(self, tmp_graph):
        outfile = Path('output.txt')
        outfile.touch(exist_ok=True)

        f = open(outfile, 'w')
        for i in range(self.verteces):
            f.write(str(' '.join([str(x) for x in tmp_graph[i]])) + "\n")
        f.close()

    # Main funcs:
    def __init__(self, filename):
        f = open(filename, 'r')
        self.verteces = int(f.readline())
        self.graph = []
        self.fill_matrix(f)

        f.close()

    def run_dijkstra(self):
        tmp_graph = copy.deepcopy(self.graph)
        distances = [math.inf] * self.verteces
        already_proceeded_verteces = [1] * self.verteces

        ver = int(input("Enter the first vertex's index:\n"))
        if ver < 0 or ver > self.verteces - 1:
            exit("Wrong vertex index.")

        begin = time.time()
        distances[ver] = 0
        min_idx = 0
        while min_idx < math.inf:
            min_idx = math.inf
            _min = math.inf
            for i in range(0, self.verteces):
                if already_proceeded_verteces[i] == 1 and distances[i] < _min:
                    _min = distances[i]
                    min_idx = i

            if min_idx != math.inf:
                for i in range(0, self.verteces):
                    if tmp_graph[min_idx][i] > 0:
                        temp = _min + tmp_graph[min_idx][i]
                        if temp < distances[i]:
                            distances[i] = temp
                already_proceeded_verteces[min_idx] = 0

        end = time.time()
        print(f"Total runtime of the function is {end - begin} seconds.")

        self.write_result(distances)

        del tmp_graph

    def run_ford_bellman(self):
        tmp_graph = copy.deepcopy(self.graph)
        distances = [math.inf] * self.verteces

        ver = int(input("Enter the first vertex's index:\n"))
        if ver < 0 or ver > self.verteces - 1:
            exit("Wrong vertex index.")

        begin = time.time()
        distances[ver] = 0
        for k in range(0, self.verteces - 1):
            for i in range(0, self.verteces):
                for j in range(0, self.verteces):
                    if distances[j] > distances[i] + tmp_graph[i][j] and distances[i] != math.inf:
                        distances[j] = distances[i] + tmp_graph[i][j]

        for k in range(0, self.verteces - 1):
            for i in range(0, self.verteces):
                for j in range(0, self.verteces):
                    if distances[j] > distances[i] + tmp_graph[i][j] and distances[i] != math.inf:
                        exit("Found negative weight cycle in the given graph.")

        end = time.time()
        print(f"Total runtime of the function is {end - begin} seconds.")

        self.write_result(distances)

    def run_floyd_warshall(self):
        tmp_graph = copy.deepcopy(self.graph)

        begin = time.time()

        for k in range(0, self.verteces):
            for i in range(0, self.verteces):
                for j in range(0, self.verteces):
                    if i == j:
                        continue
                    if tmp_graph[i][k] < math.inf and tmp_graph[k][j] < math.inf:
                        tmp_graph[i][j] = min(tmp_graph[i][j], tmp_graph[i][k] + tmp_graph[k][j])

        end = time.time()
        print(f"Total runtime of the function is {end - begin} seconds.")

        self.write_result_matrix(tmp_graph)

        del tmp_graph


def main():
    g = Graph("test5.txt")
    g.run_dijkstra()


if __name__ == "__main__":
    main()
