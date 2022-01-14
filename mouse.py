import os
import sys
import random
import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
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


class Arrow(pygame.sprite.Sprite):
    image = load_image("arrow.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Arrow.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, x, y):
        self.rect.x, self.rect.y = x, y
        if pygame.mouse.get_focused():
            self.rect = self.rect.move(x - self.rect.x, y - self.rect.y)
        else:
            screen.fill("black")


all_sprites = pygame.sprite.Group()
arrow = Arrow(all_sprites)
pygame.mouse.set_visible(False)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            all_sprites.update(x, y)
    screen.fill("black")
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()