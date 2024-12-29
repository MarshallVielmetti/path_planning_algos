from map import Map, Point, get_map
import numpy as np

import matplotlib.pyplot as plt
import heapq


class PQEntry:
    h = None
    g = None
    def __init__(self, point):
        self.point = point

    def get_h(self):
        return PQEntry.h[self.point.row][self.point.col]
    
    def get_g(self):
        return PQEntry.g[self.point.row][self.point.col]

    def __lt__(self, other):
        self_cost = self.get_g() + self.get_h()
        other_cost = other.get_g() + other.get_h()

        return self_cost < other_cost



def reconstruct_path(came_from, current: Point):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()

    return path

def astar(map, start: Point, goal: Point):
    frontier = []

    n, m = map.occupancy.shape
    y, x = np.ogrid[:n, :m]
    h = np.floor(np.sqrt((x - goal.x)**2 + (y - goal.y)**2))

    PQEntry.h = h
    PQEntry.g = np.full((n, m), np.inf)
    PQEntry.g[start.row][start.col] = 0

    # map from point to parent point
    came_from = {}

    frontier = [PQEntry(start)]

    plot_idx = 0

    while frontier:
        curr = heapq.heappop(frontier)
        print(curr.point.x, curr.point.y)
        if (curr.point == goal):
            print("found path")
            return reconstruct_path(came_from, curr.point)
        
        for i in range(8):
            x = curr.point.x + [0, 1, 0, -1, 1, 1, -1, -1][i]
            y = curr.point.y + [1, 0, -1, 0, 1, -1, 1, -1][i]

            if not map.in_bounds(x, y):
                continue

            if map.get_occupied(x, y):
                continue

            new_cost = PQEntry.g[curr.point.row][curr.point.col] + 1
            if new_cost < PQEntry.g[y][x]:
                PQEntry.g[y][x] = new_cost
                heapq.heappush(frontier, PQEntry(Point(x, y)))
                came_from[Point(x, y)] = curr.point

        plot_idx += 1
        if (plot_idx % 50) != 0:
            continue
        plot_idx = 0

        plt.imshow(PQEntry.g, cmap='hot_r', origin="lower")
        plt.show(block=False)
        plt.pause(0.00001)



    # failed to find path
    print("Failed to find path")
    return None


def sim_astar():
    print("Running: AStar")

    map_idx = input("Enter Desired Map:")
    map = get_map(map_idx)

    print("Enter Start Position:")
    start_x = int(input("X: "))
    start_y = int(input("Y: "))
    start_pos = Point(start_x, start_y)

    print("Enter Goal Position:")
    goal_x = int(input("X: "))
    goal_y = int(input("Y: "))
    goal_pos = Point(goal_x, goal_y)

    # validate
    if map.get_occupied(start_x, start_y) or map.get_occupied(goal_x, goal_y):
        print("Invalid Start or Goal Position")
        return

    map.plot_map()

    # run astar
    print("Running AStar")
    path = astar(map, start_pos, goal_pos)

    # plot final path
    map.plot_path(path)

    print(f"Path of Length {len(path)}")



if __name__ == "__main__":
    sim_astar()