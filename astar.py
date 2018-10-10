from queue import Queue, PriorityQueue
from math import sqrt


class Cell:
    def __init__(self, x, y, g=0, h=0, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g+h

    def compute_h_f(self, goal):
        self.h = sqrt((goal.x-self.x)**2+(goal.y-self.y)**2)
        self.f = self.g+self.h

    def __lt__(self, other):
        return self.f > other.f


start = Cell(0, 0)
goal = Cell(6, 6)
N = 7

OpenList = PriorityQueue()
ClosedList = PriorityQueue()

OpenList.put(start)

while not OpenList.empty():
    q = OpenList.get()
    successors = []

    if (q.x-1) >= 0 & (q.y+1) < N:
        temp = Cell(q.x-1, q.y-1)
        successors.append(temp)
    if (q.y+1) < N:
        temp = Cell(q.x, q.y+1)
        successors.append(temp)
    if (q.x+1) < N & (q.y+1) < N:
        temp = Cell(q.x+1, q.y+1)
        successors.append(temp)
    if (q.x+1) < N:
        temp = Cell(q.x+1, q.y)
        successors.append(temp)
    if (q.x+1) < N & (q.y-1) >= 0:
        temp = Cell(q.x+1, q.y-1)
        successors.append(temp)
    if (q.y-1) >= 0:
        temp = Cell(q.x, q.y-1)
        successors.append(temp)
    if (q.x-1) >= 0 & (q.y-1) >= 0:
        temp = Cell(q.x-1, q.y-1)
        successors.append(temp)
    if (q.x-1) >= 0:
        temp = Cell(q.x-1, q.y)
        successors.append(temp)

    for s in successors:
        # Check if this successor is goal
        if (s.x == goal.x & s.y == goal.y):
            break
        else:
            # Compute g (distance between successor and q)
            s.g += 1
            # Compute h (distance from goal to successor) and f
            s.compute_h_f(goal)
        elif:
            
