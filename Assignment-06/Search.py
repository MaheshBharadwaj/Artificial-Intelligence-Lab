import heapq
import itertools
import matplotlib.pyplot as plt
import random

from helpers import to_convex_contour

plt.rcParams["figure.figsize"] = (10,10)

class Polygon(object):
    __slots__ = ['no_vertices', 'vertices', 'edges']

    def __init__(self, no_vertices, vertices):
        self.no_vertices = no_vertices
        self.vertices = vertices[:]
        self.create_edges()

    def create_edges(self):
        self.edges = []
        for i in range(0, len(self.vertices)-1):
            self.edges.append(Line(self.vertices[i], self.vertices[i+1]))
        self.edges.append(Line(self.vertices[-1], self.vertices[0]))

    def plot(self):
        vertices = self.vertices
        vertices.append(vertices[0])
        for i in range(len(vertices)-1):
            plt.plot([vertices[i][0], vertices[i+1][0]], [vertices[i][1], vertices[i+1][1]], 'b')


class Line(object):
    __slots__ = ['start', 'end']

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_intersecting(self , other):
        start_point, end_point = other.start, other.end

        if self.end[0] != self.start[0]:
            m_self =  (self.end[1] - self.start[1]) / (self.end[0] - self.start[0])
            c_self = self.end[1] - (m_self * self.end[0])

            # eqn of line is m x - y + c = 0

            sign_start = (start_point[0] * m_self) - start_point[1] + c_self
            sign_end = (end_point[0] * m_self ) - end_point[1] + c_self
        else:
            # eqn is x - c = 0
            c_self = self.end[0]
            sign_start = start_point[0] - c_self
            sign_end = end_point[0] - c_self

        if sign_start == 0 and sign_end == 0:
            return False
        
        sign_start = sign_start > 0
        sign_end = sign_end > 0

        return not sign_start == sign_end
    

    def length(self):
        return ((self.start[0] - self.end[0])**2 + (self.start[1] - self.end[1])**2)**0.5


class State(object):
    __slots__ = ['point', 'distance_from_start', 'goal', 'parent']

    def __init__(self, point, distance_from_start, goal, parent):
        self.point = point
        self.distance_from_start = distance_from_start
        self.goal = goal
        self.parent = parent

    def generate_successors(self, obstacles):
        line = Line(self.point, self.goal)
        if check_intersection(line, obstacles) == False:
            return [State(self.goal, self.distance_from_start + line.length(), self.goal, self)]

        successors = []
        # for obstacle in obstacles:
        #     for vertex in obstacle.vertices:
        #         line = Line(self.point, vertex)
        #         if check_intersection(line, obstacles) == False:
        #             successors.append(State(vertex, self.distance_from_start + line.length(), self.goal, self))
        for x_add, y_add in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if x_add == 0 and y_add == 0:
                continue
            new_point = (self.point[0] + x_add, self.point[1] + y_add)
            # if not valid_point(new_point, (0, 50), (0, 50)):
            #     continue
            line = Line(self.point, new_point)
            if check_intersection(line, obstacles) == False:
                successors.append(State(new_point, self.distance_from_start + line.length(), self.goal, self))
        
        return successors
        
    def heuristics(self):
        line = Line(self.point, self.goal)
        return self.distance_from_start + line.length()

    def goal_test(self):
        return self.point == self.goal

    def __lt__(self, other):
        return self.heuristics() < other.heuristics()
    
    def __gt__(self, other):
        return self.heuristics() > other.heuristics()

    def __str__(self):
        return str(self.point)

    def __hash__(self):
        s = str(self.point)
        return hash(s)

def generate_obstacles():
    epsison = 0.3
    obstacle_list = []
    for i in range(0,5):
        for j in range(0,5):
            if random.uniform(0, 1) < epsison:
                continue
            # if i == 0 and j == 0:
            #     continue
            sides = random.randint(3,5)
            vertices = to_convex_contour(sides,((i*10)+1, (i+1)*10 - 2), ((j*10)+1, (j+1)*10 - 2) )
            obstacle_list.append(Polygon(sides, vertices))

    return obstacle_list

def valid_point(point, x_lim, y_lim):
    if point[0] < x_lim[0] or point[0] > x_lim[1] or point[1] < y_lim[0] or point[1] > y_lim[1]:
        return False
    return True


def plot_polygons(polygons, start, end):
    plt.scatter([start[0], end[0]], [start[1], end[1]], c='g')
    for polygon in polygons:
        polygon.plot()
    # for i in range(len(route) - 1):
    #     plt.plot([route[i][0], route[i+1][0]], [route[i][1], route[i+1][1]], 'r--')    

    plt.annotate('Source', start)
    plt.annotate('Goal', end)    
    plt.savefig('op.png')



def check_intersection(line, obstacles):
    edges = [edge for obstacle in obstacles for edge in obstacle.edges ]
    for edge in edges:
        if line.is_intersecting(edge):
            return True
    return False
    


def solve(start_point, goal_point, obstacles):
    start_state = State(start_point, 0.0, goal_point, None)

    bag_of_states = []
    explored = set()
    heapq.heappush(bag_of_states, start_state)

    while len(bag_of_states):
        current_state = heapq.heappop(bag_of_states)
        explored.add(current_state)

        if current_state.goal_test():
            return current_state, True

        for next_state in current_state.generate_successors(obstacles):
            if next_state not in explored:
                heapq.heappush(bag_of_states, next_state)

    if len(bag_of_states):
        return heapq.heappop(bag_of_states), False
    return None, False


def get_path(cur_state, points):
    if cur_state.parent is None:
        points = [cur_state.point] + points
        return points
    points = [cur_state.point] + points
    return get_path(cur_state.parent, points)

start_point = (0, 0)
end_point = (50, 50)
obstacles = generate_obstacles()
end_state, solution = solve(start_point, end_point, obstacles)

if solution:
    path = get_path(end_state, [])
    for i in range(len(path)-1):
        plt.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]], 'r--')
    print('Path: ' + str(path))
    print('Cost: ' + str(end_state.distance_from_start))
else:
    # if end_state is not None:
    #     path = get_path(end_state, [])
    #     for i in range(len(path)-1):
    #         plt.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]], 'r--')
    print('No solution!')

plot_polygons(obstacles, start_point, end_point)
