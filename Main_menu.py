import os
import sys
import pygame
import first_level
import webbrowser

pygame.init()
size = width, height = 750, 700
screen = pygame.display.set_mode(size)


def text(message, x, y,font_size=75, font_color=(0, 0, 0)):
    font_color = (0, 0, 0)
    font_type = 'shrift.otf'
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
        self.inactive_color = (0, 107, 83)
        self.active_color = (0, 164, 127)
        self.sign = sign

    def draw(self, x, y, message, font_size=75):
        pos = pygame.mouse.get_pos()  # координаты курсора
        click = pygame.mouse.get_pressed()  # нажатие на кнопку
        if x < pos[0] < x + self.widht and y < pos[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.widht, self.height))
            if click[0] == 1:  # нажатие на левую кнопку мыши
                if self.sign == 0:
                   pygame.mixer.music.load("button_sound.mp3")
                   pygame.mixer.music.set_volume(0.04)
                   pygame.mixer.music.play(loops=0)
                   start_game()
                if self.sign == 2:
                    webbrowser.open('https://ru.wikipedia.org/wiki/%D0%A5%D0%BE%D0%B4%D1%8F%D1%87%D0%B8%D0%B9_%D0%B7%D0%B0%D0%BC%D0%BE%D0%BA_(%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5)', new=2)
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.widht, self.height))
        text(message, x + 10, y + 10, font_size)


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
def menu():
    #pygame.mixer.music.load("sky_walk.mp3")
    #pygame.mixer.music.play(loops=-1, start=0.0)
    button_start = Button(130, 100, 0)
    button_info =  Button(130, 100, 1)
    button_story = Button(80, 65, 2)
    background = load_image("bg (1).jpg")
    demonstration = True
    while demonstration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                demonstration = False

        screen.blit(background, (0, 0))
        button_start.draw(300, 270, "Start",70)
        button_info.draw(300, 390, "Info", 70)
        button_story.draw(10, 600, "Story", 40)
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