"""
Mahesh Bharadwaj K
185001089

Assignment 4a : Center of Points using hill climb algorithm
"""

import random

class Point(object):
    __slots__ = ['x', 'y']


    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def distance(self, other):
        """
        Manhattan distance between points
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def successors(self):
        x = self.x
        y = self.y

        return Point(x+1, y), Point(x,y+1), Point(x-1, y), Point(x, y-1)

    def __str__(self):
        return f"X: {self.x}\tY: {self.y}"

    def __hash__(self):
        """
        Requried for set()
        """
        return hash(str(self.x)+str(self.y))

def computeCost(points: list, center: Point):
    """
    Total cost from center to all points given
    """
    cost = 0
    for pt in points:
        cost += pt.distance(center)

    return cost



def solve(points: list):
    """
    Hill climb implementation
    """
    x = random.randint(0, 30)
    y = random.randint(0, 30)

    center = Point(8, 9)
    # center = points[0]
    while True:
        better_found = False

        cost = computeCost(points, center)
        # print('Cost of center:  ', center, 'is: ', cost)
        for successor in center.successors():
            successor_cost = computeCost(points, successor)
            # print('Cost with ', successor, 'is: ', successor_cost)

            if successor_cost < cost:
                cost = successor_cost
                better_found=True
                center = successor

        if not better_found:
            break


    return center


def main():
    points  = [Point(1,1),Point(4,9),Point(5,2),Point(6,7)]
   
    # n = int(input('Enter the number of points: '))

    # points = set()

    # while True:
    #     x = random.randint(0, 30)
    #     y = random.randint(0, 30)

    #     points.add(Point(x, y))

    #     if len(points) == n:
    #         break
    

    print('The points are: ')
    for i, point in enumerate(points):
        print((i+1), point)

    print('The center is: %s' % (solve(list(points))))            

if __name__ == "__main__":
    main()

"""
OUTPUT:
-------
The points are: 
1 X: 1  Y: 1
2 X: 9  Y: 4
3 X: 4  Y: 6
4 X: 2  Y: 5
5 X: 7  Y: 7
The center is: X: 4     Y: 5
"""
