import pygame
import math

from Extra.utils import  lerp

class Sensor:
    def __init__(self,car,track_mask):
        self.car = car
        self.track_mask = track_mask
        self.rayCount = 7
        self.rayLength = 100
        self.raySpread = math.pi

        self.rays = []
        self.reading = []

    def update(self):

        self.castRays()

        self.reading = []

        for ray in self.rays:
            reading = self.getReading(ray)
            self.reading.append(reading)

        #print(self.reading)

    def getReading(self,ray):
        start = ray[0]
        end = ray[1]

        steps = int(self.rayLength)

        for i in range(steps + 1):
            t = i/steps

            x = round(lerp(start[0], end[0], t))
            y = round(lerp(start[1],end[1],t))

            #make sure the point is inside the track
            if 0 <= x < self.track_mask.get_size()[0] and 0 <= y < self.track_mask.get_size()[1]:
                if self.track_mask.get_at((x,y)):
                    return{
                        "point": (x,y),
                        "offset": t
                    }
         

    def castRays(self):
        self.rays = []
        for i in range(self.rayCount) :
                RayAngle = lerp(self.raySpread/2,
                                -self.raySpread/2, 
                                0.5 if self.rayCount == 1 else i /(self.rayCount-1)
                                ) + math.radians(self.car.angle)

                start =(
                    self.car.x + self.car.img.get_width() / 2,
                    self.car.y + self.car.img.get_height() / 2
                )
                end = (
                    start[0] - math.sin(RayAngle) * self.rayLength,
                    start[1] - math.cos(RayAngle) * self.rayLength
                )

                self.rays.append([start,end])

    def draw(self,win):
        for i in range(self.rayCount):

            start = self.rays[i][0]
            end = self.rays[i][1]

            if self.reading[i]:
                end = self.reading[i]["point"]

            #yellow line : start of ray -> detected point
            pygame.draw.line(
                win,(255, 255, 0), self.rays[i][0], end, 2
            )

            #Black line: detected point -> original ray endpoint
            pygame.draw.line(
                win, (0,0,0), self.rays[i][1],end,2
            )

