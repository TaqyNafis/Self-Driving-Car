import json

def save_brain(brain):
    data = {
        "levels": []
    }

    for level in brain.levels:
        data["levels"].append({
            "weights": level.weights,
            "biases": level.biases
        })

    return data


def save_brains(cars, filename):
    filename = f"json/{filename}"

    data = {
        "brains": []
    }

    for agent in cars:
        brain_data = {
            "fitness": agent["fitness"],
            "levels": save_brain(agent["brain"])["levels"]
        }

        data["brains"].append(brain_data)

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_brain(brain, data):
    for i, level in enumerate(brain.levels):
        level.weights = data["levels"][i]["weights"]
        level.biases = data["levels"][i]["biases"]



def load_brains(cars, filename, number_of_best_cars):
    filename = f"json/{filename}"

    with open(filename, "r") as file:
        data = json.load(file)

    number_to_load = min(
        number_of_best_cars,
        len(data["brains"]),
        len(cars)
    )

    for i in range(number_to_load):
        load_brain(
            cars[i]["brain"],
            data["brains"][i]
        )

    return number_to_load


def save_lap_data(generation_data, generation):

    with open(
        f"json/lap_times_generation_{generation}.json",
        "w"
    ) as file:
        json.dump(generation_data, file, indent=4)