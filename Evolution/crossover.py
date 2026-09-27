import random
from NeuralNetwork.network import NeuralNetwork

def get_chromosome(network):
    chromosome = []

    for level in network.levels:
        chromosome.extend(level.biases)

        for weights in level.weights:
            chromosome.extend(weights)

    return chromosome

def set_chromosome(network, chromosome):
    index = 0

    for level in network.levels:
        for i in range(len(level.biases)):
            level.biases[i] = chromosome[index]
            index += 1

        for i in range(len(level.weights)):
            for j in range(len(level.weights[i])):
                level.weights[i][j] = chromosome[index]
                index += 1

def one_point_crossover(parent1, parent2):
    chromosome1 = get_chromosome(parent1)
    chromosome2 = get_chromosome(parent2)

    if len(chromosome1) != len(chromosome2):
        raise ValueError("Parents must have the same network structure")

    crossover_point = random.randint(1, len(chromosome1) - 1)

    child_chromosome = (
        chromosome1[:crossover_point]
        + chromosome2[crossover_point:]
    )

    child = NeuralNetwork([
        len(parent1.levels[0].inputs)
    ] + [
        len(level.outputs)
        for level in parent1.levels
    ])

    set_chromosome(child, child_chromosome)

    return child


def crossover(parent1, parent2, method="one_point"):
    if method == "one_point":
        return one_point_crossover(parent1,parent2)
    else:
        raise ValueError(f"Unknown crossover method: {method}")