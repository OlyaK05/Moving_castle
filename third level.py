import os
import sys
import pygame
import random

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
        self.rect.x = ran
        self.speed = speed

    def update(self, *args):
        if self.rect.y < args[0]:
            self.rect.y += self.speed
        else:
            self.rect.y = -50

    class Player(pygame.sprite.Sprite):
        """класс героя"""
        ima
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y)
            self.x = 0
            self.y = 0

        def update(self, action):
            """перемещение героя по карте"""
            global run, score, gave_achiev

            x, y = 0, 0
            if action[pygame.K_UP]:
                y = -25
            elif action[pygame.K_DOWN]:
                y = 25
            elif action[pygame.K_RIGHT]:
                x = 25
            elif action[pygame.K_LEFT]:
                x = -25
            self.rect = self.rect.move(x, y)
            self.rect.x += x
            self.rect.y += y
            if pygame.sprite.spritecollideany(self, tile_let_group) \
                    or pygame.sprite.spritecollideany(self, horizontal_borders) \
                    or pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect = self.rect.move(-x, -y)  # при пересечении со спрайтами стенки/препятствия герой не двигается
                self.rect.x -= x
                self.rect.y -= y
            if pygame.sprite.spritecollideany(self, achievements_group):
                """пересечение со спрайтами достижений"""
                if (self.rect.x, self.rect.y) not in gave_achiev:
                    fire_sound = pygame.mixer.Sound("ignition of fire.mp3")
                    fire_sound.set_volume(0.03)
                    fire_sound.play()

                    score += 1
                    gave_achiev.append((self.rect.x, self.rect.y))
                GaveAchievement('empty', self.rect.x, self.rect.y)
            if self.rect.x == 660 and self.rect.y == 0:
                run = False
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


