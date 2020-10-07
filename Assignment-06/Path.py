# Problem Formulation

# - The source and goal states are represented as co-ordinates in a 2-D space.
# - The source is at co-ordinate (0, 0) and goal at co-ordinate (50, 50).
# - Since every obstacle in the path is a polygon, it can be represented as a set of vertices as co-ordinates.
# - The outline of each obstacle is represented by a pair of vertices, to represent each edge of the polygon. 
# - The Euclidean distance between each point, is considered as the distance.
# - The robot can move from one point to another, provided that there is a straight line segment between the two points, that does not intersect with any other object, at the cost of the distance between them. 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import math

class Obstacle():
    def __init__(self, no_vertices, vertices):
        self.no_vertices = no_vertices
        self.vertices = [i for i in vertices]
        self.edges = []
        
    def create_edges(self):
        self.edges = []
        for i in range(0, len(self.vertices)-1):
            self.edges.append((self.vertices[i], self.vertices[i+1]))
        self.edges.append((self.vertices[-1], self.vertices[0]))


source = (0, 0)
goal = (50, 50)


def create_obstacles():
    obstacle_list = []
    for i in range(5):
        for j in range(5):
            vertices = []
            edges = []
            sides = random.randint(3,4)
            for k in range(sides):
                x,y = random.randint((i*10)+1, (i+1)*10 - 2), random.randint((j*10)+1, (j+1)*10 - 2)
                vertices.append((x,y))
            obj = Obstacle(sides, vertices)
            obj.create_edges()
            obstacle_list.append(obj)
    return obstacle_list

obstacle_list = create_obstacles()

vertex_points = [j for i in obstacle_list for j in i.vertices]
vertex_points.append(source)
vertex_points.append(goal)
edge_lines = [j for i in obstacle_list for j in i.edges]


def show_layout():
    for i in range(0, 51):
        if i % 10 == 0 and i != 50:
            print("-"*101)
        for j in range(0, 51):
            if (i,j) == source:
                print("S", end = " ")
            elif (i,j) == goal:
                print("G", end = " ")
            elif j%10 == 0:
                print("|", end = " ")
            elif (i,j) in vertex_points:
                print(".", end = " ")
            else:
                print(" ", end = " ")
        print()
        if i == 50:
            print("-"*101)


show_layout()


# ### There are two possibilities when two line segments A, B do not intersect:
# * End points of A lie on the same side of line extended from B.
# * End points of B lie on the same side of line extended from A.



#Return True if no intersection, else False
def check_intersection(new_line, existing_line):
    for i in new_line:
        if i in existing_line:
            return True
    #Check if endpoints of new line lie on same side of existing line 
    x1, y1, x2, y2 = existing_line[0][0], existing_line[0][1], existing_line[1][0], existing_line[1][1]
    if x2!=x1:
        m = (y2 - y1)/(x2 - x1) 
    #Eqn is (y-y1) = m*(x-x1) => m*(x-x1) - (y-y1) = 0
    #Substituting values for x, y
    x, y = new_line[0][0], new_line[0][1]
    if x1==x2:
        val = (x-x1)
    else:
        val = (m*(x-x1) - (y-y1))
    if val == 0:
        return False
    r1 = True if val>0 else False
    x, y = new_line[1][0], new_line[1][1]
    if x1==x2:
        val = (x-x1)
    else:
        val = (m*(x-x1) - (y-y1))
    if val == 0:
        return False
    r2 = True if val>0 else False
    result = (r1 == r2)
    if not result:
        #Check if endpoints of existing line lie on same side of new line
        x1, y1, x2, y2 = new_line[0][0], new_line[0][1], new_line[1][0], new_line[1][1]
        if x2!=x1:
            m = (y2 - y1)/(x2 - x1)
        #Eqn is (y-y1) = m*(x-x1) => m*(x-x1) - (y-y1) = 0
        #Substituting values for x, y
        x, y = existing_line[0][0], existing_line[0][1]
        if x1==x2:
            val = (x-x1)
        else:
            val = (m*(x-x1) - (y-y1))
        if val == 0:
            return False
        r1 = True if val>0 else False
        x, y = existing_line[1][0], existing_line[1][1]
        if x1==x2:
            val = (x-x1)
        else:
            val = (m*(x-x1) - (y-y1))
        if val == 0:
            return False
        r2 = True if val>0 else False
        result = (r1 == r2)
    return result


#Heuristic is SLD from point to goal
def compute_heuristic(dist_travelled, point, goal):
    g_n = dist_travelled
    h_n = math.sqrt((goal[0]-point[0])**2 + (goal[1]-point[1])**2) 
    f_n = g_n + h_n
    return f_n



def successor_states(point, dist_travelled, goal):
    successors = []
    for vertex in vertex_points:
        flag = True
        if vertex != point:
            new_line = (point, vertex)
            if new_line not in edge_lines:
                for edge in edge_lines:
                    if not check_intersection(new_line, edge):
                        flag = False
                        break
            if not flag:
                continue
            successors.append(vertex)
    return successors


def next_state(point, dist_travelled, goal):
    successors = successor_states(point, dist_travelled, goal)
    min_vertex = (0,0)
    min_cost = 10000
    for p in successors:
        dist = math.sqrt((p[0]-point[0])**2 + (p[1]-point[1])**2)
        fitness = compute_heuristic(dist_travelled+dist, p, goal)
        if fitness < min_cost:
            min_cost = fitness
            min_vertex = p
    return min_vertex, min_cost


next_state((0,0), 0, (50, 50))

def route_find(start, end):
    node = start
    dist = 0
    route = [node]
    while node != end and len(route)<len(vertex_points):
        node, dist = next_state(node, dist, end)
        if node in route:
            print("Goal cannot be reached. ")
            return False
        route.append(node)
    cost = 0
    for i in range(len(route)-1):
        cost += math.sqrt((route[i+1][0]-route[i][0])**2 + (route[i+1][1]-route[i][1])**2)
    cost += math.sqrt((route[-2][0]-route[-1][0])**2 + (route[-2][1]-route[-1][1])**2)
    return route, cost

route, cost = route_find(source, goal)
print("The route taken is "+str(route)+" at cost "+str(cost))


def plot_image(obstacles, route):
    plt.scatter([source[0], goal[0]], [source[1], goal[1]], c='g')
    for obstacle in obstacles:
        vertices = obstacle.vertices
        vertices.append(vertices[0])
        for i in range(len(vertices)-1):
            plt.plot([vertices[i][0], vertices[i+1][0]], [vertices[i][1], vertices[i+1][1]], 'b')

    for i in range(len(route) - 1):
        plt.plot([route[i][0], route[i+1][0]], [route[i][1], route[i+1][1]], 'r--')    

    plt.annotate('Source', source)
    plt.annotate('Goal', goal)    
    plt.savefig('op.png')

plot_image(obstacle_list, route)

'''
Output:
-----------------------------------------------------------------------------------------------------
S                   |                   |                   |                   |                   | 
|                   |           .       |                   |                   |                   | 
|                   |               .   |           .       |                   |   .   .   . .     | 
|                   |                   |                   |     . .   .       |                   | 
|                   |             .     |   . .             |                   |       .           | 
|           .       | .                 |                   |             .     |                   | 
|     .             |                   |                   |                   |                   | 
|       .           |                   |       .           |                   |         .         | 
|                   |     .             |                   |         .         |                   | 
|                   |                   |                   |                   |                   | 
-----------------------------------------------------------------------------------------------------
|                   |                   |                   |                   |                   | 
|       .           |     .             |         .         |                   |                   | 
| .                 |                   |                   |                   |                   | 
|         .         | .       .         |           .       | . .               |             .     | 
|                   |             .     |                   |                   |                   | 
|           .       |       .           |                   |                   | .       .         | 
|                   |                   |       .           |   .               |                   | 
|                   |                   |             .     |                   |                   | 
|                   |                   |   .               |                   |                   | 
|                   |                   |                   |                   |                   | 
-----------------------------------------------------------------------------------------------------
|                   |                   |                   |                   |                   | 
|       .           |                   |                   |               .   |                   | 
|                   |             . .   |                   |                   |                   | 
|     .         .   |                   |     .             | .         .   .   |                   | 
|                   |                   |             .     |                   |         . .       | 
|                   |   .               |                   |                   |               .   | 
|                   |                   |                   |               .   |                   | 
|                   |                   | .                 |     .             | .   .             | 
|                   |                   |         .         |                   |                   | 
|                   |                   |                   |                   |                   | 
-----------------------------------------------------------------------------------------------------
|                   |                   |                   |                   |                   | 
|                   |                   |           . .     | .                 |             .     | 
|                   |                   |                   |                   |               .   | 
|                   | .                 |                   |   .               |   .               | 
|                   | .                 |                   |   .               |       .   .       | 
|                   |     .             |                   |             .     |                   | 
|       .           |                   |                   |                   |                   | 
|                   |   .               |     .   .         |               .   |                   | 
|             . .   | .     .           |           .       |                   |                   | 
|                   |                   |                   |                   |                   | 
-----------------------------------------------------------------------------------------------------
|                   |                   |                   |                   |                   | 
|                   |                   |               .   |         .         |                   | 
|           .       |     .       .     |                   |                   |                   | 
| .                 |                   |                   |                   |             .     | 
|           .       |             .     | .         .       |                   |                   | 
|                   |                   |       .           |                   |     . .           | 
| .                 |                   |                   |                   |   .               | 
|                   |                   |           .   .   |   .       .       |             .     | 
|           .       |                   |                   |   .     . .       |                   | 
|                   |                   |                   |                   |                   | 
|                   |                   |                   |                   |                   G 
-----------------------------------------------------------------------------------------------------
The route taken is [(0, 0), (18, 22), (24, 27), (33, 42), (34, 44), (50, 50)]at cost 90.14052912631625
'''
