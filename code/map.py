import numpy as np
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.row = y
        self.col = x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # 2D array of widht and height, unoccupied
        # row, col
        # 0,0 is bottom left
        self.occupancy = np.zeros((width, height))  

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def draw_rect(self, start_x, start_y, width, height):
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                self.set_occupied(x, y)
    
    def set_occupied(self, x, y):
        if not self.in_bounds(x, y):
            return

        self.occupancy[y][x] = 1

    def get_occupied(self, x, y):
        if not self.in_bounds(x, y):
            return 1

        return self.occupancy[y][x]
    
    def plot_map(self):
        # plot the OGM
        plt.imshow(self.occupancy, cmap='gray_r', origin="lower")
        plt.show()
        pass

    def plot_path(self, path):
        # plot the OGM
        plt.imshow(self.occupancy, cmap='gray_r', origin="lower")

        # plot the path
        for point in path:
            plt.plot(point.x, point.y, 'ro')

        plt.show()



def get_map(map_idx) -> Map:
    if map_idx == "1":
        return get_map1()
    elif map_idx == "2":
        return get_map2()
    else:
        return None


# small 10x10 map
def get_map1():
    map1 = Map(10, 10)

    map1.draw_rect(1, 1, 2, 2)
    map1.draw_rect(5, 5, 2, 2)

    return map1

# large 100x100 map
def get_map2():
    map2 = Map(100, 100)

    # draw 10 rectangles
    map2.draw_rect(10, 10, 20, 20)
    map2.draw_rect(50, 50, 20, 20)
    map2.draw_rect(80, 80, 10, 10)
    map2.draw_rect(30, 70, 10, 10)
    map2.draw_rect(70, 30, 10, 10)
    map2.draw_rect(10, 80, 10, 10)
    map2.draw_rect(80, 10, 10, 10)


    return map2