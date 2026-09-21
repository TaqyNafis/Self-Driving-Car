import pygame

def scale_image(img, factor):
    size = round(img.get_width() * factor),round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect =  rotated_image.get_rect(center= image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)
    
def get_mouse_click():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            return event.pos
    
    return None

def lerp (A,B,t): # Linear Interpolation
    return A+(B-A)*t