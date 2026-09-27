import random


def select_parents(parents, method="random"):

    if method == "random":
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        return parent1, parent2

    else:
        raise ValueError(f"Unknown selection method: {method}")