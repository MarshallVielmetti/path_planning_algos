from map import Map, Point, get_map

import numpy as np
import matplotlib.pyplot as plt

# solution radius
RAD = 10
dt = 0.1


def backtrace(V, E):
    # find the goal node
    goal = V[-1]

    # backtrace to find the path
    path = [goal]

    while goal != V[0]:
        for e in E:
            if e[1] == goal:
                goal = e[0]
                path.append(goal)
                break

    path.reverse()

    return path

def plot_tree(V, E, map: Map, goal: Point, path=None):
    plt.imshow(map.occupancy, cmap='gray_r', origin="lower")

    # plot edges
    for e in E:
        plt.plot([e[0].x, e[1].x], [e[0].y, e[1].y], 'r-')

    # plot vertices
    for v in V:
        plt.plot(v.x, v.y, 'ro', markersize=2)

    # plot goal as point with circle radius patch
    circle = plt.Circle((goal.x, goal.y), RAD, color='g', fill=False)
    plt.gca().add_artist(circle)

    if path:
        # plot solution path
        for i in range(len(path) - 1):
            plt.plot([path[i].x, path[i+1].x], [path[i].y, path[i+1].y], 'g-')
        
        plt.show()
        return

    plt.show(block=False)
    plt.pause(0.0001)

def rrt(map: Map, start_pos: Point, goal_pos: Point):
    # create the graph
    V = [start_pos]
    E = []

    plot_idx = 0
    plot_freq = 25

    while True:
        # sample a random point
        x_rand = Point(np.random.random() * map.width, np.random.random() * map.height)

        # find the nearest point in the graph
        x_nearest = V[0]
        min_dist = np.inf
        for v in V:
            dist = (v.x - x_rand.x)**2 + (v.y - x_rand.y)**2 # don't need to sqrt
            if dist < min_dist:
                min_dist = dist
                x_nearest = v

        # move towards the random point
        # get vector from nearest to random
        vec = Point(x_rand.x - x_nearest.x, x_rand.y - x_nearest.y)

        # sampled already selected point
        if vec.x == 0 and vec.y == 0:
            continue

        # normalize
        vec_len = np.sqrt(vec.x**2 + vec.y**2)
        vec = Point(vec.x / vec_len, vec.y / vec_len) 


        # scale
        scale = 5
        vec = Point(int(vec.x * scale), int(vec.y * scale))

        # nearest plus normed vec
        x_new = Point(x_nearest.x + vec.x, x_nearest.y + vec.y)

        # check if new point is occupied
        if map.get_occupied(int(x_new.x), int(x_new.y)):
            continue # invalid point selected

        # add to graph
        V.append(x_new)
        E.append((x_nearest, x_new))

        # plot graph (every x iterations)
        plot_idx += 1
        if plot_idx % plot_freq == 0:
            plot_tree(V, E, map, goal_pos)
            plot_idx = 0

        # check if we are close to the goal
        if (x_new.x - goal_pos.x)**2 + (x_new.y - goal_pos.y)**2 < RAD**2:
            break

    return (V, E)

def sim_rrt():
    print("Running: RRT")

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


    # run rrt
    print("Running RRT")
    V, E = rrt(map, start_pos, goal_pos)

    path = backtrace(V, E)
    plot_tree(V, E, map, goal_pos, path)

    # backtrace to find path

    # plot final path
    # map.plot_map()

    # plot final path
    # map.plot_path(path)



if __name__ == "__main__":
    sim_rrt()
