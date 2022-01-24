import pygame
import webbrowser
from settings import load_image, arrow_sprite, size, db
from first_level import score, run, generate_level, load_level, tile_group, achievements_group, gave_achievement, \
    tile_let_group, player_group, all_sprites

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Moving Castle")




class Button:
    """класс кнопок"""

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
                # button_sound = pygame.mixer.Sound(os.path.join("music", "button_sound.mp3"))
                # button_sound.play()
                if self.sign == 0:
                    #controller()
                    start_first_game()
                elif self.sign == 1:
                    info()
                elif self.sign == 2:
                    webbrowser.open('https://ru.wikipedia.org/wiki/%D0%A5%D0%BE%D0%B4%D1%8F%D1%87%D0%B8%D0%B9_%D0%B7%D0'
                                    '%B0%D0%BC%D0%BE%D0%BA_(%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5)', new=2)
                elif self.sign == 3:
                    show_menu()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.widht, self.height))
        text(message, x + 10, y + 10, font_size)


def text(message, x, y, font_size=75, font_type='shrift.otf', font_color=(0, 0, 0)):
    """функция вывода текста на surface"""
    font_result = pygame.font.Font(font_type, font_size)
    texts = font_result.render(message, True, font_color)
    screen.blit(texts, (x, y))


def show_menu():
    """основное меню игры"""
    background = load_image("bg (1).jpg")
   # pygame.mixer.music.load(os.path.join("music", "sky_walk.mp3"))
    #pygame.mixer.music.play(loops=-1)

    button_start = Button(130, 100, 0)
    button_info = Button(130, 100, 1)
    button_story = Button(80, 65, 2)

    demonstration = True
    while demonstration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.close_db()
                demonstration = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                arrow_sprite.update(x, y)
        screen.blit(background, (0, 0))
        text("Moving Castle,", 200, 70, 100)
        button_start.draw(300, 270, "Start", 70)
        button_info.draw(300, 390, "Info", 70)
        button_story.draw(10, 600, "Story", 40)
        if pygame.mouse.get_focused():
            arrow_sprite.draw(screen)
        pygame.display.flip()
    pygame.quit()


def info():
    background = load_image("background_info.jpg")

    button_enter = Button(70, 60, 3)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.close_db()
                running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                arrow_sprite.update(x, y)
        screen.blit(background, (0, 0))
        button_enter.draw(675, 10, "Enter", 40)
        if pygame.mouse.get_focused():
            arrow_sprite.draw(screen)
        pygame.display.flip()
    pygame.quit()


def start_first_game():
    """первый уровень"""

    #pygame.mixer.music.load(os.path.join("music", "first_game.mp3"))
    #pygame.mixer.music.play(loops=-1)
    #pygame.mixer.music.set_volume(0.2)

    player, level_x, level_y = generate_level(load_level("level.txt"))

    counter = 0
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.close_db()
                running = False
            if pygame.key.get_pressed():
                all_sprites.update(pygame.key.get_pressed())
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                arrow_sprite.update(x, y)
        tile_group.draw(screen)
        achievements_group.draw(screen)
        gave_achievement.draw(screen)
        tile_let_group.draw(screen)
        player_group.draw(screen)
        if pygame.mouse.get_focused():
            arrow_sprite.draw(screen)
        text(f"Time: {counter // 60}", 5, 5, 21, None, (255, 255, 255))
        text(f"score: {score}", 85, 5, 21, None, (255, 255, 255))
        counter += 1
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


#def level_controller():

show_menu()



