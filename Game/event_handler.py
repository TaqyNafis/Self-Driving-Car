import pygame

def handle_events():
    mouse_pos = None
    run = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

    return run, mouse_pos