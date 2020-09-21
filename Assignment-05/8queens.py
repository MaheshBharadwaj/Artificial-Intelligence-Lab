"""
Mahesh Bharadwaj K
185001089
Ex 05: 8 Queens problem using genetic algorithm
"""
import random

def generate_population(size: int):
    return  [[random.randint(1, 8) for i in range(8)] for j in range(size)]

def fitness(seq: list):
    max = 56
    attack = 0
    for i in range(8):
        for j in range(8):
            if i == j:
                continue
            # Same row
            if seq[i] == seq[j]:
                attack += 1
            
            # Same diagonal
            if ((seq[i] + i) == (seq[j] + j)) or ((seq[i] - i) == (seq[j] - j)):
                attack += 1

    return (max - attack) // 2

def reproduce(seq1: list, seq2: list):
    split = random.randint(0, 7)
    return seq1[:split] + seq2[split:]

def mutate(seq: list):
    i = random.randint(0, 7)
    new_val = random.randint(1, 8)

    seq[i] = new_val
    return seq


def pick_seq(population: list):
    probabilites = list(map(lambda seq: fitness(seq)/28, population))
    
    # Select sequence based on fitness as probability distribution
    return random.choices(population, probabilites)[0]



def geneticAlgorithm(size: int):
    population = generate_population(size)
    epsilon = 0.05
    goal = False

    for generation in range(200):
        new_population = list()
        for i in range(size):
            x, y = pick_seq(population), pick_seq(population)
            child = reproduce(x, y)

            if random.random() >= epsilon:
                child = mutate(child)

            if fitness(child) == 28:
                goal = True
                return child, goal, generation

            new_population.append(child)

        population = new_population[:]
    

    return max(population, key = lambda seq: fitness(seq)), goal, generation


if __name__ == "__main__":
    finalState, soln, gen = geneticAlgorithm(100)

    if soln:
        print("Solution Found in generation %d!" % (gen))
    else:
        print("No solution found!\nClosest child with fitness %d : " % (fitness(finalState)))

    board = [['x' for j in range(8)] for i in range(8)]

    for i, val in enumerate(finalState):
        board[i][val-1] = 'Q'

    for row in board:
        print(" ".join(row))

"""
OUTPUT:
-------

Solution Found in generation 140!
x x x x x Q x x
x x Q x x x x x
x x x x Q x x x
x x x x x x x Q
Q x x x x x x x
x x x Q x x x x
x Q x x x x x x
x x x x x x Q x

"""