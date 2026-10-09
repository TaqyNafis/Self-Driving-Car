import pygame
import time
import os
import copy
import random

from Game.Car import PlayerCar
from Game.input import move_player
from Game.Sensor import Sensor
from Game.track import *
from NeuralNetwork.network import NeuralNetwork
from NeuralNetwork.Visualizer import NetworkVisualizer
from Extra.save import save_brains,load_brains,save_lap_data, build_generation_summary, save_run_summary
from Game.event_handler import handle_events
from Evolution.selection import select_parents ,get_selection_methods
from Evolution.mutation import mutate, get_mutation_methods
from Evolution.crossover import crossover, get_crossover_methods

pygame.init()

# Setting 
# "random" "rank" "tournament" "roulette"
SELECTION_METHOD = "tournament"
# "default"
MUTATION_METHOD = "default"
#"one_point" "two point"
CROSSOVER_METHOD = "two_point"

NUMBER_OF_CAR = 150
NUMBER_OF_SAVED_BRAIN= NUMBER_OF_CAR # Number of car to have their brain saved
NUMBER_OF_ELITE =  5 # Number of Top best car to continue into the next generation

MUTATION_AMOUNT = 0.4
MUTATION_RATE = 0.2

USE_CROSSOVER = False
USE_MUTATION = True

SIMULATION_TIME_MINUTES = 1
TIMEOUT = 10

TOTAL_GENERATION = 10
SEED = 25

#Debugging setting
DEBUG = True

SHOW_CHECKPOINT = False
SHOW_LAP = True
BESTCAR_UPDATE = True
STAGNATION_CHECK = False

KEEP_OPEN = False

Frame = 60
clock = pygame.time.Clock()

#Setting Check
if NUMBER_OF_CAR < 2 and  USE_CROSSOVER:
    raise ValueError("NUMBER_OF_CAR must atleast be 2 if crossover want to be used")
if NUMBER_OF_ELITE < 0 or NUMBER_OF_SAVED_BRAIN < 0 or MUTATION_AMOUNT < 0:
    raise ValueError(
        f"Value cannot be negative: "
        f"NUMBER_OF_ELITE={NUMBER_OF_ELITE}, "
        f"NUMBER_OF_SAVED_BRAIN={NUMBER_OF_SAVED_BRAIN}, "
        f"MUTATION_AMOUNT={MUTATION_AMOUNT}"
    )
if TOTAL_GENERATION < 1 or NUMBER_OF_CAR < 1:
    raise ValueError(
        f"Value must be at least 1: "
        f"TOTAL_GENERATION={TOTAL_GENERATION}, "
        f"NUMBER_OF_CAR={NUMBER_OF_CAR}"
    )
if NUMBER_OF_ELITE > NUMBER_OF_CAR:
    raise ValueError("NUMBER_OF_ELITE cannot be greater than NUMBER_OF_CAR")
if NUMBER_OF_SAVED_BRAIN > NUMBER_OF_CAR:
    raise ValueError("NUMBER_OF_SAVED_BRAIN cannot be greater than NUMBER_OF_CAR")
if not 0 <= MUTATION_RATE <= 1:
    raise ValueError("MUTATION_RATE must be between 0 and 1")
if SELECTION_METHOD not in get_selection_methods():
    raise ValueError(
        f"Unknown selection method: {SELECTION_METHOD}. "
        f"Available methods: {get_selection_methods()}"
    )

if CROSSOVER_METHOD not in get_crossover_methods():
    raise ValueError(
        f"Unknown crossover method: {CROSSOVER_METHOD}. "
        f"Available methods: {get_crossover_methods()}"
    )

if MUTATION_METHOD not in get_mutation_methods():
    raise ValueError(
        f"Unknown mutation method: {MUTATION_METHOD}. "
        f"Available methods: {get_mutation_methods()}"
    )

if os.path.exists("json/saved_brains.json"):
    print("Warning: loading existing saved_brains.json (not a fresh start)")
#Color

WHITE = (255, 255, 255)
DARK_GRAY = (64, 64, 64)
BLACK = (0,0,0)
RED  =(255, 0, 0)

#Set Seed
if SEED is None:
    SEED = random.randrange(0, 2**32)
    
random.seed(SEED)

print(f"using Seed {SEED}")

#Track Setup

tracks = [Track1(),Track3()] 

pygame.display.set_caption("Car Game")

def build_run_settings(tracks):
    return {
        "number_of_car": NUMBER_OF_CAR,
        "number_of_elite": NUMBER_OF_ELITE,
        "selection_method": SELECTION_METHOD,
        "mutation_method": MUTATION_METHOD,
        "crossover_method": CROSSOVER_METHOD,
        "use_crossover": USE_CROSSOVER,
        "use_mutation": USE_MUTATION,
        "mutation_amount": MUTATION_AMOUNT,
        "mutation_rate": MUTATION_RATE,
        "simulation_time_minutes": SIMULATION_TIME_MINUTES,
        "timeout": TIMEOUT,
        "total_generation": TOTAL_GENERATION,
        "tracks": [
            {
                "name": track.__class__.__name__,
                "weight": track.weight,
                "target_time": track.target_time,
                "checkpoints": len(track.checkpoints),
            }
            for track in tracks
        ],
    }


def generateCars(N, track):
    cars= []
    for i in range(N):

        if N !=1:
            car = PlayerCar(4,2,*track.start_pos,"ai")
        else:
            car = PlayerCar(4,2, *track.start_pos)

        car.img.set_alpha(128)

        sensor = Sensor(car, track.track_border_mask) 
        brain = NeuralNetwork([sensor.rayCount, 6, 4])

        cars.append({
            "car": car,
            "sensor": sensor,
            "brain":brain,
            "number": i + 1,
            "current_checkpoint":0,
            "lap_start_time": None,
            "lap_times": [],
            "lap_num": 0,
            "active?": True,
            "last_progress_time": time.time(),
            "fitness": 0,
            "parent_fitness" : 0
        })
    return cars

def resetCars(cars , track):
    for agent in cars:

        car = agent["car"]

        #reset car position
        car.reset(*track.start_pos)

        # Reset agent state
        agent["sensor"] = Sensor(
            car,
            track.track_border_mask
        )

        agent["current_checkpoint"] = 0
        agent["lap_start_time"] = None
        agent["lap_times"] = []
        agent["lap_num"] = 0
        agent["active?"] = True
        agent["last_progress_time"] = time.time()

def draw(win, images, cars, visualizer, track):
    win.fill(DARK_GRAY)

    for checkpoint in track.checkpoints:
        pygame.draw.rect(
            win,
            RED,
            checkpoint["rect"]
        )

    for img, pos in images:
        win.blit(img, pos)

    for agent in cars:
        if not agent["active?"]:
            continue
        car = agent["car"]
        sensor = agent["sensor"]

        car.draw(win)
        sensor.draw(win)

    visualizer.draw(win)

    pygame.display.update()


def run_track(cars, track):
    simulation_start_time = time.time()

    resetCars(cars, track)

    WIDTH, HEIGHT = track.track_dimension

    screen = pygame.display.set_mode(
        (WIDTH + 500, HEIGHT)
    )

    images = [
        (track.finish, track.finish_pos),
        (track.track, (0, 0))
    ]

    #Generation Setup
    bestCar = cars[0]
    previous_best = None
    current_best = None

    visualizer = NetworkVisualizer( cars[0]["brain"], WIDTH + 50)

    run = True

    #Simulation loop
    while run:

        run, mouse_pos = handle_events()

        # if mouse_pos is not None:
        #     print(mouse_pos)
        
        # End Generation
        if (all(not agent["active?"] for agent in cars) or time.time() - simulation_start_time > SIMULATION_TIME_MINUTES * 60) and not KEEP_OPEN:
            run = False
            continue

        #Update Cars
        for agent in cars:

            if not agent["active?"]:
                continue

            car = agent["car"]
            sensor = agent["sensor"]
            brain = agent["brain"]
            
            #checkpoint check
            for checkpoint in track.checkpoints:
                if checkpoint["rect"].collidepoint(car.x, car.y):

                    if checkpoint["number"] == agent ["current_checkpoint"] + 1:
                        agent["current_checkpoint"] = checkpoint["number"]
                        agent["last_progress_time"] = time.time()
                        if DEBUG and SHOW_CHECKPOINT:
                            print(f"Car {agent["number"]} reached checkpoints : {agent["current_checkpoint"]}/{len(track.checkpoints)}")

            #finish line check      
            finish_poi_collide = car.collide(track.finish_mask, *track.finish_pos)
            if finish_poi_collide != None:
                if agent["current_checkpoint"] == len(track.checkpoints) and agent["lap_start_time"] is not None:
                    agent["current_checkpoint"] = 0
                    lap_time = time.time() - agent["lap_start_time"]
                    agent["lap_times"].append(lap_time)
                    agent["lap_start_time"] = None

                    if DEBUG and SHOW_LAP:
                        print(f"Car {agent["number"]} finished lap {agent["lap_num"]}\n lap time = {lap_time:.3f}")
                    
                if agent["lap_start_time"] is None:
                    agent["lap_num"] += 1
                    agent["lap_start_time"] = time.time()

            #stagnation check
            if car.control_type == "ai" and agent["active?"] and time.time() - agent["last_progress_time"] > TIMEOUT:
                if DEBUG and STAGNATION_CHECK:
                    print(f"car {agent["number"]} stagnated")

                agent["active?"] = False
            
            #Sensor
            sensor.update()

            offsets = []

            for reading in sensor.reading:
                if reading is None:
                    offsets.append(0)
                else:
                    offsets.append(1 - reading["offset"])

            #Neural Network
            outputs = brain.feedFoward(offsets)

            #Movement
            if car.control_type == "ai" and agent["active?"]:
                car.move_ai(outputs)
            elif car.control_type == "player":
                move_player(car)

            #Track Collision
            if car.collide(track.track_border_mask) is not None:
                car.bounce()
                if car.control_type == "ai":
                    agent["active?"] = False
        
        #Find Best car
        for agent in cars:
            if (
                agent["lap_num"],
                agent["current_checkpoint"]
            ) >(
                bestCar["lap_num"],
                bestCar["current_checkpoint"]
            ):
                bestCar = agent

        current_best = bestCar["number"]

        #Update Best Car Display
        if current_best != previous_best:

            if previous_best is not None:
                for agent in cars:
                    if agent["number"] == previous_best and agent["active?"]:
                        agent["car"].img.set_alpha(128)
                        break

            bestCar["car"].img.set_alpha(255)

            if DEBUG and BESTCAR_UPDATE:
                print(
                    f"Best Car: {bestCar['number']} | "
                    f"Lap: {bestCar['lap_num']} | "
                    f"Checkpoint: {bestCar['current_checkpoint']}"
                )

            previous_best = current_best

        #visualize best car brain
        bestBrain  =bestCar["brain"]
        visualizer.brain = bestBrain

        #draw
        draw(screen,images,cars,visualizer,track)
            
        clock.tick(Frame)

    return {
        agent["number"]: agent["lap_times"].copy()
        for agent in cars
        if agent["lap_times"]
    }

def main():
    generation = 1
    settings = build_run_settings(tracks) 
    run_summary = []
    
    while generation <= TOTAL_GENERATION:
        # Create the population every generation
        cars = generateCars( NUMBER_OF_CAR, tracks[0])

        #Load Best Brain
        if os.path.exists("json/saved_brains.json"):

            number_to_load = load_brains(cars, "saved_brains.json", NUMBER_OF_SAVED_BRAIN)
            elite_count = min(NUMBER_OF_ELITE, number_to_load)

            if number_to_load > 0:
                parents = [
                    { "brain": copy.deepcopy(c["brain"]), "parent_fitness": c["parent_fitness"] }
                    for c in cars[:number_to_load]
                ]
                for i in range(elite_count, NUMBER_OF_CAR):

                    parent1, parent2 = select_parents( parents, SELECTION_METHOD, USE_CROSSOVER)

                    if USE_CROSSOVER:
                        cars[i]["brain"] = crossover(parent1["brain"], parent2["brain"], CROSSOVER_METHOD
)
                    else:
                        cars[i]["brain"] = copy.deepcopy(parent1["brain"])

                    if USE_MUTATION:
                        mutate(cars[i]["brain"],MUTATION_METHOD,MUTATION_AMOUNT, MUTATION_RATE)
        print(f"\n Generation {generation}")

        generation_data = {}

        for track in tracks:
            
            print(f"Running {track.__class__.__name__}")

            lap_data = run_track(cars,track)

            generation_data[track.__class__.__name__] = lap_data

            for agent in cars:
                #calculate each car progress through each track and edded up
                track_fitness = min(1,(agent["lap_num"]-1) + agent["current_checkpoint"]/len(track.checkpoints))
                
                if agent["lap_times"]:
                    fastest_lap = min(agent["lap_times"])
                    speed_bonus = min(track.target_time / fastest_lap, 2)
                    track_fitness += speed_bonus



                agent["fitness"] += track.weight * track_fitness

        best_cars = sorted(cars, key=lambda agent: agent["fitness"], reverse=True )[:NUMBER_OF_SAVED_BRAIN]

        if NUMBER_OF_CAR != 1:
            save_brains(best_cars, "saved_brains.json")

            print("Best Brain Saved")
        save_lap_data(generation_data, generation)

        run_summary.append(build_generation_summary(generation, cars, generation_data))
        save_run_summary(SEED, run_summary, settings)

        generation += 1
    


if __name__ == "__main__":
    main()


pygame.quit()


