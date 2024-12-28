import numpy as np
import time
import matplotlib.pyplot as plt

from map import Map, get_map, Point

import heapq


class PQEntry:
    def __init__(self, dist, point):
        self.dist = dist
        self.point = point

    def __lt__(self, other):
        return self.dist < other.dist


def djikstras(map: Map, start_pos: Point, goal_pos: Point):
    # init PQ
    pq = [PQEntry(0, start_pos)]

    cost = np.full((map.width, map.height), np.inf)
    cost[start_pos.row][start_pos.col] = 0

    plt_idx = 0

    while pq:
        pqe = heapq.heappop(pq)

        # shortest distance to next point is infinite -- done
        if pqe.dist == np.inf:
            break

        new_dist = pqe.dist + 1

        # check all 4 directions
        for i in range(8):
            x = pqe.point.x + [0, 1, 0, -1, 1, 1, -1, -1][i]
            y = pqe.point.y + [1, 0, -1, 0, 1, -1, 1, -1][i]

            # check if in bounds
            if not map.in_bounds(x, y):
                continue

            # check if occupied
            if map.get_occupied(x, y):
                continue

            # check if new distance is less than current
            if new_dist < cost[y][x]:
                cost[y][x] = new_dist
                heapq.heappush(pq, PQEntry(new_dist, Point(x, y)))

        # display the cost map
        plt_idx += 1
        if (plt_idx % 50) != 0:
            continue

        plt_idx = 0

        plt.imshow(cost, cmap='hot_r', origin="lower")
        plt.show(block=False)
        plt.pause(0.1)
        # time.sleep(0.1)
        # plt.clf()

    # now we have the cost map
    print("Completed Djikstras")

    # now we need to backtrack to find the path
    path = []
    current = goal_pos
    while current != start_pos:
        path.append(current)

        # check all 4 directions
        min_cost = np.inf
        min_point = None
        for i in range(8):
            x = pqe.point.x + [0, 1, 0, -1, 1, 1, -1, -1][i]
            y = pqe.point.y + [1, 0, -1, 0, 1, -1, 1, -1][i]

            # check if in bounds
            if not map.in_bounds(x, y):
                continue

            # check if occupied
            if map.get_occupied(x, y):
                continue

            if cost[y][x] < min_cost:
                min_cost = cost[y][x]
                min_point = Point(x, y)

        current = min_point

    path.append(start_pos)
    path.reverse()

    return path



def sim_djikstras():
    print("Running: Djikstras")

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

    # run djikstras
    print("Running Djikstras")
    path = djikstras(map, start_pos, goal_pos)

    print("Path Found")

    # plot final path
    map.plot_path(path)

    print(f"Path of Length {len(path)}")



if __name__ == "__main__":
    sim_djikstras()