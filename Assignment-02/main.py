"""
Mahesh Bharadwaj K
185001089
Assignment 02: State Space Search - Decantation Problem 

FORMULATION
-----------

1. State:
   Each state represents the amount of water present in each jar
   and capacity of jar.

2. Actions:
   Completely empty a jar into another jar with space or completely
   fill up a jar from another jar. 

3. Initial State:
   8L in 8L jar
   0L in 5L and 3L jars

4. Goal State:
   4L in 8L jar
   1L in 5L jar
   3L in 3L jar

4. Sucessor State:
   States obtained by applying action(pouring) to current state.

"""

import copy

class jar(object):
    __slots__ = ['cur', 'max']

    def __init__(self, cur, max):
        self.cur = cur
        self.max = max

    def __eq__(self, other):
        if self.cur == other.cur and self.max == other.max:
            return True
        return False
    
    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.cur)

    def __hash__(self):
        return hash((self.cur, self.max))

    def isFull(self):
        return self.cur == self.max

    def spaceLeft(self):
        return self.max - self.cur

   

class state(object):

    __slots__ = ['jars', 'parent']

    def __init__(self, jars, parent=None):
        self.jars = jars
        self.parent = parent

    def __eq__(self, other):
        flag = True
        for i in range(3):
            if self.jars[i] != other.jars[i]:
                flag = False
                break

        return flag

    def __str__(self):
        s = "("
        for jar in self.jars:
            s += str(jar) + ', '
        s = s[:-2]
        s += ')'
        return s    

    def __hash__(self):
        return hash(self.jars)


def next_states(curr_state):
    next = []
    

    for i in range(len(curr_state.jars)):
        for j in range(len(curr_state.jars)):
            if i == j:
                continue
            jars_temp = copy.deepcopy(curr_state.jars)
            
            #No capacity left to transfer from jar 'i'
            if jars_temp[i].cur <= 0:
                break
            if jars_temp[j].spaceLeft() > 0:
                avail = jars_temp[j].spaceLeft()

                if jars_temp[i].cur < avail:
                    jars_temp[j].cur += jars_temp[i].cur 
                    jars_temp[i].cur = 0

                else:
                    jars_temp[j].cur += avail
                    jars_temp[i].cur -= avail

                next.append(state(jars_temp, parent=curr_state))

    return next

initial_state = state( (jar(8, 8), jar(0, 5), jar(0, 3)))
goal_state = state( (jar(4, 8), jar(1, 5), jar(3, 3)))


#Testing next_state function
# for next_state in next_states(initial_state):
#     print(next_state)


def print_steps(current_state):

    #Base case, this is the root state
    if current_state.parent is None:
        print(current_state)
        return
    
    #Recursive step
    print_steps(current_state.parent)
    print(current_state)



def bfs(initial_state, goal_state,trace=False):
    visited = set()

    states = []
    states.append(initial_state)

    while len(states) != 0:
        if trace:
            print('Queue Contents:')
            for s in states:
                print(s, end=' ')
            print()

        current_state = states.pop(0)
        if current_state == goal_state:
            print("Found Goal State!\nPrinting steps: ")
            print_steps(current_state)
            break
        successors = next_states(current_state)

        for new_state in successors:
            if new_state not in visited:
                visited.add(new_state)
                states.append(new_state)
            else:
                #Duplicate state
                pass

#trace = True for queue contents
bfs(initial_state, goal_state,trace=True)


"""
OUTPUT:
-------

mahesh@mahesh-PC:~/Documents/Artificial-Intelligence/Assignment-02$ python3 main.py 
Queue Contents:
(8, 0, 0) 
Queue Contents:
(3, 5, 0) (5, 0, 3) 
Queue Contents:
(5, 0, 3) (0, 5, 3) (8, 0, 0) (3, 2, 3) 
Queue Contents:
(0, 5, 3) (8, 0, 0) (3, 2, 3) (5, 3, 0) 
Queue Contents:
(8, 0, 0) (3, 2, 3) (5, 3, 0) 
Queue Contents:
(3, 2, 3) (5, 3, 0) 
Queue Contents:
(5, 3, 0) (6, 2, 0) 
Queue Contents:
(6, 2, 0) (2, 3, 3) 
Queue Contents:
(2, 3, 3) (6, 0, 2) 
Queue Contents:
(6, 0, 2) (2, 5, 1) 
Queue Contents:
(2, 5, 1) (1, 5, 2) 
Queue Contents:
(1, 5, 2) (7, 0, 1) 
Queue Contents:
(7, 0, 1) (1, 4, 3) 
Queue Contents:
(1, 4, 3) (7, 1, 0) 
Queue Contents:
(7, 1, 0) (4, 4, 0) 
Queue Contents:
(4, 4, 0) (4, 1, 3) 
Queue Contents:
(4, 1, 3) 
Found Goal State!
Printing steps:
(8, 0, 0)
(5, 0, 3)
(5, 3, 0)
(2, 3, 3)
(2, 5, 1)
(7, 0, 1)
(7, 1, 0)
(4, 1, 3)
"""