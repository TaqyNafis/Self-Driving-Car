import pygame

from input import exit_game
from Car import TestCar
from Sensor import Sensor

pygame.init()

screen = pygame.display.set_mode((800, 600))
run = True

mouse_rect_surface = pygame.Surface((20, 20))
mouse_rect_surface.fill((0, 255, 0))

Player_Car = TestCar(0, 0)

clock = pygame.time.Clock()
while run:

    screen.fill((0, 0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Create a transparent screen-sized surface
    mouse_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    mouse_surface.fill((0, 0, 0, 0))

    # Put the mouse rectangle onto the surface
    pygame.draw.rect(
        mouse_surface,
        (0, 255, 0, 255),
        (mouse_x, mouse_y, 20, 20)
    )

    # Create the mask
    mouse_mask = pygame.mask.from_surface(mouse_surface)

    sensor = Sensor(Player_Car, mouse_mask)
    sensor.update()

    Player_Car.draw(screen)
    sensor.draw(screen)

    run = exit_game(run)

    screen.blit(mouse_rect_surface, (mouse_x, mouse_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()