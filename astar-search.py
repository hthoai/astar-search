import sys
from queue import PriorityQueue
from math import sqrt


class Cell:
    """
    Represents a position in map.

    A cell has X Y coordinates, its parent cell and some function's values.
    The coordinates of the top-left one is (0, 0).
    """

    def __init__(self, x=0, y=0, g=0.0, h=0.0, f=0.0, parent=None, parent_f=float('inf')):
        """
        Initialize a new cell with the given arguments.

        The new cell will automatically be assigned as above,
        with a parent_f attribute of positive infinity float.

        Arguments:
        x: The cell's x position.
        y: The cell's y position.
        g: The cost to move from the start cell to this cell.
        h: Heuristic - a function that estimates how close a cell is to the goal
        (use Euclidean distance).
        f: The cost to move from the start cell to this cell &
        the estimated cost to move from this cell to the goal (f = g+h).
        parent: Its parent cell - from that it's expanded.
        """
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent
        self.parent_f = parent_f

    def set_parent(self, parent):
        """Set parent for this cell."""
        self.parent = parent

    def compute_h_f(self, goal):
        """Compute h & f function, use Euclidean distance"""
        self.h = sqrt((goal.x-self.x)**2+(goal.y-self.y)**2)
        self.f = self.g+self.h

    def __lt__(self, other):
        """A cell with less f is  prioritized"""
        return self.f < other.f


def is_in_bounds(successor, N):
    """Check if a successor is in bounds"""
    (row, col) = successor
    return (row >= 0) and (row < N) and (col >= 0) and (col < N)


def is_destination(row, col, goal):
    """Check if a cell is goal"""
    return row == goal.x and col == goal.y


def a_star_search(outfile, grid, N, start, goal):
    """
    Implement A* search algorithm.

    At each step it picks the neighbour cell having the lowest f,
    and process that cell.

    Arguments:
    outfile: The file to write result in.
    grid: A 2D matrix includes the status of each cell
    (it is free or obstacle).
    N: The number of row/col in grid (row = col).
    start: The start cell.
    goal: The goal cell.
    """
    # Create a closed list and initialize it to false
    # which means that no cell has been included yet
    closed_list = [[False for x in range(N)] for y in range(N)]
    open_list = PriorityQueue()
    open_list.put(start)
    found_goal = False

    while not open_list.empty():
        q = open_list.get()
        closed_list[q.x][q.y] = True

        # Coordinates of 8-successors of a cell
        successors = [(q.x-1, q.y-1), (q.x, q.y-1), (q.x+1, q.y - 1), (q.x+1, q.y),
                      (q.x+1, q.y+1), (q.x, q.y+1), (q.x-1, q.y+1), (q.x-1, q.y)]

        for successor in successors:
            # Check if this successor is in bounds
            if is_in_bounds(successor, N) == True:
                temp = Cell(successor[0], successor[1])

                # Check if this successor is destination
                if is_destination(temp.x, temp.y, goal) == True:
                    temp.set_parent(q)
                    found_goal = True

                    u, v = goal.x, goal.y
                    road = []
                    maps = [['-' for x in range(N)]for y in range(N)]

                    for i in range(N):
                        for j in range(N):
                            if (grid[i][j] == 1):
                                maps[i][j] = 'o'

                    # Trace back to find the road from start to goal
                    while (u != start.x or v != start.y):
                        point = (u, v)
                        temp = temp.parent
                        road.append(point)
                        u = temp.x
                        v = temp.y
                    point = (start.x, start.y)
                    road.append(point)

                    outfile.write('%d\n' % len(road))

                    for i in range(len(road)):
                        (x, y) = road.pop()
                        maps[x][y] = 'x'
                        outfile.write('(%d, %d) ' % (x, y))
                    outfile.write('\n')

                    maps[start.x][start.y] = 'S'
                    maps[goal.x][goal.y] = 'G'

                    for i in range(N):
                        for j in range(N):
                            outfile.write('%c ' % maps[i][j])
                        outfile.write('\n')

                    return

                # The successor is not in Close List & not an obstacle
                elif (closed_list[temp.x][temp.y] == False) and (grid[temp.x][temp.y] == 0):
                    temp.g = q.g+1
                    temp.compute_h_f(goal)

                    if temp.parent_f == float('inf') or temp.parent_f > temp.f:
                        temp.parent_f = temp.f
                        temp.set_parent(q)
                        open_list.put(temp)

    if found_goal == False:
        outfile.write('-1')

    outfile.close()


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        N = int(next(f))
        start_x, start_y = map(int, next(f).split())
        goal_x, goal_y = map(int, next(f).split())
        grid = [[int(x)for x in line.split()]for line in f]
        f.close()

    start = Cell(start_x, start_y)
    goal = Cell(goal_x, goal_y)

    outfile = open(sys.argv[2], 'w')

    a_star_search(outfile, grid, N, start, goal)
