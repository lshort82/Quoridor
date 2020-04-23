import math, sys, time
import matplotlib.pyplot as plt
import copy

class Board:

    def __init__(self, n):
        self.p1_location = (0, math.floor(n/2))
        self.p2_location = (n - 1, math.floor(n/2))
        self.board, self.vertices = self.board_init(n)
        self.valid_walls = self.walls_init(n)
        self.p1_dist = self.dijkstras(self.board, self.p1_location, 'p1goal')
        self.p2_dist = self.dijkstras(self.board, self.p2_location, 'p2goal')

    def board_init(self, n):
        board = {'p1goal': {}, 'p2goal': {}}
        vertices = {'p1goal', 'p2goal'}
        for i in range(n):
            for j in range(n):
                vertices.add((i,j))
                board[(i,j)] = {}
                if i == 0:
                    board[(i,j)]['p2goal'] = 0
                elif i == n - 1:
                    board[(i,j)]['p1goal'] = 0
                if i > 0:
                    board[(i,j)][(i - 1, j)] = 1
                if i < n - 1:
                    board[(i,j)][(i + 1, j)] = 1
                if j > 0:
                    board[(i,j)][(i, j - 1)] = 1
                if j < n - 1:
                    board[(i,j)][(i, j + 1)] = 1
        return board, vertices

    #a wall is defined by the vertices below or to the left
    #an orientation of 1 is vertical, 0 horizontal
    def walls_init(self, n):
        walls = set()
        for i in range(n - 1):
            for j in range(n - 1):
                walls.add((0, (i, j), (i, j + 1)))
        for i in range(n - 1):
            for j in range(n - 1):
                walls.add((1, (i, j), (i + 1, j)))
        return walls

    #based on Dijkstras
    #p should be 1 or 2, corresponding to p1goal or p2goal
    def dijkstras(self, board, pos, goal):
        visited = {}
        left = {vertex: None for vertex in self.vertices}
        curr_dist = 0
        left[pos] = curr_dist
        while True:
            for neighbour, distance in board[pos].items():
                if neighbour not in left: continue
                new_dist = curr_dist + distance
                if left[neighbour] is None or left[neighbour] > new_dist:
                    left[neighbour] = new_dist
            visited[pos] = curr_dist
            del left[pos]
            if left is None or len(left) == 0: break
            new_vertices = [vertex for vertex in left.items() if vertex[1]]
            if len(new_vertices) == 0: break
            pos, curr_dist = sorted(new_vertices, key = lambda x: x[1])[0]
        return visited[goal]

    def find_best_move(self, p):
        if p == 1:
            pos = self.p1_location
            opp_pos = self.p2_location
            goal = 'p1goal'
            opp_goal = 'p2goal'
            dist = self.p1_dist
            opp_dist = self.p2_dist
        else:
            pos = self.p2_location
            opp_pos = self.p1_location
            goal = 'p2goal'
            opp_goal = 'p1goal'
            dist = self.p2_dist
            opp_dist = self.p1_dist
        curr_best_score = -sys.maxsize
        curr_best_moves = []
        for vertex in self.board[pos]:
            if vertex == 'p1goal' or vertex == 'p2goal':
                pass
            else:
                dist = self.dijkstras(self.board, vertex, goal)
                if opp_dist - dist > curr_best_score:
                    curr_best_score = opp_dist - dist
                    curr_best_moves = ["Move to: (" + str(vertex[0]) + ", " + str(vertex[1]) + ")"]
                elif opp_dist - dist == curr_best_score:
                    curr_best_moves.append("Move to: (" + str(vertex[0]) + ", " + str(vertex[1]) + ")")
        for wall in self.valid_walls:
            print(wall)
            new_board = copy.deepcopy(self.board)
            orientation = wall[0]
            for edge in wall[1:]:
                if orientation == 0:
                    del new_board[edge][(edge[0] + 1, edge[1])]
                    del new_board[(edge[0] + 1, edge[1])][edge]
                elif orientation == 1:
                    del new_board[edge][(edge[0], edge[1] + 1)]
                    del new_board[(edge[0], edge[1] + 1)][edge]
            dist = self.dijkstras(new_board, pos, goal)
            opp_dist = self.dijkstras(new_board, opp_pos, opp_goal)
            if opp_dist - dist > curr_best_score:
                curr_best_score = opp_dist - dist
                curr_best_moves = ["Place wall: " + wall]
            elif opp_dist - dist == curr_best_score:
                curr_best_moves.append("Place wall: " + wall)
        return curr_best_score, curr_best_moves


    def set_p1_location(self, pos):
        self.p1_location = pos

    def set_p2_location(self, pos):
        self.p2_location = pos

def main():
    ns = range(3, 20)
    runtimes = []
    for n in ns:
        board = Board(n)
        start_time = time.time()
        best_score, best_moves = board.find_best_move(1)
        end_tme = time.time()
        runtimes.append(end_tme - start_time)
        print("N = " + str(n) + " best score: " + str(best_score))
        print(best_moves)
    plt.plot(ns, runtimes)
    plt.title("Quoridor Optimal Move Calculation Time vs. Board Size")
    plt.xlabel("N-value")
    plt.ylabel("Runtime (Seconds)")
    plt.show()

if __name__ == "__main__":
    main()

