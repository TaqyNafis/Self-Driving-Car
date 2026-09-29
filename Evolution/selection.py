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
    # RANK_POWER controls selection pressure: weight = 1 / rank**RANK_POWER
    # Higher = top cars dominate, lower = more diversity.
    # (approx. pick chance with 150 parents)
    #
    #   0    -> same as random selection (baseline)
    #   0.5  -> very weak. Rank 1 ~4%, bottom half gets ~35% of picks
    #   1    -> moderate. Rank 1 ~18%, top 5 ~41%, top 10 ~52%
    #   1.5  -> strong. Rank 1 ~41%, top 5 ~72%, top 10 ~82%
    #   2    -> very strong. Rank 1 ~61%, top 5 ~89%, nearly all clones of the top 2-3
    #   3+   -> basically just cloning rank 1
    #
    # Lower it if the population stalls or stops improving
    # Raise it if too many weak cars are being picked as parents
    power = 1

    rank_weights  =  [1 / (r ** power) for r in range(1, len(parents) + 1)]

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