import random

def select_parents(cars, number_of_parents, method="tops"):
    if method == "top":
        return cars[:number_of_parents]

    elif method == "random":
        return random.sample(cars, number_of_parents)

    else:
        raise ValueError(f"Uknown selection method: {method}")