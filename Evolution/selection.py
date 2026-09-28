import random

def random_selection(parents):
        parent1 = random.choice(parents)

        if len(parents) == 1:
            return parent1, parent1

        while  True:
            parent2 = random.choice(parents)

            if parent1 != parent2:
                break

        return parent1, parent2

def rank_selection(parents):
    rank_weights  =  list(range(len(parents), 0 , -1))

    parent1 = random.choices(parents, weights= rank_weights, k =1)[0]

    if len(parents) == 1:
        return parent1, parent1
    
    while True:
        parent2 = random.choices(parents, weights= rank_weights, k =1)[0]
        if parent1 != parent2:
             break
    return parent1 , parent2
   

def select_parents(parents, method="random"):

    if method == "random":
        return random_selection(parents)
    elif method == "rank":
        return rank_selection(parents)     
    else:
        raise ValueError(f"Unknown selection method: {method}")

def get_selection_methods():
    return ["random", "rank"]