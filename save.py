import json

def save_brain(brain, filename):
    filename = f"json/{filename}"

    data ={
        "levels" : []
    }

    for level in brain.levels:
        data["levels"].append({
            "weights": level.weights,
            "biases": level.biases
        })


    with open(filename,"w") as file:
        json.dump(data, file, indent=4)

def load_brain (brain, filename):
    filename = f"json/{filename}"

    with open(filename,"r") as file:
        data = json.load(file)

    for i, level in enumerate(brain.levels):
        level.weights = data["levels"][i]["weights"]
        
        level.biases = data["levels"][i]["biases"]

def save_lap_data(cars, generation):
    lap_data = {}

    for agent in cars:
        if not agent["lap_times"]:
            continue
        car_number = agent["number"]

        lap_data[f"car{car_number}"] = {
            "lap_times": {
                f"lap_time {i}": lap_time
                for i, lap_time in enumerate(
                    agent["lap_times"],
                    start=1
                )
            }
        }

    with open(
        f"json/lap_times_generation_{generation}.json",
        "w"
    ) as file:
        json.dump(lap_data, file, indent=4)