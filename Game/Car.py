import pygame
import math

from utils import blit_rotate_center, scale_image, lerp

CAR = scale_image(pygame.image.load("asset/car.png"),0.55)


class AbstractCar:
    def __init__(self, max_velo , rotation_velo, start_x = 0, start_y = 0, start_angle = 0, control_type="player"):
        self.img = self.IMG.copy()
        self.control_type = control_type
        self.max_velo = max_velo
        self.velo = 0
        self.rotation_velo = rotation_velo
        self.angle = start_angle
        self.x = start_x
        self. y = start_y
        self.accel = 0.1
        self.braking = self.accel/2
        self.friction = self.accel/4 # can change to track based not in car
    def rotate (self, left= False, right = False):
        if left:
            self.angle += self.rotation_velo
        elif right:
            self.angle -= self.rotation_velo

    def reset(self, start_x, start_y, start_angle = 0):
        self.x = start_x
        self.y = start_y
        self.angle = start_angle
        self.velo = 0

    def draw(self,win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.velo = min(self.velo + self.accel, self.max_velo)
        self.move()

    def move_backward(self):
        self.velo = max(self.velo - self.braking, 0)
        #print(self.velo,"-",self.braking, "=", self.velo - self.braking)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velo # cos x = height / hypothenus 
        horizontal = math.sin(radians) * self.velo # sin y = width / hypothenus

        self.y -= vertical
        self.x -= horizontal 

    def reduce_speed(self):
        self.velo = max(self.velo - self.friction, 0)
        self.move()

    def collide(self,mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x),int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    
    def bounce(self):
        self.velo = -self.velo/1.5
        self.move()

    def move_ai(self,output):
        if output[0]:
            self.move_forward()
        if output[1]:
            self.rotate(left=True)
        if output[2]:
            self.rotate(right=True)
        if output[3]:
            self.move_backward()

class PlayerCar(AbstractCar):
    IMG = CAR

class TestCar(AbstractCar):
    IMG = scale_image(pygame.image.load("asset/car.png"),1)
    START_POS = (400,300)


