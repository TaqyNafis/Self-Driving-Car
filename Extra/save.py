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
    filepath = f"json/Laps"

    with open(
        f"{filepath}/lap_times_generation_{generation}.json",
        "w"
    ) as file:
        json.dump(generation_data, file, indent=4)

def build_generation_summary(generation, cars, generation_data):
    TOP_N = 10
    fitnesses = sorted((agent["fitness"] for agent in cars), reverse=True)
    top = fitnesses[:TOP_N]

    best_lap_times = {}
    for track_name, lap_data in generation_data.items():
        all_laps = [lap for laps in lap_data.values() for lap in laps]
        best_lap_times[track_name] = min(all_laps) if all_laps else None

    return {
        "generation": generation,
        "best_fitness": top[0],
        f"top_{TOP_N}_avg_fitness": sum(top) / len(top),
        "finishers": {
            track_name: len(lap_data)
            for track_name, lap_data in generation_data.items()
        },
        "best_lap_time": best_lap_times,
    }

def save_run_summary(seed, summaries, settings):
    filepath = f"json/Summary"
    with open(f"{filepath}/summary_seed{seed}.json", "w") as file:
        json.dump(
            {"seed": seed, "settings": settings, "generations": summaries},file,indent=4)