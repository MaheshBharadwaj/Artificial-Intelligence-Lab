"""
Mahesh Bharadwaj K
185001089

Assignment 4a : 8 Queens problem using hill climb algorithm

"""
from random import shuffle
import copy


class State(object):
    """
    State is represented as array of 8 integers
    eg [1, 2, 5, 8, 7, 4, 3, 6]
    signifies:
    column 1 has queen in row 1
    column 2 has queen in row 2
    column 3 has queen in row 5
    
    ie array indices represent columns, and the value in that
    location represents the row in which queen is present
    """
    __slots__ = ['seq']

    def __init__(self, seq:list):
        self.seq = copy.copy(seq)

    def attacking_pairs(self):
        pairs = 0
        for i in range(8):
            for j in range(8):
                if i == j:
                    continue
                #Same row
                if self.seq[i] == self.seq[j]:
                    pairs += 1
                #Diagonal Cases
                elif self.seq[i] - i == self.seq[j] - j:
                    pairs +=1
                elif self.seq[i] + i == self.seq[j] + j:
                    pairs += 1
                else:
                    pass
        return pairs
    
    def successors(self):
        next = []
        
        for i in range(8):
            #Top most row
            if self.seq[i] == 8:
                tmp_seq = copy.copy(self.seq)
                tmp_seq[i] -= 1
                next.append(State(tmp_seq))
            #Bottom most row
            elif self.seq[i] == 1:
                tmp_seq = copy.copy(self.seq)
                tmp_seq[i] += 1
                next.append(State(tmp_seq))
            else:
                tmp_seq = copy.copy(self.seq)
                tmp_seq[i] -= 1
                next.append(State(tmp_seq))
                tmp_seq = copy.copy(self.seq)
                tmp_seq[i] += 1
                next.append(State(tmp_seq))
        return next
    
    def __str__(self):
        return 'State: ' + str(self.seq) +\
                '\nAttacked Pairs: ' + str(self.attacking_pairs())

    

def solve(start_state: State):

    while True:
        current_cost = start_state.attacking_pairs()
        better_state = False
        for successor in start_state.successors():
            successor_cost = successor.attacking_pairs()

            if successor_cost < current_cost:
                better_state=True
                current_cost = successor_cost
                start_state = copy.deepcopy(successor)
        if not better_state:
            break

    return start_state

if __name__ == "__main__":
    start_seq = [i for i in range(1, 9)]
    shuffle(start_seq)
    init_state = State(start_seq)
    print(init_state)

    final_state = solve(init_state)

    print(final_state)


"""
OUTPUT:
-------

➜ python3 8Queens.py
State: [6, 2, 7, 3, 4, 8, 1, 5]
Attacked Pairs: 4
State: [6, 3, 7, 2, 4, 8, 1, 5]
Attacked Pairs: 0

Local minima
"""
