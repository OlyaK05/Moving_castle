import os
import sys
import pygame
import first_level

pygame.init()
size = width, height = 750, 700
screen = pygame.display.set_mode(size)


def text(message, x, y, font_color=(0, 0, 0), font_type='shrift.otf', font_size=75):
    front_type = pygame.font.Font(font_type, font_size)
    text = front_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("Не найдено:/")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((-10, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Button():
    def __init__(self, width, height, sign):
        self.widht = width
        self.height = height
        self.inactive_color = (13, 102, 58)
        self.active_color = (13, 162, 58)
        self.sign = sign

    def draw(self, x, y, message):
        pos = pygame.mouse.get_pos()  # координаты курсора
        click = pygame.mouse.get_pressed()  # нажатие на кнопку
        if x < pos[0] < x + self.widht and y < pos[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.widht, self.height))
            if click[0] == 1:  # нажатие на левую кнопку мыши
                if self.sign == 1:
                   pygame.mixer.music.load("button_sound.mp3")
                   pygame.mixer.music.set_volume(0.04)
                   pygame.mixer.music.play(loops=0)
                   start_game()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.widht, self.height))
        text(message, x + 10, y + 10)


def menu():
    button_start = Button(150, 110, 1)
    button_info =  Button(150, 110, 0)
    background = load_image("bg (1).jpg")
    demonstration = True
    while demonstration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                demonstration = False

        screen.blit(background, (0, 0))
        button_start.draw(300, 300, "Start")
        button_info.draw(300, 430, "Info")
        pygame.display.flip()
    pygame.quit()


def start_game():
    screen.fill((0,0,0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed():
                first_level.all_sprites.update(pygame.key.get_pressed())
        first_level.tile_group.draw(first_level.screen)
        first_level.tile_let_group.draw(first_level.screen)
        first_level.player_group.draw(first_level.screen)
        pygame.display.flip()
    pygame.quit()


menu()