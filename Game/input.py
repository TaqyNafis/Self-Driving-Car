import pygame

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]: #and player_car.velo !=0:
        player_car.rotate(left=True)
    if keys[pygame.K_d]: #and player_car.velo !=0:
        player_car.rotate(right=True)

    if keys[pygame.K_w] and not keys[pygame.K_s]:
        player_car.move_forward()
        moved = True
    elif keys[pygame.K_s]:
        player_car.move_backward()
        moved = True
    
    if not moved:
        player_car.reduce_speed() 