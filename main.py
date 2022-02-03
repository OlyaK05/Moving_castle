import os
import pygame
import pygame_gui
import webbrowser
from levels import level_controller
from settings import load_image, arrow_sprite, text, screen, terminate, width, height, sound_button_click, main_music

pygame.init()
pr_control = True
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Moving Castle")


def show_menu():
    global pr_control, clock, counter, score
    """основное меню игры"""

    manager = pygame_gui.UIManager((width, height))
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 270), (130, 100)),
                                                text='Start',
                                                manager=manager)
    info_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 390), (130, 100)),
                                               text='Info',
                                               manager=manager)
    story_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 600), (80, 50)),
                                                text='Story',
                                                manager=manager)
    main_music()
    background = load_image("bg (1).jpg")
    demonstration = True
    while demonstration:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                demonstration = False
                return

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                arrow_sprite.update(x, y)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                sound_button_click()
                if event.ui_element == start_button:
                    if level_controller() == 0:
                        return
                    main_music()
                elif event.ui_element == info_button:
                    if info() == 0:
                        terminate()
                        return
                elif event.ui_element == story_button:
                    webbrowser.open(
                        'https://ru.wikipedia.org/wiki/%D0%A5%D0%BE%D0%B4%D1%8F%D1%87%D0%B8%D0%B9_%D0%B7%D0'
                        '%B0%D0%BC%D0%BE%D0%BA_(%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5)', new=2)
            if pr_control:
                manager.process_events(event)
        if demonstration and pr_control:
            manager.update(time_delta)
            screen.blit(background, (0, 0))
            text("Moving Castle,", 190, 70, 100, font_color=(0, 0, 0))
            text("Moving Castle,", 193, 70, 100)
            manager.draw_ui(screen)
            if pygame.mouse.get_focused():
                arrow_sprite.draw(screen)
            pygame.display.update()


def info():
    global pr_control, clock

    manager_info = pygame_gui.UIManager((width, height))
    enter_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((675, 10), (70, 60)),
                                                text='Enter',
                                                manager=manager_info)
    running = True
    background = load_image("background_info.jpg")
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 0

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                arrow_sprite.update(x, y)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                sound_button_click()
                if event.ui_element == enter_button:
                    return
            if pr_control:
                manager_info.process_events(event)
        if running and pr_control:
            manager_info.update(time_delta)
            screen.blit(background, (0, 0))
            text("Rules of the game", 200, 20, 90)
            text("1. Игра состоит из трёх уровней.", 10, 380, 32, None)
            text("2. На каждом уровне нужно собирать дрова(это будут очки)", 10, 410, 33, None)
            text("3. Для перехода на следующий уровень необходимо попасть", 10, 440, 33, None)
            text("на картинку с огнём", 10, 460, 32, None)
            text("4. Если игрок попадает на воду, то к итоговому времени", 10, 570, 32, None)
            text("прибавляется +10 секунд", 10, 590, 32, None)
            text("5. Цель игры - пройти все уровни за минимальное время", 10, 630, 32, None)
            text("с наибольшим числом очков.", 10, 650, 32, None)
            manager_info.draw_ui(screen)
            if pygame.mouse.get_focused():
                arrow_sprite.draw(screen)
            pygame.display.flip()


show_menu()
terminate()