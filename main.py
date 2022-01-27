import os
import pygame
import webbrowser
from levels import level_controller
from settings import load_image, arrow_sprite, text, screen, terminate

pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Moving Castle")
control = True


class Button:
    """класс кнопок"""

    def __init__(self, width, height, sign):
        self.widht = width
        self.height = height
        self.inactive_color = (0, 107, 83)
        self.active_color = (0, 164, 127)
        self.sign = sign

    def draw(self, x, y, message, font_size=75):
        global control
        pos = pygame.mouse.get_pos()  # координаты курсора
        click = pygame.mouse.get_pressed()  # нажатие на кнопку
        if x < pos[0] < x + self.widht and y < pos[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.widht, self.height))
            if click[0] == 1:  # нажатие на левую кнопку мыши
                button_sound = pygame.mixer.Sound(os.path.join("music", "button_sound.mp3"))
                button_sound.set_volume(0.1)
                button_sound.play()
                if self.sign == 0:
                    level_controller()
                elif self.sign == 1:
                    info()
                elif self.sign == 2:
                    webbrowser.open('https://ru.wikipedia.org/wiki/%D0%A5%D0%BE%D0%B4%D1%8F%D1%87%D0%B8%D0%B9_%D0%B7%D0'
                                    '%B0%D0%BC%D0%BE%D0%BA_(%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5)', new=2)
                elif self.sign == 3:
                    control = False
                    show_menu()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.widht, self.height))
        text(message, x + 10, y + 10, font_size)


def show_menu():
    """основное меню игры"""
    background = load_image("bg (1).jpg")
    pygame.mixer.music.load(os.path.join("music", "sky_walk.mp3"))
    pygame.mixer.music.play(loops=-1)

    button_start = Button(130, 100, 0)
    button_info = Button(130, 100, 1)
    button_story = Button(80, 65, 2)

    demonstration = True
    while demonstration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                demonstration = False
                break
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                arrow_sprite.update(x, y)
        if demonstration:
            screen.blit(background, (0, 0))
            text("Moving Castle,", 190, 70, 100, font_color=(0, 0, 0))
            text("Moving Castle,", 193, 70, 100)
            button_start.draw(300, 270, "Start", 70)
            button_info.draw(300, 390, "Info", 70)
            button_story.draw(10, 600, "Story", 40)
            if pygame.mouse.get_focused():
                arrow_sprite.draw(screen)
            pygame.display.flip()


def info():
    running = True
    button_enter = Button(70, 60, 3)
    background = load_image("background_info.jpg")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
                break
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                arrow_sprite.update(x, y)
        if running:
            screen.blit(background, (0, 0))
            button_enter.draw(675, 10, "Enter", 40)
            text("Rules of the game", 200, 20, 90)
            text("1. Игра состоит из трёх уровней.", 10, 380, 32, None)
            text("2. На каждом уровне нужно собирать дрова(это будут очки)", 10, 410, 31, None)
            text("3. Для перехода на следующий уровень необходимо попасть", 10, 440, 31, None)
            text("на картинку с огнём", 10, 460, 31, None)
            text("4. Если игрок попадает на воду, то к итоговому времени", 10, 570, 31, None)
            text("прибавляется +10 секунд", 10, 590, 31, None)
            text("5. Цель игры - пройти все уровни за минимальное время", 10, 630, 31, None)
            text("с наибольшим числом очков.", 10, 650, 31, None)
            if pygame.mouse.get_focused():
                arrow_sprite.draw(screen)
            pygame.display.flip()


show_menu()
