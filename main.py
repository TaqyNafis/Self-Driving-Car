import pygame
import time
import os
import copy

from Game.Car import PlayerCar
from Game.input import *
from Game.Sensor import Sensor
from NeuralNetwork.network import NeuralNetwork
from NeuralNetwork.Visualizer import NetworkVisualizer
from Game.track import *
from Extra.save import *
from Game.event_handler import handle_events
from Evolution.selection import select_parents
from Evolution.mutation import mutate

pygame.init()

# Setting 

SELECTION_METHOD = "top"
MUTATION_METHOD = "default"

NUMBER_OF_CAR = 1
NUMBER_OF_BEST_CAR = 20
NUMBER_OF_PARENT = 3

MUTATION_AMOUNT = 0.2

SIMULATION_TIME_MINUTES = 2
TIMEOUT = 10

TOTAL_GENERATION = 2

#Debuggin setting
DEBUG = True

SHOW_CHECKPOINT = False
SHOW_LAP = True
BESTCAR_UPDATE = True
STAGNATION_CHECK = False

KEEP_OPEN = False

Frame = 60
clock = pygame.time.Clock()

#Color

WHITE = (255, 255, 255)
DARK_GRAY = (64, 64, 64)
BLACK = (0,0,0)
RED  =(255, 0, 0)

#Track Setup

tracks = [Track1(),Track3()] 

pygame.display.set_caption("Car Game")



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
            "fitness": 0
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

def main():
    generation = 1
    
    while generation <= TOTAL_GENERATION:
        # Create the population every generation
        cars = generateCars(
            NUMBER_OF_CAR,
            tracks[0]
        )

        # #Load Best Brain
        if os.path.exists("json/best_brains.json"):

            number_to_load = load_brains(
                cars,
                "best_brains.json",
                NUMBER_OF_BEST_CAR
            )

            if number_to_load > 0:
                parents = select_parents(
                    cars[:number_to_load],
                    NUMBER_OF_PARENT,
                    SELECTION_METHOD
                )

                for i in range(number_to_load, NUMBER_OF_CAR):

                    parents = parents[(i - number_to_load) % len(parents)]
                    cars[i]["brain"]= copy.deepcopy( parents["brain"])

                    mutate(
                        cars[i]["brain"],
                        MUTATION_METHOD,
                        MUTATION_AMOUNT
                    )

        print(f"\n Generation {generation}")

        for track in tracks:
            
            print(f"Running {track.__class__.__name__}")

            run_track(cars,track)

            for agent in cars:
                #calculate each car progress through each track and edded up
                track_fitness = track.training_weight * ((agent["lap_num"]-1) + agent["current_checkpoint"]/len(track.checkpoints))
                agent["fitness"] += track_fitness

        best_cars = sorted(cars, key=lambda agent: agent["fitness"], reverse=True)[:NUMBER_OF_BEST_CAR]

        if NUMBER_OF_CAR != 1:
            save_brains(best_cars, "best_brains.json")

            print("Best Brain Saved")
        save_lap_data(cars,generation)

        generation += 1
    


if __name__ == "__main__":
    main()


pygame.quit()


