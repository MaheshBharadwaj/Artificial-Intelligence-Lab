import numpy as np
import heapq as heap
import copy
from enum import Enum
from os import system

class heuristic(Enum):
    NONE = 0
    BEST_FIRST = 1
    A_STAR = 2 


#Maps element to its i, j value in the goal state (eg 8 is at 2, 2)
actual_position = [(),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

class state(object):
    def __init__(self,parent=None, state=None, depth=None, a_p=None, h=heuristic.NONE):
        self.parent = parent
        self.state = state
        self.depth = depth
        self.h = h
        self.actual_position = a_p

    def heuristic_fn(self):
        if self.h == heuristic.NONE:
            return -1
        
        count = 0
        
        # Adding depth of state as it is equal to number of steps taken
        # To reach the current state from start state
        if self.h == heuristic.A_STAR:
            count += self.depth

        sequence = self.state

        # Calculate manhattan distance of all misplaced tiles 
        for i in range(3):
            for j in range(3):
                if sequence[i][j] != 0:
                    actual_loc = self.actual_position[sequence[i][j]]
                    count = count +  (abs(actual_loc[0] - i)  + abs(actual_loc[1] - j))
        return count

    def generate_states(self):

        sequence = self.state
        space_i = -1
        space_j = -1

        # Finding where the empty space is located
        for i in range(3):
            for j in range(3):
                if sequence[i][j] == 0:
                    space_i = i
                    space_j = j

        # Each of the 4 represents left, right, bottom and 
        # top cells' offset from space cell
        for row_add,col_add in [(-1,0),(1,0),(0,1),(0,-1)]:
                temp_sequence = copy.deepcopy(sequence)
                if space_i + row_add >= 0 and space_i + row_add < 3\
                   and space_j + col_add >= 0 and space_j + col_add < 3:
                    temp_sequence[space_i][space_j],temp_sequence[space_i + row_add][space_j + col_add]=\
                    temp_sequence[space_i + row_add][space_j + col_add],temp_sequence[space_i][space_j]

                    yield state(self,temp_sequence,self.depth + 1,self.actual_position, self.h)


    def is_goal(self):
        count = 0
        sequence = self.state
        for i in range(3):
            for j in range(3):
                if sequence[i][j] != 0:
                    actual_loc = self.actual_position[sequence[i][j]]
                    count = count +  (abs(actual_loc[0] - i)  + abs(actual_loc[1] - j))

        if count == 0:
            return True
        return False


    def __str__(self):
        return '\nState:\n' + str(self.state) + '\nDepth: ' + str(self.depth)

    def __lt__(self,other):
        return self.heuristic_fn() < other.heuristic_fn()
    
    def __gt__(self,other):
        return self.heuristic_fn() > other.heuristic_fn()
    
    def __eq__(self,other):
            for j in range(3):
                if self.state[i][j] != other.state[i][j]:
                    return False
        return True

    def __hash__(self):
        return hash(self.state.tostring())





def print_path(s):
    # Base case: when parent is None, it is the start state.
    if s.parent is None:
        print(str(s))
        return
    
    print_path(s.parent)
    print(str(s))

def solve_dfs(init_state, actual_position):
    # Creating initial state from input sequence
    start_state = state(parent=None, state=init_state, depth=1, a_p=actual_position)

    discovered = [start_state]
    explored = set()

    while len(discovered):
        current_state = discovered.pop(0)

        if current_state.is_goal():
            print_path(current_state)
            return 
        
        explored.add(current_state)

        for successor_state in current_state.generate_states():
            if successor_state in explored:
                continue
            
            discovered.append(successor_state)


def solve_informed(init_state, actual_position,h):
    start_state = state(None, init_state, 1, actual_position,h)

    discovered = [start_state]
    explored = set() 

    while len(discovered):

        # Pop from priority queue
        current_state = heap.heappop(discovered)

        if current_state.is_goal():
            print_path(current_state)
            return 

        explored.add(current_state)

        for successor_state in current_state.generate_states():
            if successor_state in explored:
                continue
            
            # Push to priority queue
            heap.heappush(discovered, successor_state)

opt = -1
l = []

for i in range(3):
    l.append(list(map(int,input().split(' '))))
    
input_array = np.array(l)
while opt != 4:
    system('clear')
    print('1 - Uninformed\n2 - BFS\n3 - A*\n4- exit\nEnter option: ')
    opt = int(input())

    if opt == 1:
        solve_dfs(input_array, actual_position)
    elif opt == 2:
        solve_informed(input_array, actual_position, heuristic.BEST_FIRST)
    elif opt == 3:
        solve_informed(input_array, actual_position, heuristic.A_STAR)
    elif opt == 4:
        break
    else:
        print('Invalid Input!')
    
    print('Press ANY key to continue....')
    input()
    
        