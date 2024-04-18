import pygame


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

# Arabanın açısını ayarlayarak (döndürerek) o yönde ilerletme
def blit_rotate_center(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)

def blit_text_center(screen, font, text):
    render = font.render(text, 1, (240,255,255))
    screen.blit(render, (screen.get_width()/2 - render.get_width()/2, screen.get_height()/2.10 - render.get_height()/2))