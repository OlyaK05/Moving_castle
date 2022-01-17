import os
import sys
import pygame

pygame.init()
size = width, height = 750, 700
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    """загрузка изображений из директории data"""
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("Не найдено:/")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

class Ball(pygame.sprite.Sprite):
    image = load_image("sprite_dog.png", -1)

    def __init__(self, x, speed):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
speed = 1
b1 = Ball(width//2, speed)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    all_sprites.draw(screen)
    all_sprites.update(width)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()


